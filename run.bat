@echo off
REM Quick Start Script for Text-to-SQL Pipeline
REM This script sets up and runs the pipeline

setlocal enabledelayedexpansion

cd /d "%~dp0"

echo.
echo ========================================
echo Text-to-SQL Pipeline - Quick Start
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo OK - Python found

REM Create virtual environment
echo [2/5] Setting up virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Created new virtual environment
) else (
    echo Virtual environment exists
)

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [4/5] Installing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo Error installing requirements
    pause
    exit /b 1
)
echo Dependencies installed

REM Create .env if not exists
echo [5/5] Checking configuration...
if not exist ".env" (
    copy .env.example .env
    echo Created .env file - please edit with your credentials
)
echo Configuration ready

echo.
echo ========================================
echo Setup Completed!
echo ========================================
echo.
echo Available options:
echo   1. Run Web UI (Streamlit)
echo   2. Run CLI (Interactive)
echo   3. Run Tests
echo   4. Exit
echo.

:menu
set /p choice="Choose option: "

if "%choice%"=="1" (
    echo Starting Streamlit...
    streamlit run app.py
    goto menu
) else if "%choice%"=="2" (
    echo Starting CLI...
    python cli.py --interactive
    goto menu
) else if "%choice%"=="3" (
    echo Running tests...
    python test_pipeline.py
    pause
    goto menu
) else if "%choice%"=="4" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid option
    goto menu
)
