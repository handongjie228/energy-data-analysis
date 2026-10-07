@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment not found. Running setup_env.bat ...
  call setup_env.bat nopause
)

echo [1/2] Environment check ...
".venv\Scripts\python.exe" check_env.py
if errorlevel 1 (
  echo.
  echo Environment check failed. Please fix the FAIL items above.
  if /I not "%~1"=="nopause" pause
  exit /b 1
)

echo.
echo [2/2] Running energy analysis ...
".venv\Scripts\python.exe" energy_analysis.py
if errorlevel 1 (
  echo.
  echo Analysis failed. Please copy the error message to Codex.
  if /I not "%~1"=="nopause" pause
  exit /b 1
)

echo.
echo All done. Outputs are in the output folder.
if /I not "%~1"=="nopause" pause
