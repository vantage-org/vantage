#!/usr/bin/env bash

export VG_PLUGIN_PATH="$VG_PLUGIN_PATH":"$VG_APP_DIR"/tests/run_pre_runs_first

output=$(vantage plug run)

if [[ "$output" != 'pre'$'\n''commands' ]]; then
    echo "Pre didn't run before commands"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
