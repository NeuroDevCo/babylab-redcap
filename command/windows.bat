@echo off
setlocal

REM === Step 1: Ensure Python 3.12.0 is installed ===
set PY312_PATH=C:\Program Files\Python312
set PY312_EXE="%PY312_PATH%\python.exe"

IF NOT EXIST %PY312_EXE% (
    echo Python 3.12.0 not found. Installing...
    set PYTHON_INSTALLER=python-3.12.0-amd64.exe
    if not exist "%PYTHON_INSTALLER%" (
        curl -LO https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
    )
    python-3.12.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
)

IF NOT EXIST "%USERPROFILE%/babylab-redcap" mkdir "%USERPROFILE%/babylab-redcap"
cd "%USERPROFILE%/babylab-redcap"
IF NOT EXIST "pyproject.toml" uv init
uv python install 3.12.0
uv add babylab
start chrome http://127.0.0.1:5000
uv run flask --app babylab.app run

