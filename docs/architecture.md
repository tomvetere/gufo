# Architecture

This page describes how Gufo's internal classes interact — the composition
relationships, rendering pipeline, and data flow.

## Class Diagram

```mermaid
classDiagram
    direction TB

    class Chart {
        -_data: Any
        -_layers: list~Layer~
        -_canvas: Canvas
        -_theme_override: Theme | str
        -_palette: list | None
        -_facet_column: str
        -_facet_row: str
        -_apply_funcs: list
        +scatter(x, y, **kw) Chart
        +line(x, y, **kw) Chart
        +bar(x, y, **kw) Chart
        +histogram(x, **kw) Chart
        +kdeplot(x, **kw) Chart
        +boxplot(x, y, **kw) Chart
        +violin(x, y, **kw) Chart
        +heatmap(**kw) Chart
        +area(x, y, **kw) Chart
        +strip(x, y, **kw) Chart
        +swarm(x, y, **kw) Chart
        +countplot(x, **kw) Chart
        +ecdf(x, **kw) Chart
        +rug(x, **kw) Chart
        +pointplot(x, y, **kw) Chart
        +title(text) Chart
        +xlabel(text) Chart
        +ylabel(text) Chart
        +legend(**kw) Chart
        +theme(name_or_theme) Chart
        +palette(colors) Chart
        +facet(column, **kw) Chart
        +apply(func) Chart
        +size(w, h) Chart
        +show()
        +save(path)
        -_render() tuple
        -_render_onto(fig, axes)
        -_apply_decorators(fig, axes)
    }

    class Grid {
        -_rows: int
        -_cols: int
        -_panels: dict~tuple, Chart~
        -_title: str
        -_theme_override: Theme | str
        -_apply_funcs: list
        +__setitem__(idx, chart)
        +title(text) Grid
        +theme(name_or_theme) Grid
        +apply(func) Grid
        +show()
        +save(path)
        -_render() tuple
    }

    class Layer {
        <<dataclass>>
        +mark_type: str
        +x: Any
        +y: Any
        +encodings: dict
        +kwargs: dict
        +palette: list | None
    }

    class Canvas {
        -_figsize: tuple
        -_figure: Figure
        -_axes: Axes
        +build() tuple
        +from_existing(fig, axes)$ Canvas
    }

    class DataAdapter {
        -_data: Any
        -_type: str
        +raw_data: Any
        +data_type: str
        +from_any(data)$ DataAdapter
        +resolve(key) ndarray
        +subset(mask) DataAdapter
        +column_names() list
    }

    class Theme {
        -_name: str
        -_rc: dict
        +name: str
        +merge(overrides) Theme
        +rename(name) Theme
        +as_context() contextmanager
        +apply_global()
    }

    class Palette {
        <<dataclass>>
        +categorical: list~str~
        +sequential: list~str~
        +diverging: list~str~
    }

    class Regression {
        <<dataclass>>
        +degree: int
        +color: str
        +linestyle: str
        +linewidth: float
        +render(x, y, axes)
    }

    class KDE {
        <<dataclass>>
        +bw_method: Any
        +color: str
        +fill: bool
        +n_points: int
        +render(x, axes)
    }

    class Lowess {
        <<dataclass>>
        +frac: float
        +color: str
        +linestyle: str
        +render(x, y, axes)
    }

    Chart "1" *-- "1" Canvas : _canvas
    Chart "1" *-- "0..*" Layer : _layers
    Chart ..> DataAdapter : creates at render time
    Chart ..> Theme : resolves via _resolve_theme()
    Chart ..> Palette : resolves via resolve_palette()

    Grid "1" *-- "0..*" Chart : _panels
    Grid ..> Theme : optional override

    Layer "0..1" o-- Regression : encodings["fit"]
    Layer "0..1" o-- KDE : encodings["kde"]
    Layer "0..1" o-- Lowess : encodings["fit"]
```

## Rendering Pipeline

