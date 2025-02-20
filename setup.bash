#!/bin/bash

if ! command -v python3 &> /dev/null
then
    echo "[!] Python is not installed. please install via https://www.python.org/downloads/"
    exit 1
fi

cd "$(dirname "$0")"

if [ -f "local_version.txt" ]; then
    echo "local_version.txt found [✔]"
else
    echo "[!] local_version.txt was not found. This file is important for our automatic update function."
    read -p "Do you want to install a clean version of https://github.com/VOYXXY/EB-Spammer (y/n): " download_version
    
    if [ "$download_version" == "y" ]; then
        echo "[!] Downloading..."
        
        if ! command -v git &> /dev/null
        then
            echo "[!] Git is not installed. Please install Git and try again."
            exit 1
        fi

        git clone https://github.com/VOYXXY/EB-Spammer.git
        if [ -d "EB-Spammer" ]; then
            echo "[!] Download complete."
        else
            echo "[!] Error while downloading, check your internet connection and try again."
            exit 1
        fi
    else
        echo "[!] Continuing without important file."
    fi
fi

echo "Installing requirements..."
if [ -f "requirements.txt" ]; then
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
else
    echo "[!] requirements.txt not found."
    exit 1
fi

echo "Starting main.py..."
python3 main.py
