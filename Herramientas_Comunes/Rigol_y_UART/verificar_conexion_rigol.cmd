@echo off
setlocal
cd /d "%~dp0.."

echo Verificando el RIGOL DS1202Z-E por USB-TMC...
echo.
python ".\Instrumentacion_RIGOL\rigol_ds1202ze.py" info

echo.
pause
endlocal
