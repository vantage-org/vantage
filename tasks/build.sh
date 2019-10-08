#!/bin/sh
# ---
# requires:
#   - init
# ---
. venv/bin/activate
pyinstaller --noconfirm --clean --onefile --name vantage vantage/__main__.py
