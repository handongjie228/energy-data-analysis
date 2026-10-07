@echo off
chcp 65001 >nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

echo [1/3] Creating virtual environment ...
if not exist ".venv\Scripts\python.exe" (
  py -3.11 -m venv .venv
  if errorlevel 1 python -m venv .venv
)

echo [2/3] Upgrading pip ...
".venv\Scripts\python.exe" -m pip install --upgrade pip

echo [3/3] Installing pandas, numpy, matplotlib ...
".venv\Scripts\python.exe" -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
  echo Tsinghua mirror failed, retrying with official PyPI ...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)

echo.
echo Done. You can now run run_analysis.bat
if /I not "%~1"=="nopause" pause
