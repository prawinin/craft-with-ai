@echo off
REM ============================================================================
REM   Python for AI — Windows Starter Script
REM   Just double-click this file and the course will start automatically!
REM
REM   If this doesn't work, right-click > "Run as administrator"
REM ============================================================================

title Python for AI — Course Launcher
color 0B

echo.
echo   ╔═══════════════════════════════════════════════╗
echo   ║                                               ║
echo   ║     Python for AI — Course Launcher            ║
echo   ║                                               ║
echo   ╚═══════════════════════════════════════════════╝
echo.

REM ── Step 1: Check Python ──────────────────────────────────────────────────
echo [1/4] Checking for Python...

REM Try "python" first (Windows convention), then "python3"
set PYTHON_CMD=

where python >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    REM Verify it's Python 3 and not the Windows Store stub
    python -c "import sys; assert sys.version_info.major == 3" >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python
    )
)

if "%PYTHON_CMD%"=="" (
    where python3 >nul 2>nul
    if %ERRORLEVEL% EQU 0 (
        set PYTHON_CMD=python3
    )
)

if "%PYTHON_CMD%"=="" (
    echo.
    echo   ERROR: Python 3 is not installed or not in PATH!
    echo.
    echo   Please install Python:
    echo.
    echo   1. Go to https://www.python.org/downloads/
    echo   2. Download the latest Python 3 installer
    echo   3. IMPORTANT: Check "Add Python to PATH" during installation!
    echo   4. Click "Install Now"
    echo   5. After installation, run this script again
    echo.
    echo   If Python is already installed but this error persists,
    echo   you may need to add Python to your PATH manually:
    echo   - Search for "Environment Variables" in Windows Settings
    echo   - Under "Path", add the Python installation directory
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%V in ('%PYTHON_CMD% --version 2^>^&1') do set PY_VERSION=%%V
echo   ✓ Found %PYTHON_CMD% (%PY_VERSION%)

REM Check minimum version
%PYTHON_CMD% -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo   WARNING: Python 3.8 or higher is required. You have %PY_VERSION%.
    echo   Please update Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM ── Step 2: Set up virtual environment ────────────────────────────────────
echo [2/4] Setting up virtual environment...

set VENV_DIR=%~dp0.venv

if not exist "%VENV_DIR%" (
    echo   Creating virtual environment...
    %PYTHON_CMD% -m venv --system-site-packages "%VENV_DIR%"
    if %ERRORLEVEL% NEQ 0 (
        echo   ERROR: Failed to create virtual environment.
        echo   Try running: %PYTHON_CMD% -m pip install --user virtualenv
        pause
        exit /b 1
    )
    echo   ✓ Virtual environment created
) else (
    echo   ✓ Virtual environment exists
)

REM Activate venv
call "%VENV_DIR%\Scripts\activate.bat"

REM ── Step 3: Install dependencies ──────────────────────────────────────────
echo [3/4] Installing dependencies...

python -m pip install --upgrade pip -q >nul 2>nul

if exist "%~dp0requirements.txt" (
    pip install -r "%~dp0requirements.txt" -q >nul 2>nul
    echo   ✓ Dependencies installed
) else (
    pip install rich -q >nul 2>nul
    echo   ✓ Core dependencies installed
)

REM ── Step 4: Launch! ───────────────────────────────────────────────────────
echo [4/4] Launching Python for AI Course...
echo.
echo   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

python "%~dp0course_runner.py"

REM Deactivate venv on exit
call deactivate >nul 2>nul

echo.
echo   Course session ended. Press any key to close.
pause >nul
