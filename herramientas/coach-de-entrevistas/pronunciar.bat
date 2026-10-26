@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Pronunciador

set "PY="
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
if not defined PY (
  py -3 -c "import sys" >nul 2>nul && set "PY=py -3"
)
if not defined PY (
  python -c "import sys" >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo.
  echo  No encontre Python. Abri iniciar.bat una vez, o instala Python desde python.org.
  echo.
  pause
  exit /b 1
)
%PY% pronunciar.py %*
