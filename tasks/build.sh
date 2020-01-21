#!/bin/sh
# ---
# help-text: Build the vantage binary
# requires:
#   - test
# ---
set -e
. venv/bin/activate
pyinstaller --noconfirm --clean --onedir --name vantage vantage/__main__.py

VERSION=$(vantage __version)

cp -r dist "vantage-$VERSION"
cp install.sh README.md LICENSE "vantage-$VERSION/"
tar -cvzf "vantage-$VERSION.tar.gz" "vantage-$VERSION"
