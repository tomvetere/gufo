"""Sphinx configuration for cerno documentation."""

import importlib.metadata

# -- Project information -----------------------------------------------------

project = "cerno"
author = "Thomas"
copyright = "2026, Thomas"
release = importlib.metadata.version("cerno")
version = ".".join(release.split(".")[:2])  # "0.1" from "0.1.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "myst_parser",
]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
]

# -- Autodoc configuration ---------------------------------------------------

autodoc_default_options = {
    "members": True,
    "undoc-members": False,
    "show-inheritance": True,
    "member-order": "bysource",
    "special-members": "__init__",
}

autodoc_typehints = "description"
autodoc_typehints_format = "short"
autosummary_generate = True

# -- Intersphinx -------------------------------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "pandas": ("https://pandas.pydata.org/docs", None),
    "numpy": ("https://numpy.org/doc/stable", None),
}

# -- HTML output -------------------------------------------------------------

html_theme = "furo"

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#4C72B0",
        "color-brand-content": "#4C72B0",
    },
    "dark_css_variables": {
        "color-brand-primary": "#6e94d4",
        "color-brand-content": "#6e94d4",
    },
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

html_title = "cerno"
html_logo = "_static/cerno_logo.png"
html_static_path = ["_static"]

# -- Copybutton --------------------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
