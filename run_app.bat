@echo off
echo.
echo ========================================
echo   Converter ^| Space by Dammytech
echo ========================================
echo.
echo Starting the application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found!
    echo Please make sure you're in the correct directory
    pause
    exit /b 1
)

REM Try to run the application
python main.py

REM If there's an error, show message
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo ERROR: Application failed to start
    echo ========================================
    echo.
    echo This might be due to missing dependencies.
    echo Run: python install_dependencies.py
    echo.
    echo Contact support: petersdamilare5@gmail.com
    echo Website: https://dammytech.netlify.app
    echo.
)

pause