```mermaid
flowchart TD
    A["chart.show() / chart.save()"] --> B["Chart._render()"]
    B --> C{Faceted?}
    C -- Yes --> D["render_facet()"]
    C -- No --> E["_resolve_theme()"]

    D --> D1["DataAdapter.from_any(data)"]
    D1 --> D2["Split data by facet column"]
    D2 --> D3["plt.subplots(rows, cols)"]
    D3 --> D4["For each category:\nadapter.subset(mask)"]
    D4 --> D5["chart._render_onto(fig, axes, sub_adapter)"]
    D5 --> D6["Shared legend / colorbar"]

    E --> F["theme.as_context()"]
    F --> G["Canvas.build() → fig, axes"]
    G --> H["Chart._render_onto(fig, axes)"]

    H --> I["DataAdapter.from_any(data)"]
    I --> J["resolve_palette()"]
    J --> K["For each Layer"]
    K --> L["render_layer(layer, adapter, axes)"]
    L --> M["_REGISTRY lookup by mark_type"]
    M --> N["mark.render(layer, adapter, axes)"]
    N --> N1["adapter.resolve(x) → numpy"]
    N --> N2["adapter.resolve(y) → numpy"]
    N --> N3["axes.scatter / .plot / .bar / ..."]
    N --> N4{"fit= or kde= overlay?"}
    N4 -- Yes --> N5["overlay.render(x, y, axes)"]

    K --> O["_apply_decorators(fig, axes)"]
    O --> P["title, labels, legend,\nlimits, scales, ticks,\nreferences, annotations"]
    P --> Q["Execute apply(func) callbacks"]

    style A fill:#4C72B0,color:#fff
    style H fill:#55A868,color:#fff
    style N fill:#DD8452,color:#fff
    style O fill:#8172B3,color:#fff
```

## Data Flow

`DataAdapter` is the single resolution point for all input types. Marks never
receive raw DataFrames — they always go through `adapter.resolve(key)`.

```mermaid
flowchart TD
    A["User data"] --> B["DataAdapter.from_any(data)"]

    B --> C{"_detect_type()"}
    C --> C1["pandas DataFrame"]
    C --> C2["polars DataFrame"]
    C --> C3["dict"]
    C --> C4["None (raw arrays)"]

    B --> D["adapter.resolve(key)"]
    D --> E{"key type?"}
    E -- "str" --> F["Column lookup → numpy array"]
    E -- "list of str" --> G["Wide-form → list of arrays"]
    E -- "array-like" --> H["np.asarray() passthrough"]
    E -- "None" --> I["None"]

    F --> J["Mark renderer"]
    G --> J
    H --> J
```

## Layout Relationships

```mermaid
flowchart TD
    subgraph "Entry Points"
        A1["gufo.grid(rows, cols)"] --> G["Grid"]
        A2["gufo.pairplot(data, ...)"] --> G
        A3["gufo.jointplot(data, x, y)"] --> G
    end

    G --> |"__setitem__"| P["Chart panels"]
    G --> |"_render()"| S["plt.subplots(rows, cols)"]
    S --> |"For each panel"| R["chart._render_onto(fig, axes[r,c])"]

    subgraph "Faceting (inside Chart)"
        F1["chart.facet(column)"] --> F2["render_facet()"]
        F2 --> F3["Split data by category"]
        F3 --> F4["chart._render_onto(fig, axes, sub_adapter)"]
    end
```

## Color Resolution

```mermaid
flowchart TD
    A["enc.get('color')"] --> B{"resolve_color()"}
    B -- "None" --> C["Use palette defaults"]
    B -- "Column name" --> D["adapter.resolve() → array"]
    B -- "Literal color" --> E["Apply to all points"]

    D --> F{"Array type?"}
    F -- "Categorical" --> G["iter_color_groups()\nOne color per category"]
    F -- "Continuous numeric" --> H["Colormap + colorbar\n(vmin, vmax, cmap)"]
```
