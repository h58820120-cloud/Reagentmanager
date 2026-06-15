@echo off
chcp 65001 >nul
echo Building complete standalone package...
echo.

call venv\Scripts\activate.bat

echo Step 1: Creating database...
python init_database.py --init
echo.

pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Step 2: Installing PyInstaller...
    pip install pyinstaller
)

if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

echo Step 3: Building executable...
pyinstaller --onefile --windowed --name ReagentSystem ^
    --add-data "reagent_system.db;." ^
    --hidden-import=PyQt6 ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=PyQt6.QtChart ^
    --hidden-import=sqlalchemy ^
    --hidden-import=sqlalchemy.orm ^
    --collect-all PyQt6 ^
    --collect-all sqlalchemy ^
    main.py

if errorlevel 1 (
    echo Error: Build failed
    pause
    exit /b 1
)

echo.
echo Complete! Executable: dist\ReagentSystem.exe
echo.
pause
