#!/bin/bash

. assert.sh

VG="$(pwd)/../vantage"

# Run a core plugin
assert_raises "$VG __env"

# Run a simple script plugin
VG_PLUGIN_PATH=../plugins/dogfood assert "$VG pong" "ping"

# Run a plugin inside a directory
VG_PLUGIN_PATH=../plugins/dogfood assert "$VG hw" "Hello World!"

# Run a sub-command of a plugin
VG_PLUGIN_PATH=../plugins/dogfood assert "$VG hw reverse" "World Hello!"

# Run a nested sub-command of a plugin
VG_PLUGIN_PATH=../plugins/dogfood assert "$VG hw translate french" "Bonjour World!"

assert_end plugins
