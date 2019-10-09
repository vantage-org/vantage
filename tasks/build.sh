#!/bin/sh
# ---
# help-text: Build the vantage binary
# requires:
#   - init
# ---
. venv/bin/activate
pyinstaller --noconfirm --clean --onefile --name vantage vantage/__main__.py
