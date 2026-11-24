@echo off
chcp 65001 > nul
echo ==============================================================================
echo          TRAFFICFLOW AI - SISTEMA DE OPTIMIZACIÓN DEL TRÁFICO
echo          Carrera: Ingeniería Industrial | Cálculo Diferencial
echo ==============================================================================
echo.
echo Verificando entorno de Python y Streamlit...

REM Intentar ejecutar con python
python -m streamlit run app.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [AVISO] Si Streamlit no inició directamente, verifique que las dependencias
    echo estén instaladas ejecutando en su terminal:
    echo     pip install -r requirements.txt
    echo.
    echo O bien verifique su instalación de Python.
    pause
)
