@echo off
setlocal
cd /d "%~dp0.."

echo ======================================================
echo   Captura de ensayo - RIGOL DS1202Z-E
echo ======================================================
echo.
echo Antes de continuar:
echo   1. Configure las sondas y el disparo en el osciloscopio.
echo   2. Detenga la adquisicion si desea conservar un evento unico.
echo   3. Cierre Ultra Sigma y UltraScope.
echo.
set /p "RIGOL_LABEL=Nombre breve del ensayo: "
if not defined RIGOL_LABEL set "RIGOL_LABEL=ensayo"

echo.
echo Adquiriendo pantalla, CH1, CH2 y metadatos...
python ".\Instrumentacion_RIGOL\rigol_ds1202ze.py" bundle --label "%RIGOL_LABEL%"

if errorlevel 1 (
    echo.
    echo ERROR: no se completo la captura.
    echo Compruebe que el osciloscopio este encendido, conectado por USB
    echo y que Ultra Sigma o UltraScope no esten usando el equipo.
) else (
    echo.
    echo Captura terminada correctamente.
    echo Los archivos se guardaron en la carpeta capturas_rigol.
)

echo.
pause
endlocal
