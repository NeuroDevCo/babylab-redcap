@echo off
setlocal

REM Step 1: Ensure Python 3.12.0 is installed and on PATH
set PY312_PATH=C:\Program Files\Python312
set PY312_EXE="%PY312_PATH%\python.exe"

REM Check if Python 3.12.0 exists
if not exist %PY312_EXE% (
    echo Python 3.12.0 not found. Downloading and installing...
    set PYTHON_INSTALLER=python-3.12.0-amd64.exe
    if not exist "%PYTHON_INSTALLER%" (
        curl -LO https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    )
    "%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del "%PYTHON_INSTALLER%"
    REM Wait for install to complete
    timeout /t 5 >nul
    if not exist %PY312_EXE% (
        echo Failed to install Python 3.12.0. Exiting.
        pause
        exit /b 1
    )
)

REM Add Python 3.12.0 to PATH for this session
set "PATH=%PY312_PATH%;%PY312_PATH%\Scripts;%PATH%"

REM Step 2: Install or upgrade babylab
%PY312_EXE% -m ensurepip --upgrade
%PY312_EXE% -m pip install --upgrade pip
%PY312_EXE% -m pip install --upgrade babylab

REM Step 3: Run the Flask app with Python 3.12.0
start "" cmd /k "%PY312_EXE% -m flask --app babylab.app run"

REM Optional: Wait a few seconds to allow the server to start
timeout /t 3 >nul

REM Step 4: Open Chrome at the specified URL
start chrome https://127.0.0.1:5000

endlocal