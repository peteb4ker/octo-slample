"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:

https://www.sphinx-doc.org/en/master/usage/configuration.html

Project information
https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""
from __future__ import annotations


project = "octo-slample"
copyright = "2023, Pete Baker <peteb4ker@gmail.com>"
author = "Pete Baker <peteb4ker@gmail.com>"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_click.ext",
    "sphinx_rtd_theme",
    "sphinx.ext.coverage",
    "autoapi.extension",
]

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    ".pytest_cache",
    "venv",
]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"

coverage_show_missing_items = True

autoapi_type = "python"
autoapi_dirs = ["octo_slample"]
