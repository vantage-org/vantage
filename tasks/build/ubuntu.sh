#!/bin/sh
# ---
# image:
#   tag: "ubuntu:20.04"
#   rm: true
#   tty: true
#   interactive: true
#   volume:
#     - $VG_APP_DIR:/usr/src/app
#   workdir: /usr/src/app
# help-text: Build the vantage binary for Ubuntu 20.04
# ---
set -eu

echo "Building $VERSION for ubuntu"

apt-get update
apt-get install --assume-yes python3 python3-venv python3-pip

rm -rf venv dist build
python3 -m venv venv
. venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install -e .

pyinstaller --noconfirm --clean --onedir --name vantage vantage/__main__.py

cp -r dist "vantage-$VERSION-ubuntu"
cp install.sh README.md LICENSE "vantage-$VERSION-ubuntu/"
tar -cvzf "vantage-$VERSION-ubuntu.tar.gz" -C "vantage-$VERSION-ubuntu" .
