"""Generate gallery images for the gufo documentation."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ensure gufo is importable from the repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import gufo

OUT = Path(__file__).resolve().parents[1] / "_static" / "gallery"
OUT.mkdir(parents=True, exist_ok=True)

# ── Synthetic data ─────────────────────────────────────────────────

rng = np.random.default_rng(42)

n = 80
df = pd.DataFrame({
    "x": rng.normal(50, 15, n),
    "y": rng.normal(50, 15, n),
    "size": rng.uniform(10, 100, n),
    "value": rng.uniform(0, 1, n),
    "category": rng.choice(["A", "B", "C"], n),
    "group": rng.choice(["alpha", "beta"], n),
})
df["y"] = df["x"] * 0.6 + rng.normal(0, 8, n)

time_x = list(range(1, 11))
line_df = pd.DataFrame({
    "day": time_x * 3,
    "sales": ([10, 15, 13, 17, 20, 18, 25, 28, 30, 35]
              + [8, 12, 11, 14, 16, 19, 22, 21, 26, 29]
              + [5, 9, 10, 12, 11, 15, 17, 20, 22, 25]),
    "channel": ["online"] * 10 + ["retail"] * 10 + ["wholesale"] * 10,
})

bar_df = pd.DataFrame({
    "fruit": ["apple", "banana", "cherry", "apple", "banana", "cherry"],
    "count": [30, 25, 15, 20, 30, 25],
    "region": ["east", "east", "east", "west", "west", "west"],
})

box_df = pd.DataFrame({
    "group": (["A"] * 30 + ["B"] * 30 + ["C"] * 30),
    "value": np.concatenate([
        rng.normal(50, 10, 30),
        rng.normal(60, 8, 30),
        rng.normal(45, 12, 30),
    ]),
    "sub": rng.choice(["x", "y"], 90),
})

heatmap_df = pd.DataFrame(
    rng.uniform(0, 100, (5, 5)).round(1),
    index=["Mon", "Tue", "Wed", "Thu", "Fri"],
    columns=["Q1", "Q2", "Q3", "Q4", "Q5"],
)

area_df = pd.DataFrame({
    "month": list(range(1, 13)),
    "product_a": [10, 15, 13, 18, 22, 28, 35, 33, 30, 25, 20, 18],
    "product_b": [5, 8, 10, 12, 14, 18, 20, 22, 19, 16, 12, 9],
    "product_c": [3, 4, 5, 6, 8, 10, 12, 11, 10, 8, 6, 4],
})


def save(name):
    """Close all figures after saving — just a convenience."""
    plt.close("all")
    print(f"  {name}")


# ── Gallery images ─────────────────────────────────────────────────

print("Generating gallery images...")

# 1. Scatter with color + size
(
    gufo.chart(df)
    .scatter("x", "y", color="category", size="size")
    .title("Scatter — color + size")
    .xlabel("X").ylabel("Y")
    .save(OUT / "scatter.png")
)
save("scatter.png")

# 2. Line (multi-series)
(
    gufo.chart(line_df)
    .line("day", "sales", color="channel")
    .title("Line — multi-series")
    .xlabel("Day").ylabel("Sales")
    .legend()
    .save(OUT / "line.png")
)
save("line.png")

# 3. Bar (grouped)
(
    gufo.chart(bar_df)
    .bar("fruit", "count", color="region")
    .title("Bar — grouped")
    .save(OUT / "bar_grouped.png")
)
save("bar_grouped.png")

# 4. Bar (stacked)
(
    gufo.chart(bar_df)
    .bar("fruit", "count", color="region", stacked=True)
    .title("Bar — stacked")
    .save(OUT / "bar_stacked.png")
)
save("bar_stacked.png")

# 5. Histogram with KDE
(
    gufo.chart(df)
    .histogram("x", kde=gufo.kde())
    .title("Histogram — with KDE overlay")
    .save(OUT / "histogram_kde.png")
)
save("histogram_kde.png")

# 6. Boxplot with categorical color
(
    gufo.chart(box_df)
    .boxplot("group", "value", color="sub")
    .title("Box plot — categorical color")
    .save(OUT / "boxplot.png")
)
save("boxplot.png")

# 7. Violin
(
    gufo.chart(box_df)
    .violin("group", "value", color="sub")
    .title("Violin plot")
    .save(OUT / "violin.png")
)
save("violin.png")

# 8. Heatmap (annotated)
(
    gufo.chart(heatmap_df)
    .heatmap(annotate=True, cmap="YlOrRd")
    .title("Heatmap — annotated")
    .save(OUT / "heatmap.png")
)
save("heatmap.png")

# 9. Area (stacked)
(
    gufo.chart(area_df)
    .area("month", ["product_a", "product_b", "product_c"])
    .title("Area — stacked")
    .xlabel("Month").ylabel("Revenue")
    .save(OUT / "area.png")
)
save("area.png")

# 10. KDE (filled)
(
    gufo.chart(df)
    .kdeplot("x", fill=True, color="category")
    .title("KDE — filled density")
    .save(OUT / "kde.png")
)
save("kde.png")

# 11. Strip
(
    gufo.chart(box_df)
    .strip("group", "value", color="sub", alpha=0.6)
    .title("Strip plot")
    .save(OUT / "strip.png")
)
save("strip.png")

# 12. Swarm
(
    gufo.chart(box_df)
    .swarm("group", "value", alpha=0.6)
    .title("Swarm plot")
    .save(OUT / "swarm.png")
)
save("swarm.png")

# 13. Countplot (grouped)
count_df = pd.DataFrame({
    "animal": rng.choice(["cat", "dog", "fish", "bird"], 100),
    "owner": rng.choice(["Alice", "Bob"], 100),
})
(
    gufo.chart(count_df)
    .countplot("animal", color="owner")
    .title("Count plot — grouped")
    .save(OUT / "countplot.png")
)
save("countplot.png")

# 14. ECDF
(
    gufo.chart(df)
    .ecdf("x", color="category")
    .title("ECDF")
    .save(OUT / "ecdf.png")
)
save("ecdf.png")

# 15. Rug (layered with histogram)
(
    gufo.chart(df)
    .histogram("x")
    .rug("x", color="red")
    .title("Histogram + rug plot")
    .save(OUT / "rug.png")
)
save("rug.png")

# 16. Pairplot
pair_df = pd.DataFrame({
    "a": rng.normal(0, 1, 60),
    "b": rng.normal(0, 1, 60),
    "c": rng.normal(0, 1, 60),
    "species": rng.choice(["x", "y"], 60),
})
gufo.pairplot(pair_df, ["a", "b", "c"], color="species").save(OUT / "pairplot.png")
save("pairplot.png")

# 17. Jointplot
gufo.jointplot(df, "x", "y").save(OUT / "jointplot.png")
save("jointplot.png")

# 18. Scatter with continuous color + colorbar
(
    gufo.chart(df)
    .scatter("x", "y", color="value", cmap="viridis")
    .title("Scatter — continuous color")
    .save(OUT / "scatter_continuous.png")
)
save("scatter_continuous.png")

# 19. Faceted scatter
(
    gufo.chart(df)
    .scatter("x", "y")
    .facet("category")
    .title("Scatter — faceted")
    .save(OUT / "faceted.png")
)
save("faceted.png")

print(f"\nDone — {len(list(OUT.glob('*.png')))} images in {OUT}")
