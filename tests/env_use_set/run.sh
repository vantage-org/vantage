#!/usr/bin/env bash
# If the VG_ENV_FILE has been set, use that

export VG_ENV_FILE="$VG_APP_DIR"/tests/env_use_set/env

output=$(vantage config file)

if [[ "$output" != "/tmp/"* ]]; then
    echo "Not copying set env to temp"
    echo "$output"
    exit $VG_TEST_FAILED
fi

output=$(vantage config get)

if [[ "$output" != *"FOO=BAR"* ]]; then
    echo "Not loading set env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
