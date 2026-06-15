@echo off
REM Medical Laboratory Reagent Management System
REM Simple Windows Batch File

setlocal enabledelayedexpansion

REM Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    cls
    echo.
    echo ERROR: Python 3.12 not found
    echo.
    echo Please install Python 3.12 or higher
    echo Download from: https://www.python.org/downloads/
    echo.
    echo Important: Check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

cls
echo.
echo ========================================
echo Medical Laboratory Reagent Management
echo System v1.0.0
echo ========================================
echo.

REM Check virtual environment
if not exist "venv" (
    echo Step 1: Creating Python virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Complete: Virtual environment created
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check and install dependencies
echo Step 2: Checking and installing dependencies...
pip show PyQt6 >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Warning: Some dependencies may not have installed correctly
    )
)
echo Complete: Dependencies ready
echo.

REM Initialize database
if not exist "reagent_system.db" (
    echo Step 3: Initializing database...
    python init_database.py --init
    if errorlevel 1 (
        echo Warning: Database initialization may have issues
    )
    echo Complete: Database initialized
    echo.
)

REM Run application
echo Step 4: Starting application...
echo.
echo ========================================
echo Application is starting...
echo ========================================
echo.

python main.py
if errorlevel 1 (
    echo.
    echo ========================================
    echo Error: Application failed to start
    echo ========================================
    pause
    exit /b 1
)

pause
