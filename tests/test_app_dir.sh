#!/bin/bash
set -e

. assert.sh

# Finds .vantage file in CWD
cd .. > /dev/null
assert "vantage __env VG_APP_DIR" "$(pwd)"
cd - > /dev/null

# Travels up the file system until it finds a .vantage file
assert "vantage __env VG_APP_DIR" "$(dirname $(pwd))"

# Can be set as an ENV var
VG_APP_DIR=/foo assert "vantage __env VG_APP_DIR" "/foo"

# Can be set as an option
assert "vantage -a /foo __env VG_APP_DIR" "/foo"

# Otherwise assumes CWD
cd ~ > /dev/null
assert "vantage __env VG_APP_DIR" "$(pwd)"
cd - > /dev/null

assert_end app_dir
