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

# Set env in default env
touch /vagrant/.env/default
VG_DEFAULT_ENV=/vagrant/.env/default vantage __env FOO default
assert "cat /vagrant/.env/default" "FOO=default"
rm /vagrant/.env/default

# Override set env
touch /vagrant/.env/default
VG_DEFAULT_ENV=/vagrant/.env/default vantage __env FOO wrong
VG_DEFAULT_ENV=/vagrant/.env/default vantage __env FOO default
assert "cat /vagrant/.env/default" "FOO=default"
rm /vagrant/.env/default

# Set env in named env
touch /vagrant/.env/default
touch /vagrant/.env/named
VG_DEFAULT_ENV=/vagrant/.env/default vantage -e /vagrant/.env/named __env FOO named
assert "cat /vagrant/.env/default" ""
assert "cat /vagrant/.env/named" "FOO=named"
rm /vagrant/.env/default
rm /vagrant/.env/named

assert_end env
