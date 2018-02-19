#!/bin/bash

. assert.sh

VG="$(pwd)/../vantage"

# Prints env files
assert "$VG __list_env_files" "one\ntwo"

assert_end list_env_files
