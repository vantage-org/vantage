#!/usr/bin/env bash

export VG_ENV_FILE=$(mktemp)

vantage config set FOO=BAR

output=$(vantage config get FOO)

if [[ "$output" != "BAR" ]]; then
    echo "Not getting the set env value"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
