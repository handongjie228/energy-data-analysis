@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found. Running setup_env.bat ...
  call setup_env.bat nopause
)

echo Running energy_all_in_one.py
".venv\Scripts\python.exe" energy_all_in_one.py

if errorlevel 1 (
  echo.
  echo Failed. Please copy the error message to Codex.
  if /I not "%~1"=="nopause" pause
  exit /b 1
)

if /I not "%~1"=="nopause" pause
