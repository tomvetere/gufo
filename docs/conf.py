"""Sphinx configuration for gufo documentation."""

import importlib.metadata

# -- Project information -----------------------------------------------------

project = "gufo"
author = "Thomas"
copyright = "2026, Thomas"
release = importlib.metadata.version("gufo")
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
    "sphinxcontrib.mermaid",
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

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "logo": {
        "image_light": "_static/gufo_logo.png",
        "image_dark": "_static/gufo_logo.png",
    },
    "github_url": "https://github.com/tomvetere/gufo",
    "navbar_align": "left",
    "navigation_with_keys": True,
}

html_title = "gufo"
html_static_path = ["_static"]

# -- Copybutton --------------------------------------------------------------

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
