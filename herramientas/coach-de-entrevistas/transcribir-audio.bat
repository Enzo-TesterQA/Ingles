@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Coach de entrevistas - transcribir audio

if not exist ".venv\instalado.txt" (
  echo.
  echo  Primero abri iniciar.bat una vez para instalar todo.
  echo.
  pause
  exit /b 1
)
if "%~1"=="" (
  echo.
  echo  Arrastra una nota de voz o un audio (ogg, opus, m4a, mp3, wav^) sobre este archivo.
  echo.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" coach.py --archivo "%~1"
echo.
pause
