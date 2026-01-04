@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM =========================
REM Obtener ruta actual
REM =========================
set BASEDIR=%~dp0
set BASEDIR=%BASEDIR:~0,-1%

REM =========================
REM Ruta del VBS
REM =========================
set VBS=%BASEDIR%\launcher.vbs

REM =========================
REM Crear el VBS
REM =========================
(
echo Set WshShell = CreateObject("WScript.Shell"^)
echo WshShell.Run """%BASEDIR%\run.bat""", 0, False
) > "%VBS%"

REM =========================
REM Crear run.bat (el real)
REM =========================
(
echo @echo off
echo cd /d "%BASEDIR%"
echo "%~dp0.venv\Scripts\pythonw.exe" "%~dp0main.py"
) > "%BASEDIR%\run.bat"

REM =========================
REM Crear tarea programada
REM =========================
schtasks /create ^
    /tn "SolarSystemDesktop" ^
    /tr "wscript.exe \"%VBS%\"" ^
    /sc onlogon ^
    /rl limited ^
    /f

echo.
echo ✔ Instalado correctamente
pause
