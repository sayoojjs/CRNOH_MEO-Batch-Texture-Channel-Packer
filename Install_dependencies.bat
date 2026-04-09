@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [MSG] Python not found. Downloading installer...
    curl -o python_installer.exe https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
    echo [MSG] Installing Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1
    del python_installer.exe
    echo [MSG] Python installed. Restarting script...
    timeout /t 3 >nul
    call "%~f0"
    exit
) else (
    echo [MSG] Python found. Skipping install.
)

echo [MSG] Installing dependencies...
pip install -r requirements.txt

pause
