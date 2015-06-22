#!/usr/bin/env bash
# The env file created by vantage shuld be deleted after vantage has completed

output=$(vantage config file)

if [[ -f "$output" ]]; then
    echo "Didn't delete env file"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
