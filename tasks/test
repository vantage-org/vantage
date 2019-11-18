#!/bin/sh
# ---
# help-text: Run the test suite
# requires:
#   - init
# ---
set -e
(
    cd "$VG_APP_DIR"
    . venv/bin/activate
    cd tests/cases
    pytest --basetemp="$VG_APP_DIR/tests/tmp" "$@"
)
