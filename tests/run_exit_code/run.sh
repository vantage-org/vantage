#!/usr/bin/env bash

export VG_PLUGIN_PATH="$VG_PLUGIN_PATH":"$VG_APP_DIR"/tests/run_exit_code

vantage plug run

exit_code=$?

if [[ $exit_code -ne 42 ]]; then
    echo "Exit code $exit_code not 42"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
