#!/usr/bin/env bash

env=$(mktemp)

vantage --env "$env" config set -s FOO=BAR

output=$(cat "$env")

if [[ "$output" != "FOO=BAR" ]]; then
    echo "Set var not saved to extra"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
