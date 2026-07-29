@echo off
setlocal
cd /d "%~dp0"
title Atlas del tejido emprendedor de Boyaca

set "PYTHON_EXE=..\.venv\Scripts\python.exe"
if exist "%PYTHON_EXE%" goto python_ready

set "PYTHON_EXE=.venv\Scripts\python.exe"
if exist "%PYTHON_EXE%" goto python_ready

echo Preparando el entorno local por primera vez...
py -3 -m venv .venv
if errorlevel 1 goto error_python

:python_ready
"%PYTHON_EXE%" -c "import streamlit, plotly, pandas" >nul 2>&1
if errorlevel 1 (
    echo Instalando los componentes del tablero...
    "%PYTHON_EXE%" -m pip install --prefer-binary -r requirements.txt
    if errorlevel 1 goto error_dependencies
)

echo.
echo Iniciando el atlas en http://localhost:8501
echo Para cerrarlo, presione Ctrl+C en esta ventana.
start "" cmd /c "timeout /t 3 /nobreak >nul & start http://localhost:8501"
"%PYTHON_EXE%" -m streamlit run app.py --server.port 8501 --server.address localhost
goto end

:error_python
echo.
echo No fue posible encontrar Python ni crear el entorno local.
echo Instale Python 3.12 o ejecute este archivo desde el proyecto completo.
pause
goto end

:error_dependencies
echo.
echo No fue posible instalar las dependencias del tablero.
echo Revise su conexion a internet e intente nuevamente.
pause

:end
endlocal
