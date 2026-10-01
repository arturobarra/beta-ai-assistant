@echo off
chcp 65001 >nul
set "PY=%LocalAppData%\Programs\Python\Python312\python.exe"
if not exist "%PY%" set "PY=python"
echo Instalando dependencias visuales de Beta...
"%PY%" -m pip install --upgrade pygame PySide6 numpy
if errorlevel 1 (
  echo.
  echo Hubo un problema durante la instalacion.
  pause
  exit /b 1
)
echo.
echo Dependencias instaladas correctamente.
pause
