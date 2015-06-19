#!/usr/bin/env bash

output=$(vantage help)

if [[ $output == "Usage: vantage [--env|-e ENV_FILE [...]] COMMAND [OPTIONS]"* ]]; then
    exit $VG_TEST_PASSED
fi
echo "$output"
exit $VG_TEST_FAILED
