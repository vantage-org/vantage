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
# help-text: Build the vantage binary for Ubuntu 20.04 (inside a container)
# ---
set -eu

echo "Building $VERSION for ubuntu"

rm -rf venv-ubuntu build/x86_64-unknown-linux-gnu

apt update
apt install --assume-yes software-properties-common build-essential
add-apt-repository ppa:deadsnakes/ppa
apt install --assume-yes python3.9 python3.9-dev python3.9-venv
python3.9 -m venv venv-ubuntu
. venv-ubuntu/bin/activate
pip install -U pip
pip install pyoxidizer==0.16.2

pyoxidizer build

cp -r build/x86_64-unknown-linux-gnu/debug/install "vantage-$VERSION-ubuntu"
cp install.sh README.md LICENSE "vantage-$VERSION-ubuntu/"
tar -cvzf "vantage-$VERSION-ubuntu.tar.gz" "vantage-$VERSION-ubuntu"
