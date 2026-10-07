@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found. Running setup_env.bat ...
  call setup_env.bat nopause
)

echo Running energy_analysis.py ...
".venv\Scripts\python.exe" energy_analysis.py

if errorlevel 1 (
  echo.
  echo Something went wrong. Please copy the error message to Codex.
  pause
)
