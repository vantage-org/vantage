#!/bin/bash

. assert.sh

VG="$(pwd)/../vantage"

assert "$VG __list_scripts" "hw\npong\ntests\n__env\n__list_env_files\n__list_scripts\n__plugins\n__update"

assert "$VG __list_scripts -h" "hw\npong\ntests\n__env\n__list_env_files\n__list_scripts\n__plugins\n__update"

assert "$VG __list_scripts -v FOO=bar" "hw\npong\ntests\n__env\n__list_env_files\n__list_scripts\n__plugins\n__update"
assert "$VG __list_scripts -e one" "hw\npong\ntests\n__env\n__list_env_files\n__list_scripts\n__plugins\n__update"
assert "$VG __list_scripts -a /vantage" "hw\npong\ntests\n__env\n__list_env_files\n__list_scripts\n__plugins\n__update"

assert "$VG __list_scripts hw " "hw\nreverse\ntranslate"

assert "$VG __list_scripts hw tr" "hw\nreverse\ntranslate"

assert "$VG __list_scripts hw translate" "french"

assert "$VG __list_scripts hw translate french" ""

assert_end list_scripts
