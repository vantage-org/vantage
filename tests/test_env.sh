#!/bin/bash

. assert.sh

# Uses default env
VG_DEFAULT_ENV=/vagrant/.env/one assert "vantage __env FOO" "one"

# Uses env by path
assert "vantage -e /vagrant/.env/one __env FOO" "one"

# Uses env by name
VG_ENV_DIR=/vagrant/.env assert "vantage -e one __env FOO" "one"

# Uses ENV from .vantage
assert "vantage __env FOO" ".vantage"

# Uses var
assert "vantage -v FOO=var __env FOO" "var"

# CLI env overrides default env
VG_DEFAULT_ENV=/vagrant/.env/one assert "vantage -e /vagrant/.env/two __env FOO" "two"

# Var overrides env
assert "vantage -e /vagrant/.env/one -v FOO=var __env FOO" "var"
assert "vantage -v FOO=var -e /vagrant/.env/one __env FOO" "var"

# Can use env from command line
VG_DEFAULT_ENV=/vagrant/.env/one assert "vantage 'echo \$FOO'" "one"

# Temp env file is deleted
temp_env_file=$(vantage __env VG_ENV_FILE)
assert_raises "[ -f $temp_env_file ]" "1"

assert_end env
