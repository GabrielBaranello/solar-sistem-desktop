@echo off

REM Ir a la carpeta donde está este .bat
cd /d "%~dp0"

REM Verificar que el entorno virtual exista
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: No se encontro el entorno virtual.
    echo Ejecuta: python -m venv venv
    pause
    exit /b
)
echo El codigo de python esta iniciado...
echo presione Ctrl+C para detenerlo.
REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Ejecutar el script
python main.py

REM Pausa para ver errores
pause
