#!/bin/bash

. assert.sh

VG="$(pwd)/../vantage"

assert_raises "$VG exit 145" 145
assert "$VG echo hello" "hello"

assert_end run_command
