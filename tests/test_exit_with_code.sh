#!/bin/bash

. assert.sh

VG="$(pwd)/../vantage"

assert_raises "$VG exit 145" 145

assert_end exit_with_code
