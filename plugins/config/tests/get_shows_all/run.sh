#!/usr/bin/env bash

unset VG_ENV_FILE
export VG_DEFAULT_ENV="$VG_APP_DIR"/plugins/config/tests/get_shows_all/default

output=$(vantage --env "$VG_APP_DIR"/plugins/config/tests/get_shows_all/extra config get)

if [[ "$output" != *"ONE=1"*"TWO=2"* ]]; then
    echo "Not getting all env"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
