@echo off
chcp 65001 >nul
echo ================================================
echo  PostgreSQL Setup for Reagent Management System
echo ================================================
echo.

REM Check if psql is available
psql --version >nul 2>&1
if errorlevel 1 (
    echo PostgreSQL not found. Please download from:
    echo https://www.postgresql.org/download/windows/
    echo.
    echo Recommended version: PostgreSQL 16
    echo During installation:
    echo   - Port: 5432 (default)
    echo   - Remember the password you set for 'postgres'
    echo.
    pause
    exit /b 1
)

echo PostgreSQL found. Setting up database...
echo.

REM Create database and user
psql -U postgres -c "CREATE USER reagent_user WITH PASSWORD 'Reagent@2024';" 2>nul
psql -U postgres -c "CREATE DATABASE reagent_db OWNER reagent_user ENCODING 'UTF8';" 2>nul
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE reagent_db TO reagent_user;" 2>nul

echo.
echo Database setup complete!
echo.
echo Connection settings:
echo   Host:     localhost (or this computer's IP)
echo   Port:     5432
echo   Database: reagent_db
echo   User:     reagent_user
echo   Password: Reagent@2024
echo.
echo Now update db_config.py:
echo   DB_MODE = 'postgresql'
echo   PG_HOST = '(this computer IP)'
echo   PG_PASSWORD = 'Reagent@2024'
echo.

REM Install psycopg2
echo Installing Python PostgreSQL driver...
pip install psycopg2-binary

echo.
echo Done! Run: python main.py
echo.
pause
