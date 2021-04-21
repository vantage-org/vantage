#!/bin/sh
set -eu

echo "Building $VERSION"

rm -rf venv-debian dist build
vg --var VERSION build debian

rm -rf venv-ubuntu dist build venv-debian
vg --var VERSION build ubuntu

rm -rf venv-macos dist build venv-ubuntu
vg --var VERSION build macos

rm -rf venv-macos
