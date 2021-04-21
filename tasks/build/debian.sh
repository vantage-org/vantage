#!/bin/sh
# ---
# image:
#   tag: "debian:10.7"
#   rm: true
#   tty: true
#   interactive: true
#   volume:
#     - $VG_APP_DIR:/usr/src/app
#   workdir: /usr/src/app
# help-text: Build the vantage binary for Debian 10.7 (Buster)
# ---
set -eu

echo "Building $VERSION for debian"

apt-get update
apt-get install --assume-yes python3 python3-venv python3-pip

rm -rf venv-debian dist build
python3 -m venv venv-debian
. venv-debian/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .

pyinstaller --noconfirm --clean --onedir --name vantage vantage/__main__.py

cp -r dist "vantage-$VERSION-debian"
cp install.sh README.md LICENSE "vantage-$VERSION-debian/"
tar -cvzf "vantage-$VERSION-debian.tar.gz" -C "vantage-$VERSION-debian" .
