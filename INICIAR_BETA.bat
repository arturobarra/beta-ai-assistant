@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=python"
where py >nul 2>nul && set "PYTHON=py -3"

echo ==============================================================
echo INICIANDO BETA v3.7.5 ESTABLE
echo Carpeta: %CD%
echo ==============================================================

%PYTHON% "beta.py"
set "RC=%ERRORLEVEL%"

echo.
if not "%RC%"=="0" (
    echo [ERROR] Beta v3.7.5 estable termino con codigo %RC%.
) else (
    echo Beta v3.7.5 estable finalizo correctamente.
)

echo.
pause
exit /b %RC%




