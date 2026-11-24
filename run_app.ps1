# Script de PowerShell para iniciar TrafficFlow AI
# Codificación UTF-8

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "         TRAFFICFLOW AI - SISTEMA DE OPTIMIZACIÓN DEL TRÁFICO                 " -ForegroundColor Green
Write-Host "         Carrera: Ingeniería Industrial | Cálculo Diferencial                 " -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si streamlit está disponible
try {
    Write-Host "[1/2] Iniciando servidor de Streamlit..." -ForegroundColor Yellow
    streamlit run app.py
}
catch {
    Write-Host ""
    Write-Host "[AVISO] No se pudo iniciar directamente con 'streamlit run'." -ForegroundColor Red
    Write-Host "Intentando con 'python -m streamlit run app.py'..." -ForegroundColor Yellow
    python -m streamlit run app.py
}
