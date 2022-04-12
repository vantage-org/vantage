#!/bin/sh
# ---
# help-text: Build the vantage binary for M1 chip Macs. Must be run on a MacOS M1 host.
# ---
set -eu

echo "Building $VERSION for MacOS (M1)"

cd "$VG_APP_DIR"

rm -rf venv-macos-m1 build/aarch64-apple-darwin

python3.9 -m venv venv-macos-m1
. venv-macos-m1/bin/activate
pip install -U pip
pip install pyoxidizer==0.18.0

pyoxidizer build
# pyoxidizer analyze build/aarch64-apple-darwin/debug/install/vantage

cp -r build/aarch64-apple-darwin/debug/install "build/vantage-$VERSION-macos-m1"
chmod +x "build/vantage-$VERSION-macos-m1/vantage"
cp install.sh README.md LICENSE "build/vantage-$VERSION-macos-m1/"

cd build
tar -cvzf "vantage-$VERSION-macos-m1.tar.gz" "vantage-$VERSION-macos-m1"

rm -rf venv-macos-m1
