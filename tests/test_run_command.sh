#!/bin/bash

. assert.sh

assert_raises "vantage exit 145" 145
assert "vantage echo hello" "hello"

assert_end run_command
