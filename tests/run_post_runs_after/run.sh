#!/usr/bin/env bash

export VG_PLUGIN_PATH="$VG_PLUGIN_PATH":"$VG_APP_DIR"/tests/run_post_runs_after

output=$(vantage plug run)

if [[ "$output" != 'commands'$'\n''post' ]]; then
    echo "Post didn't run after commands"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
