#!/bin/sh
set -e

echo "Removing any existing vantage installations..."
rm -rf /usr/local/vantage /usr/local/bin/vantage /usr/local/bin/vg

echo "Moving vantage to /usr/local/vantage..."
mkdir -p /usr/local/vantage
mv ./vantage ./README.md ./LICENSE /usr/local/vantage

echo "Linking executables to /usr/local/bin/..."
ln -s /usr/local/vantage/vantage /usr/local/bin/vantage
ln -s /usr/local/vantage/vantage /usr/local/bin/vg

echo "Done!"
echo "Run 'vantage --help' to see what to do now :)"
