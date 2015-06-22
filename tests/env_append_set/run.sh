#!/usr/bin/env bash
# If you provide a --env FILE argument to vantage it should append the
# variables in FILE to the current VG_ENV_FILE. FILE should take precedence

output=$(vantage --env "$VG_APP_DIR"/tests/env_append_set/extra config file)

if [[ "$output" != "/tmp/"* ]]; then
    echo "No temp file for env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

output=$(vantage --env "$VG_APP_DIR"/tests/env_append_set/extra config get)

if [[ "$output" != *"FOO=BAR"* && "$output" != *"BAR=FOO"* ]]; then
    echo "Not loading set env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
