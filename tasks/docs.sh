#!/bin/sh
# ---
# help-text: Build the documentation
# ---
set -e
(
    cd "$VG_APP_DIR"
    if [ ! -d venv-docs ]; then
        python3.9 -m venv venv-docs
        . venv-docs/bin/activate
        pip install -U pip
        pip install mkdocs-material mkdocstrings mkdocs-git-revision-date-plugin
        pip install -e .
    else
        . venv-docs/bin/activate
    fi
    mkdocs serve
)
