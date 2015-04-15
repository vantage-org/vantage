#!/usr/bin/env bash
set -eo pipefail
shopt -s nullglob

rm -rf /usr/local/vantage
git clone https://github.com/WilliamMayor/vantage.git /usr/local/vantage
cd /usr/local/vantage
make install
