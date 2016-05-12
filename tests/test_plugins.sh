#!/bin/bash

. assert.sh

# Run a plugin inside the plugin path
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage hw" "Hello World!"

# Run a sub-command of a plugin
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage hw reverse" "World Hello!"

# Run a sub-script inside a plugin
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage hw help" "Prints hello world"

# Run a plugin using an alias
VG_PLUGIN_PATH=/vagrant/plugins/dogfood assert "vantage greeter" "Hello World!"

assert_end plugins
