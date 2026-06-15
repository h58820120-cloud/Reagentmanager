@echo off
chcp 65001 >nul
echo Building standalone executable...
echo This may take 5 minutes first time...
echo.

REM Activate venv
call venv\Scripts\activate.bat

REM Install PyInstaller if needed
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Remove old build
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "ReagentSystem.spec" del ReagentSystem.spec

REM Build executable with all dependencies
pyinstaller --onefile --windowed --name "ReagentSystem" ^
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
echo Success! Executable created at: dist\ReagentSystem.exe
echo.
pause
