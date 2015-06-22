#!/usr/bin/env bash
set -e

rm -rf /usr/local/vantage

git clone https://github.com/vantage-org/vantage.git /usr/local/vantage
mkdir /usr/local/vantage/installed

ln -s /usr/local/vantage/vantage /usr/local/bin/vantage
ln -s /usr/local/vantage/vantage /usr/local/bin/vg
