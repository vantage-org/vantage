#!/usr/bin/env bash

export VG_ENV_FILE=$(mktemp)

vantage config set ONE=1 TWO=2

output=$(vantage config get ONE)

if [[ "$output" != "1" ]]; then
    echo "Not getting the first set env value"
    echo "$output"
    exit $VG_TEST_FAILED
fi

output=$(vantage config get TWO)

if [[ "$output" != "2" ]]; then
    echo "Not getting the first set env value"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
