#!/bin/bash
URL="http://127.0.0.1:5000"

if open -a "Safari" "$URL" & python3 -m flask --app babylab.app run; then
    exit 0
elif open -a "Microsoft Edge" "$URL" & python3 -m flask --app babylab.app run; then
    exit 0
elif open -a "Firefox" "$URL" & python3 -m flask --app babylab.app run; then
    exit 0
elif open -a "Google Chrome" "$URL" & python3 -m flask --app babylab.app run; then
    exit 0
else
    echo "No supported browser found."
    exit 1
fi