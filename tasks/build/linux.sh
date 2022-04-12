#!/bin/sh
# ---
# help-text: Build the vantage binary for Linux. Must be run on a Linux host.
# ---
set -eu

echo "Building $VERSION for linux"

rm -rf venv-linux build/x86_64-unknown-linux-gnu

python -m venv venv-linux
. venv-linux/bin/activate
pip install -U pip
pip install pyoxidizer==0.18.0

pyoxidizer build

cp -r build/x86_64-unknown-linux-gnu/debug/install "build/vantage-$VERSION-linux"
chmod +x "build/vantage-$VERSION-linux/vantage"
cp install.sh README.md LICENSE "build/vantage-$VERSION-linux/"

cd build
tar -cvzf "vantage-$VERSION-linux.tar.gz" "vantage-$VERSION-linux"

rm -rf venv-linux
