#!/bin/sh
# ---
# help-text: Build the vantage binary
# requires:
#   - test
# ---
. venv/bin/activate
pyinstaller --noconfirm --clean --onedir --name vantage vantage/__main__.py
