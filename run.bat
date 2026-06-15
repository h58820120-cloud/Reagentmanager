@echo off
chcp 65001 >nul

setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        if exist "C:\Python312\python.exe" (
            set "PATH=C:\Python312;%PATH%"
        ) else if exist "C:\Python311\python.exe" (
            set "PATH=C:\Python311;%PATH%"
        ) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%PATH%"
        ) else (
            cls
            echo.
            echo Error: Python not found in PATH
            echo.
            echo Solution: Find Python installation folder
            echo Look for a folder like: C:\PythonXXX or C:\Users\YourName\AppData\Local\Programs\Python\PythonXXX
            echo.
            echo Then manually add to PATH. Open CMD as Administrator and run:
            echo setx PATH "C:\Your\Python\Path;%%PATH%%"
            echo.
            pause
            exit /b 1
        )
    )
)

cls
echo.
echo Starting Medical Reagent Management System v1.0.0
echo.

if not exist "venv" (
    echo Step 1: Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Complete: Virtual environment created
    echo.
)

call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Step 2: Installing dependencies...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Warning: Some dependencies may not have installed
    )
)
echo Complete: Dependencies ready
echo.

if not exist "reagent_system.db" (
    echo Step 3: Initializing database...
    python init_database.py --init
    if errorlevel 1 (
        echo Warning: Database initialization may have issues
    )
    echo Complete: Database initialized
    echo.
)

echo Step 4: Starting application...
echo.

python main.py
if errorlevel 1 (
    echo.
    echo Error: Application failed
    pause
    exit /b 1
)

pause
