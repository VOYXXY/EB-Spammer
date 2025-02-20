@echo off
cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Python not installed , please install via https://www.python.org/downloads/
    pause
    exit /b
)

if exist "local_version.txt" (
    echo local_version.txt found [✔]
) else (
    echo [!] local_version.txt was not found. This file is important for our automatic update function.
    set /p download_version="Do you want to install a clean version of https://github.com/VOYXXY/EB-Spammer (y/n): "
    
    if /i "%download_version%"=="y" (
        echo [!] Downloading...
        
        REM Check if git is installed
        where git >nul 2>nul
        if %errorlevel% neq 0 (
            echo [!] Git is not installed. Please install Git and try again.
            pause
            exit /b
        )

        git clone https://github.com/VOYXXY/EB-Spammer.git
        if exist "EB-Spammer" (
            echo [!] Download complete.
        ) else (
            echo [!] Error while downloading, check your internet connection and try again.
            pause
            exit /b
        )
    ) else (
        echo [!] Continuing without important file.
    )
)

echo Installing requirements...
if exist "requirements.txt" (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    echo [!] requirements.txt not found.
    pause
    exit /b
)

title EB-Spammer
echo Starting main.py...
python main.py

echo.
pause
