@echo off
setlocal
cd /d "%~dp0..\.."
echo =========================================================
echo   LAB7 - RIGOL DS1202Z-E - CAPTURA RAPIDA CH1 + CH2
echo =========================================================
echo Compruebe antes: Rigol en STOP tras SINGLE; CH1=J5, CH2=J7.
echo Se guardaran los CSV de ambos canales, sin imagen.
echo.
python -u ".\Herramientas_Comunes\Rigol_y_UART\rigol_ds1202ze.py" bundle --quick --only data --label lab7_datos --root ".\Laboratorio_7\04_Ensayos\Capturas_Rigol"
if errorlevel 1 (
  echo.
  echo ERROR: no se pudo completar la captura. Revise el mensaje anterior.
) else (
  echo.
  echo Captura terminada. Los CSV estan en 04_Ensayos\Capturas_Rigol.
)
echo.
pause
endlocal
