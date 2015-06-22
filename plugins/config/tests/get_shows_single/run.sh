#!/usr/bin/env bash

unset VG_ENV_FILE
export VG_DEFAULT_ENV="$VG_APP_DIR"/plugins/config/tests/get_shows_single/default

output=$(vantage --env "$VG_APP_DIR"/plugins/config/tests/get_shows_single/extra config get FOO)

if [[ "$output" != "BAR" ]]; then
    echo "Not getting env value"
    echo "$output"
    exit $VG_TEST_FAILED
fi

exit $VG_TEST_PASSED
