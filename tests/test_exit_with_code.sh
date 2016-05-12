#!/bin/bash

. assert.sh

assert_raises "vantage exit 145" 145

assert_end exit_with_code
