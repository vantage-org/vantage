#!/usr/bin/env bash
# If you provide a --env FILE argument to vantage it will append the variables
# in FILE to the default env. FILE should take precedence over the default.

export VG_DEFAULT_ENV="$VG_APP_DIR"/tests/env_append_default/default

output=$(vantage --env "$VG_APP_DIR"/tests/env_append_default/extra config file)

if [[ "$output" != "/tmp/"* ]]; then
    echo "No temp file for env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

output=$(vantage --env "$VG_APP_DIR"/tests/env_append_default/extra config get)

if [[ "$output" != *"FOO=BAR"*"BAR=FOO"* ]]; then
    echo "Not loading set env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
