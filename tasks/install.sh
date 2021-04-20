#!/bin/sh
# ---
# help-text: Install this dev version to /usr/local/bin/vg-next
# requires:
#   - build
# ---
rm -f /usr/local/bin/vg-next
ln -s "$VG_APP_DIR/dist/vantage/vantage" /usr/local/bin/vg-next
