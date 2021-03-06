#!/bin/sh
# ---
# help-text: Build the vantage binary for MacOS. Must be run on a MacOS host.
# ---
set -eu

echo "Building $VERSION for MacOS"

python3 -m venv venv-macos
. venv-macos/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .

pyinstaller --noconfirm --clean --onedir --name vantage vantage/__main__.py

cp -r dist "vantage-$VERSION-macos"
cp install.sh README.md LICENSE "vantage-$VERSION-macos/"
tar -cvzf "vantage-$VERSION-macos.tar.gz" "vantage-$VERSION-macos"
