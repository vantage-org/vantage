#!/usr/bin/env bash

output=$(vantage unknown)

if [[ $output == "vantage: unknown: Command not found"* ]]; then
    if [[ $output == *"Usage: vantage [--env|-e ENV_FILE [...]] COMMAND [OPTIONS]"* ]]; then
        exit $VG_TEST_PASSED
    fi
fi

echo "$output"
exit $VG_TEST_FAILED
