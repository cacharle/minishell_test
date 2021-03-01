# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from pathlib import Path

# -- Project information -----------------------------------------------------

project = 'minishell_test'
copyright = '2021, Charles Cabergs'
author = 'Charles Cabergs'

# The full version, including alpha/beta/rc tags
release = '1.0.1'

# display_github = True

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.extlinks",
    "sphinxcontrib.programoutput",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'README.rst']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    "style_external_links": True,
}

github_url = 'https://github.com/cacharle/minishell_test'
html_context = {
    "display_github": True,
    "github_user": "cacharle",
    "github_repo": "minishell_test",
    "conf_py_path": f"/{Path(__file__).parent.name}/",
    "github_version": "master",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


def setup(app):
    from sphinx.util.docfields import Field
    app.add_object_type(
        directivename="conf",
        rolename="conf",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
        doc_field_types=[
            Field(
                'type',
                label='Type',
                has_arg=False,
                names=('type',),
                bodyrolename='class'
            ),
        ]
    )


extlinks = {
    "issue": ("https://github.com/cacharle/minishell_test/issues/%s", "#"),
    "pull": ("https://github.com/cacharle/minishell_test/pull/%s", "p"),
    "user": ("https://github.com/%s", "@"),
}
