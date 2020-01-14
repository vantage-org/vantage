#!/bin/sh
# ---
# help-text: Build the vantage binary
# requires:
#   - test
# ---
. venv/bin/activate
pyinstaller --noconfirm --clean --onedir --name vantage vantage/__main__.py

VERSION=$($VG_BINARY version)

cp -r dist "vantage-$VERSION"
cp install.sh README.md LICENSE "vantage-$VERSION/"
tar -cvzf "vantage-$VERSION.tar.gz" "vantage-$VERSION"

$VG_BINARY clean
