#!/usr/bin/env bash
set -e

rm -rf /usr/local/vantage
git clone https://github.com/WilliamMayor/vantage.git /usr/local/vantage
cd /usr/local/vantage
make install
