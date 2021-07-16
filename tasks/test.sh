#!/bin/sh
# ---
# help-text: Run the test suite
# ---
set -e
(
    cd "$VG_APP_DIR"
    if [ ! -d venv-test ]; then
        python3.9 -m venv venv-test
        . venv-test/bin/activate
        pip install -U pip
        pip install pytest
        pip install -e .
    else
        . venv-test/bin/activate
    fi
    cd tests/cases
    pytest --basetemp="$VG_APP_DIR/tests/tmp" "$@"
)
