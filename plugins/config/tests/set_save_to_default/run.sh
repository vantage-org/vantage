#!/usr/bin/env bash

env=$(mktemp)
unset VG_ENV_FILE
export VG_DEFAULT_ENV="$env"

vantage config set --save FOO=BAR

output=$(cat "$env")

if [[ "$output" != "FOO=BAR" ]]; then
    echo "Set var not saved to default"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
