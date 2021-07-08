#!/bin/sh
# ---
# help-text: Run the test suite
# ---
set -e
(
    cd "$VG_APP_DIR"
    if [ ! -d venv ]; then
        python3.9 -m venv venv
        . venv/bin/activate
        pip install pytest
        pip install . -e
    else
        . venv/bin/activate
    fi
    cd tests/cases
    pytest --basetemp="$VG_APP_DIR/tests/tmp" "$@"
)
