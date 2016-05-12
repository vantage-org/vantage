#!/bin/bash

. assert.sh

# Finds .vantage file in CWD
cd .. || exit
assert "vantage __env VG_APP_DIR" "$(pwd)"
cd - || exit

# Travels up the file system until it finds a .vantage file
assert "vantage __env VG_APP_DIR" "/vagrant"

# Can be set as an ENV var
VG_APP_DIR=/foo assert "vantage __env VG_APP_DIR" "/foo"

# Can be set as a var
assert "vantage --var VG_APP_DIR=/foo __env VG_APP_DIR" "/foo"

# Otherwise assumes CWD
cd ~ || exit
assert "vantage __env VG_APP_DIR" "$(pwd)"
cd - || exit

assert_end app_dir
