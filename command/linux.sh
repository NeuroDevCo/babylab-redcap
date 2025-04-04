#!/bin/sh

sudo apt-get -y install xdg-utils firefox python3
python3 -m pip install babylab waitress python-dotenv flask

URL="http://127.0.0.1:5000"

if command -v firefox > /dev/null; then
    python3 -m flask --app babylab.app run & firefox "$URL"
elif command -v google-chrome > /dev/null; then
    # If Firefox is not installed, try Chrome
    python3 -m flask --app babylab.app run & google-chrome "$URL"
else
    echo "No supported browser found."
fi