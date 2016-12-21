#!/bin/bash

. assert.sh

# Uses default env
VG_DEFAULT_ENV=../.env/one assert "vantage __env FOO" "one"

# Uses env by path
assert "vantage -e ../.env/one __env FOO" "one"

# Uses env by name
VG_ENV_DIR=../.env assert "vantage -e one __env FOO" "one"

# Uses ENV from .vantage
assert "vantage __env FOO" ".vantage"

# Uses var
assert "vantage -v FOO=var __env FOO" "var"

# CLI env overrides default env
VG_DEFAULT_ENV=../.env/one assert "vantage -e ../.env/two __env FOO" "two"

# Var overrides env
assert "vantage -e ../.env/one -v FOO=var __env FOO" "var"
assert "vantage -v FOO=var -e ../.env/one __env FOO" "var"

# Can use env from command line
VG_DEFAULT_ENV=../.env/one assert "vantage 'echo \$FOO'" "one"

# Temp env file is deleted
temp_env_file=$(vantage __env VG_ENV_FILE)
assert_raises "[ -f $temp_env_file ]" "1"

# Set env in default env
touch ../.env/default
VG_DEFAULT_ENV=../.env/default vantage __env FOO default
assert_raises "grep -q 'FOO=default' ../.env/default"
rm ../.env/default

# Override set env
touch ../.env/default
VG_DEFAULT_ENV=../.env/default vantage __env FOO wrong
VG_DEFAULT_ENV=../.env/default vantage __env FOO default
assert_raises "grep -q 'FOO=default' ../.env/default"
assert_raises "grep -qv 'FOO=wrong' ../.env/default"
rm ../.env/default

# Set env in named env
touch ../.env/default
touch ../.env/named
VG_DEFAULT_ENV=../.env/default vantage -e ../.env/named __env FOO named
assert "cat ../.env/default" ""
assert_raises "grep -q 'FOO=named' ../.env/named"
rm ../.env/default
rm ../.env/named

assert_end env
