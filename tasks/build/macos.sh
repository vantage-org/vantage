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
pip install pyoxidizer==0.18.0

pyoxidizer build
# pyoxidizer analyze build/x86_64-apple-darwin/debug/install/vantage

cp -r build/x86_64-apple-darwin/debug/install "build/vantage-$VERSION-macos"
chmod +x "build/vantage-$VERSION-macos/vantage"
cp install.sh README.md LICENSE "build/vantage-$VERSION-macos/"

cd build
tar -cvzf "vantage-$VERSION-macos.tar.gz" "vantage-$VERSION-macos"

rm -rf venv-macos
