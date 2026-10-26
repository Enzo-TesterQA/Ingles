@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Coach de entrevistas

if exist ".venv\instalado.txt" goto run

set "PY="
for %%V in (3.12 3.11 3.13 3.14 3.10) do (
  if not defined PY (
    py -%%V -c "import sys" >nul 2>nul && set "PY=py -%%V"
  )
)
if not defined PY (
  python -c "import sys; assert (3, 10) <= sys.version_info[:2] <= (3, 13)" >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo.
  echo  No encontre Python 3.10 a 3.13 en esta PC.
  echo  Instala Python 3.12 desde https://www.python.org/downloads/
  echo  y en el instalador marca la opcion "Add python.exe to PATH".
  echo  Despues volve a abrir este archivo.
  echo.
  pause
  exit /b 1
)

echo.
echo  Primera vez: preparo todo lo necesario. Tarda unos minutos y no se repite.
echo.
%PY% -m venv .venv
if errorlevel 1 goto fail
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto fail
echo ok> ".venv\instalado.txt"

:run
".venv\Scripts\python.exe" coach.py %*
echo.
pause
exit /b 0

:fail
echo.
echo  Algo fallo en la instalacion. Revisa tu conexion a internet y volve a intentar.
echo  Si se repite, borra la carpeta .venv y abri este archivo de nuevo.
echo.
pause
exit /b 1
