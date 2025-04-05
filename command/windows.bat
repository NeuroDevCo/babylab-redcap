@echo off
set URL=http://127.0.0.1:5000

REM Try to open in Edge
start msedge %URL%
if errorlevel 1 (
    REM If Edge is not installed, try Firefox
    start firefox %URL%
    if errorlevel 1 (
        REM If Firefox is not installed, try Chrome
        start chrome %URL%
        if errorlevel 1 (
            echo "No supported browser found."
        )
    )
)

python -m flask --app babylab.app run
