#!/bin/bash

. assert.sh

# Run a core plugin
assert_raises "vantage __env"

# Run a simple script plugin
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage pong" "ping"

# Run a plugin inside a directory
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage hw" "Hello World!"

# Run a sub-command of a plugin
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage hw reverse" "World Hello!"

# Run a nested sub-command of a plugin
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage hw translate french" "Bonjour World!"

assert_end plugins
