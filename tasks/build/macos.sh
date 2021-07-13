#!/bin/sh
# ---
# help-text: Build the vantage binary for MacOS. Must be run on a MacOS host.
# ---
set -eu

echo "Building $VERSION for MacOS"

cd "$VG_APP_DIR"

rm -rf venv-macos build/x86_64-apple-darwin

python3.9 -m venv venv-macos
. venv-macos/bin/activate
pip install -U pip
pip install pyoxidizer==0.16.2

pyoxidizer build

cp -r build/x86_64-apple-darwin/debug/install "build/vantage-$VERSION-macos"
cp install.sh README.md LICENSE "build/vantage-$VERSION-macos/"

cd build
tar -cvzf "vantage-$VERSION-macos.tar.gz" "vantage-$VERSION-macos"

rm -rf venv-macos
