#!/bin/sh
# ---
# help-text: Install this dev version to /usr/local/bin/vg-next
# requires:
#   - build
# ---
sudo rm /usr/local/bin/vg-next
sudo ln -s "$VG_APP_DIR/dist/vantage/vantage" /usr/local/bin/vg-next
