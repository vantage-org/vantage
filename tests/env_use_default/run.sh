#!/usr/bin/env bash
# If a default env file has been set, use that

export VG_DEFAULT_ENV="$VG_APP_DIR"/tests/env_use_default/env


output=$(vantage config file)

if [[ "$output" != "/tmp/"* ]]; then
    echo "No temp file for env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

output=$(vantage config get)

if [[ "$output" != *"FOO=BAR"* ]]; then
    echo "Not loading default env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
