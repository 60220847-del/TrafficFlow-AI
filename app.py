"""
APLICACIÓN PRINCIPAL: TRAFFICFLOW AI
====================================
Sistema Inteligente de Simulación y Optimización del Tráfico Vehicular
Carrera: Ingeniería Industrial | Asignatura: Cálculo Diferencial

Autor: Proyecto Universitario de Ingeniería Industrial
Tecnologías: Python, Streamlit, Plotly, NumPy, SciPy, Scikit-learn, OpenCV
"""

import sys
import time
import os
import math
import numpy as np
import streamlit as st

# Configuración de página de Streamlit
st.set_page_config(
    page_title="TrafficFlow AI - Optimización del Tráfico",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Importación de módulos del proyecto
from simulacion import SimuladorInterseccion, ConfiguracionSemaforo, FaseSemaforo
from optimizacion import (
    optimizar_tiempos_semaforo,
    generar_datos_curvas,
    obtener_demostracion_paso_a_paso,
    funcion_objetivo
)
from inteligencia_artificial import ModeloRecomendadorTraficoIA, GeneradorDatosSinteticosTrafico
from comparacion import ejecutar_comparativa_escenarios
from deteccion_vehiculos import DetectorVehiculosOpenCV, obtener_instrucciones_modelos_avanzados, OPENCV_DISPONIBLE
from graficos import (
    generar_vista_interseccion,
    generar_grafico_dinamica_colas,
    generar_grafico_tasas_flujo,
    generar_grafico_optimizacion_calculo,
    generar_grafico_importancia_variables,
    generar_grafico_comparativo_barras,
    generar_grafico_radar_desempeno
)
from teoria import obtener_secciones_teoricas, obtener_referencias_apa7
from simulador_visual import generar_componente_simulador_html
from dashboard_intelligence import renderizar_traffic_intelligence_center


# ==============================================================================
# ESTILOS VISUALES PERSONALIZADOS (TEMA OSCURO PROFESIONAL VIAL)
# ==============================================================================
st.markdown("""
<style>
    /* Estructura general tema oscuro */
    .stApp {
        background-color: #0b1017;
        color: #e6edf3;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    }
    
    /* Encabezado principal */
    .titulo-principal {
        font-size: 2.1rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00E676 0%, #00E5FF 50%, #FFD600 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitulo-principal {
        font-size: 1.0rem;
        color: #8b949e;
        margin-bottom: 1.2rem;
    }
    
    /* Tarjetas de indicadores (KPIs) */
    .kpi-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .kpi-titulo {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: #8b949e;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .kpi-valor {
        font-size: 1.7rem;
        font-weight: 700;
        color: #f0f6fc;
        margin: 4px 0;
    }
    .kpi-sub {
        font-size: 0.8rem;
        color: #00E5FF;
    }
    
    /* Semáforo visual en tarjeta */
    .semaforo-box {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
    }
    .sem-verde { background-color: rgba(0, 230, 118, 0.15); color: #00E676; border: 1px solid #00E676; }
    .sem-amarillo { background-color: rgba(255, 214, 0, 0.15); color: #FFD600; border: 1px solid #FFD600; }
    .sem-rojo { background-color: rgba(255, 23, 68, 0.15); color: #FF1744; border: 1px solid #FF1744; }
    
    /* Cajas didácticas de fórmula */
    .formula-box {
        background-color: #121820;
        border-left: 4px solid #00E5FF;
        padding: 12px 18px;
        border-radius: 4px;
        margin: 12px 0;
    }
    
    /* Cajas de advertencia metodológica */
    .disclaimer-box {
        background-color: rgba(255, 214, 0, 0.08);
        border: 1px solid rgba(255, 214, 0, 0.3);
        border-left: 4px solid #FFD600;
        padding: 12px 16px;
        border-radius: 4px;
        margin: 14px 0;
        color: #e6edf3;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# INICIALIZACIÓN DE VARIABLES DE ESTADO (SESSION_STATE)
# ==============================================================================
if "simulador" not in st.session_state:
    st.session_state.simulador = SimuladorInterseccion(
        config_semaforo=ConfiguracionSemaforo(
            tiempo_verde_1=30.0,
            tiempo_verde_2=30.0,
            tiempo_amarillo_1=3.0,
            tiempo_amarillo_2=3.0,
            tiempo_todo_rojo=1.0
        ),
        tasa_llegada_1=20.0,
        tasa_llegada_2=14.0,
        cola_inicial_1=6,
        cola_inicial_2=4,
        es_estocastico=True,
        semilla=42
    )

if "modelo_ia" not in st.session_state:
    st.session_state.modelo_ia = ModeloRecomendadorTraficoIA(tipo_modelo="RandomForest")

if "simulando_activo" not in st.session_state:
    st.session_state.simulando_activo = False


# ==============================================================================
# BARRA LATERAL (SIDEBAR DE NAVEGACIÓN Y PARÁMETROS GLOBALES)
# ==============================================================================
with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/google/material-design-icons/master/png/maps/traffic/materialicons/48dp/2x/baseline_traffic_white_48dp.png",
        width=48
    )
    st.markdown("### **TrafficFlow AI**")
    st.caption("Ingeniería Industrial | Cálculo Diferencial")
    st.divider()

    menu_seleccionado = st.radio(
        "**Navegación del Sistema:**",
        [
            "🚦 Simulación Interactiva",
            "🎛️ Traffic Intelligence Center",
            "📐 Modelo Matemático y Colas",
            "🧮 Cálculo Diferencial y Optimización",
            "🤖 Inteligencia Artificial (ML)",
            "📹 Detección de Vehículos (OpenCV)",
            "📊 Comparación de Escenarios",
            "📚 Fundamentación Teórica y APA 7"
        ],
        index=0
    )

    st.divider()
    st.markdown("##### ⚙️ Parámetros de la Intersección")
    
    # Parámetros editables en la barra lateral
    param_lambda1 = st.slider(
        "Tasa Llegada Vía 1 (λ₁ veh/min)",
        min_value=4.0, max_value=45.0, value=22.0, step=1.0,
        help="Cantidad esperada de vehículos que llegan por minuto a la Vía 1 (Norte-Sur)."
    )
    param_lambda2 = st.slider(
        "Tasa Llegada Vía 2 (λ₂ veh/min)",
        min_value=4.0, max_value=45.0, value=14.0, step=1.0,
        help="Cantidad esperada de vehículos que llegan por minuto a la Vía 2 (Este-Oeste)."
    )
    
    param_ciclo_C = st.slider(
        "Ciclo de Verde Combinado C (seg)",
        min_value=30.0, max_value=120.0, value=60.0, step=5.0,
        help="Tiempo total disponible de luz verde a distribuir entre ambas vías (C = g₁ + g₂)."
    )

    st.divider()
    st.caption("Versión 1.0.0 | Universidad | 100% en Español")


# ==============================================================================
# SECCIÓN 1: SIMULACIÓN INTERACTIVA VISUAL
# ==============================================================================
if menu_seleccionado == "🚦 Simulación Interactiva":
    st.markdown('<div class="titulo-principal">Centro de Control Inteligente de Tráfico | Ciudad Isométrica 2.5D</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Monitoreo en tiempo real a 60 FPS en entorno de ciudad inteligente isométrica 3D: vehículos detallados con faros y luces de freno reactivas, '
        'semáforos verticales con viseras, efecto bloom resplandeciente, temporizadores LED con cuenta regresiva, y arquitectura urbana dinámica.'
        '</div>',
        unsafe_allow_html=True
    )

    # 1. Cálculo dinámico de tiempos óptimos para conectar con la simulación
    res_opt_calc_live = optimizar_tiempos_semaforo(
        A=param_lambda1, B=param_lambda2, C=param_ciclo_C,
        g_min=10.0, h_min=10.0
    )
    g_calculo_actual = res_opt_calc_live["g_optimo"]

    # Recomendación en vivo de la Inteligencia Artificial (Scikit-Learn)
    try:
        pred_ia_live = st.session_state.modelo_ia.predecir_tiempos_optimos(
            cola_v1=float(st.session_state.simulador.cola_1),
            cola_v2=float(st.session_state.simulador.cola_2),
            lambda_v1=param_lambda1,
            lambda_v2=param_lambda2,
            espera_v1=12.0, espera_v2=10.0,
            flujo_sat_1=36.0, flujo_sat_2=36.0,
            ciclo_total_C=param_ciclo_C,
            g_min=10.0, h_min=10.0
        )
        g_ia_actual = pred_ia_live["g1_recomendado"]
    except Exception:
        g_ia_actual = g_calculo_actual

    # 2. Renderizado del Simulador Visual Realista (Canvas Interactivo a 60 FPS)
    simulador_html = generar_componente_simulador_html(
        tiempo_verde_1=st.session_state.simulador.config.tiempo_verde_1,
        tiempo_verde_2=st.session_state.simulador.config.tiempo_verde_2,
        tiempo_amarillo=3.0,
        tiempo_todo_rojo=1.0,
        lambda_1=param_lambda1,
        lambda_2=param_lambda2,
        g_calculo=g_calculo_actual,
        g_ia=g_ia_actual,
        ciclo_C=param_ciclo_C,
        modo_inicial="calculo"
    )
    st.components.v1.html(simulador_html, height=730, scrolling=False)

    st.markdown("#### 🎛️ Consola de Control Discreto y Telemetría Científica")

    # Fila de Controles de Ejecución Manual
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4, col_ctrl5 = st.columns([1.2, 1.2, 1.2, 2, 2])
    with col_ctrl1:
        if st.button("▶️ Avanzar Paso (5s)", use_container_width=True):
            st.session_state.simulador.avanzar_paso(dt=5.0)
    with col_ctrl2:
        if st.button("⏩ Ciclo Completo", use_container_width=True):
            duracion_ciclo = st.session_state.simulador.config.ciclo_total
            st.session_state.simulador.simular_horizonte(duracion_total_segundos=duracion_ciclo, dt=1.0)
    with col_ctrl3:
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.simulador.reiniciar()
            st.success("Simulación reiniciada a t=0s.")
    with col_ctrl4:
        tiempo_verde_1_manual = st.number_input(
            "Verde Vía 1 Manual (g₁ s)", min_value=10.0, max_value=param_ciclo_C - 10.0,
            value=float(st.session_state.simulador.config.tiempo_verde_1), step=2.0
        )
    with col_ctrl5:
        tiempo_verde_2_manual = param_ciclo_C - tiempo_verde_1_manual
        st.metric("Verde Vía 2 Manual (g₂ s)", f"{tiempo_verde_2_manual:.1f} s", delta=f"{tiempo_verde_2_manual - tiempo_verde_1_manual:+.1f}s dif")

    # Actualizar configuración del semáforo en simulación
    st.session_state.simulador.config.tiempo_verde_1 = tiempo_verde_1_manual
    st.session_state.simulador.config.tiempo_verde_2 = tiempo_verde_2_manual
    st.session_state.simulador.lambda_1 = param_lambda1 / 60.0
    st.session_state.simulador.lambda_2 = param_lambda2 / 60.0

    # Obtener estado visual actual
    estado_vis = st.session_state.simulador.obtener_estado_visual()
    metricas_actuales = st.session_state.simulador.obtener_resumen_metricas()

    # Tarjetas de Indicadores en Tiempo Real
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Tiempo Simulado</div>
            <div class="kpi-valor">{estado_vis['tiempo_actual']:.1f} s</div>
            <div class="kpi-sub">Fase: {estado_vis['fase_actual']}</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi2:
        badge_luz1 = "sem-verde" if estado_vis["luz_1"] == "VERDE" else ("sem-amarillo" if estado_vis["luz_1"] == "AMARILLO" else "sem-rojo")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Semáforo Vía 1 (N-S)</div>
            <div class="kpi-valor"><span class="semaforo-box {badge_luz1}">{estado_vis['luz_1']}</span></div>
            <div class="kpi-sub">Resta: {estado_vis['tiempo_restante_fase']:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi3:
        badge_luz2 = "sem-verde" if estado_vis["luz_2"] == "VERDE" else ("sem-amarillo" if estado_vis["luz_2"] == "AMARILLO" else "sem-rojo")
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Semáforo Vía 2 (E-O)</div>
            <div class="kpi-valor"><span class="semaforo-box {badge_luz2}">{estado_vis['luz_2']}</span></div>
            <div class="kpi-sub">Resta: {estado_vis['tiempo_restante_fase']:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Colas en Espera</div>
            <div class="kpi-valor">{int(estado_vis['cola_1'])} | {int(estado_vis['cola_2'])}</div>
            <div class="kpi-sub">Vía 1: {estado_vis['cola_1']:.1f} | Vía 2: {estado_vis['cola_2']:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    with kpi5:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Total Atendidos</div>
            <div class="kpi-valor">{metricas_actuales['total_atendidos']} veh</div>
            <div class="kpi-sub">Espera media: {metricas_actuales['espera_promedio_global']:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)

    # Vista Esquemática Vectorial de la Intersección (Plotly Detallado con autos realistas)
    with st.expander("🗺️ Ver Mapa Vectorial Detallado de la Intersección (Plotly)", expanded=False):
        fig_interseccion = generar_vista_interseccion(estado_vis)
        st.plotly_chart(fig_interseccion, use_container_width=True)

    # Gráfico de Evolución de Colas
    st.markdown("#### 📈 Evolución Dinámica de Colas y Ecuación Diferencial Q'(t)")
    fig_colas = generar_grafico_dinamica_colas(st.session_state.simulador.historial)
    st.plotly_chart(fig_colas, use_container_width=True)


# ==============================================================================
# SECCIÓN: TRAFFIC INTELLIGENCE CENTER (DASHBOARD EJECUTIVO DE CONTROL)
# ==============================================================================
elif menu_seleccionado == "🎛️ Traffic Intelligence Center":
    renderizar_traffic_intelligence_center(
        simulador=st.session_state.simulador,
        modelo_ia=st.session_state.modelo_ia,
        param_lambda1=param_lambda1,
        param_lambda2=param_lambda2,
        param_ciclo_C=param_ciclo_C
    )


# ==============================================================================
# SECCIÓN 2: MODELO MATEMÁTICO DEL TRÁFICO Y DINÁMICA DE COLAS
# ==============================================================================
elif menu_seleccionado == "📐 Modelo Matemático y Colas":
    st.markdown('<div class="titulo-principal">Modelo Matemático del Tráfico Vehicular</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Formulación mediante la Ecuación Diferencial de Conservación de Flujo y Teoría de Colas.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info("📌 **Ecuación Diferencial Fundamental del Flujo de Colas:**")
    st.latex(r"\frac{dQ}{dt} = Q'(t) = \lambda(t) - \mu(t), \quad \text{sujeto a } Q(t) \ge 0")

    col_m1, col_m2 = st.columns([1, 1])
    with col_m1:
        st.markdown("#### Definición de Variables y Parámetros")
        st.markdown("""
        - **$Q(t)$ [vehículos]:** Cantidad instantánea de vehículos en cola en el acceso en el tiempo $t$.
        - **$\\lambda(t)$ [veh/s o veh/min]:** Tasa de llegada vehicular al acceso.
        - **$\\mu(t)$ [veh/s o veh/min]:** Tasa instantánea de salida (capacidad de atención del semáforo).
        - **$S$ [veh/s]:** Flujo de saturación máximo durante la fase de luz verde.
        - **$\\beta$ [adimensional]:** Factor de vaciado durante el intervalo amarillo (típicamente $\\approx 0.35$).
        - **$W_q$ [segundos]:** Tiempo promedio de espera en cola por vehículo (según la Ley de Little: $L_q = \\lambda W_q$).
        """)
    with col_m2:
        st.markdown("#### Supuestos y Condiciones de Frontera")
        st.markdown("""
        1. **Condición de No Negatividad:** La cantidad de vehículos no puede ser negativa:
           $$\\text{Si } Q(t) = 0 \\text{ y } \\lambda(t) < \\mu(t) \\implies Q'(t) = 0$$
        2. **Dependencia del Estado del Semáforo:**
           - **Luz Verde ($g$):** $\\mu(t) = S$.
           - **Luz Amarilla ($y$):** $\\mu(t) = \\beta \\cdot S$.
           - **Luz Roja ($r$):** $\\mu(t) = 0$. Durante la fase roja, la cola crece a una tasa constante $Q'(t) = \\lambda(t)$.
        3. **Aproximación Continua de Fluidos:** Permite modelar el flujo discreto de vehículos como un volumen continuo diferenciable para aplicar cálculo diferencial.
        """)

    st.divider()
    st.markdown("#### Comparación de Tasas de Llegada (λ) vs Tasas de Salida Semafórica (μ)")
    fig_tasas = generar_grafico_tasas_flujo(st.session_state.simulador.historial)
    st.plotly_chart(fig_tasas, use_container_width=True)


# ==============================================================================
# SECCIÓN 3: CÁLCULO DIFERENCIAL Y OPTIMIZACIÓN MATEMÁTICA
# ==============================================================================
elif menu_seleccionado == "🧮 Cálculo Diferencial y Optimización":
    st.markdown('<div class="titulo-principal">Cálculo Diferencial y Optimización de Semáforos</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Deducción analítica rigurosa, condición de primer orden, concavidad por segunda derivada y evaluación de restricciones.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="disclaimer-box">
        <strong>⚠️ AVISO METODOLÓGICO Y PEDAGÓGICO:</strong><br>
        La función $E(g) = \\frac{A}{g} + \\frac{B}{C - g}$ implementada en esta sección constituye un <strong>modelo didáctico</strong>
        diseñado para demostrar de forma analítica y rigurosa la aplicación de las derivadas, puntos críticos, criterios de convexidad
        y optimización con restricciones en el curso de Cálculo Diferencial. <em>No debe presentarse como una fórmula empírica universal
        de ingeniería de tránsito ni confundirse con una medición real del retraso vehicular</em>.
    </div>
    """, unsafe_allow_html=True)

    # Parámetros del modelo interactivo
    col_p1, col_p2, col_p3, col_p4 = st.columns(4)
    with col_p1:
        param_A = st.number_input("Parámetro A (Demanda Vía 1)", min_value=1.0, max_value=200.0, value=float(param_lambda1), step=1.0)
    with col_p2:
        param_B = st.number_input("Parámetro B (Demanda Vía 2)", min_value=1.0, max_value=200.0, value=float(param_lambda2), step=1.0)
    with col_p3:
        param_C_opt = st.number_input("Ciclo Total C (s)", min_value=30.0, max_value=150.0, value=float(param_ciclo_C), step=5.0)
    with col_p4:
        g_min_normativo = st.number_input("Verde Mínimo g_min (s)", min_value=5.0, max_value=30.0, value=10.0, step=1.0)

    # Ejecutar optimización
    h_min_normativo = g_min_normativo
    resultado_opt = optimizar_tiempos_semaforo(
        A=param_A, B=param_B, C=param_C_opt,
        g_min=g_min_normativo, h_min=h_min_normativo
    )
    datos_curvas = generar_datos_curvas(A=param_A, B=param_B, C=param_C_opt)

    # Tarjetas de Resultados Matemáticos
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Punto Crítico Teórico (g*)</div>
            <div class="kpi-valor" style="color: #00E5FF;">{resultado_opt['g_teorico']:.2f} s</div>
            <div class="kpi-sub">Fórmula: C√A / (√A + √B)</div>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Verde Óptimo Factible (g₁)</div>
            <div class="kpi-valor" style="color: #00E676;">{resultado_opt['g_optimo']:.2f} s</div>
            <div class="kpi-sub">Estado: {resultado_opt['estado_restriccion']}</div>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Verde Óptimo Vía 2 (g₂)</div>
            <div class="kpi-valor" style="color: #FFD600;">{resultado_opt['g2_optimo']:.2f} s</div>
            <div class="kpi-sub">C - g₁ = {param_C_opt:.0f} - {resultado_opt['g_optimo']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    with r4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-titulo">Valor Mínimo E(g*)</div>
            <div class="kpi-valor" style="color: #D500F9;">{resultado_opt['E_optimo']:.2f}</div>
            <div class="kpi-sub">Segunda derivada: {resultado_opt['E_segunda_opt']:.4f} > 0</div>
        </div>
        """, unsafe_allow_html=True)

    # Gráficas de E(g), E'(g) y E''(g)
    fig_opt = generar_grafico_optimizacion_calculo(datos_curvas, resultado_opt)
    st.plotly_chart(fig_opt, use_container_width=True)

    # Demostración Paso a Paso para la Exposición
    st.markdown("### 🎓 Demostración Matemática Formal Paso a Paso")
    st.caption("Deducción analítica detallada de la optimización mediante cálculo diferencial para la defensa oral ante el docente.")
    pasos = obtener_demostracion_paso_a_paso(param_A, param_B, param_C_opt)
    tab_titulos = [f"Paso {i+1}" for i in range(len(pasos))]
    tabs_demostracion = st.tabs(tab_titulos)
    for idx, p in enumerate(pasos):
        with tabs_demostracion[idx]:
            st.markdown(f"#### {p['titulo']}")
            st.write(p['descripcion'])
            st.latex(p['latex'])

    st.info(f"**Análisis de Restricciones Operativas:** {resultado_opt['motivo_restriccion']}")


# ==============================================================================
# SECCIÓN 4: INTELIGENCIA ARTIFICIAL (MACHINE LEARNING CON SCIKIT-LEARN)
# ==============================================================================
elif menu_seleccionado == "🤖 Inteligencia Artificial (ML)":
    st.markdown('<div class="titulo-principal">Inteligencia Artificial y Aprendizaje Automático</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Modelo predictivo real entrenado con Scikit-learn (Random Forest Regressor) para control adaptativo de semáforos.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="disclaimer-box">
        <strong>NOTA METODOLÓGICA SOBRE LOS DATOS DE ENTRENAMIENTO:</strong><br>
        Los datos de entrenamiento son <strong>100% sintéticos y controlados</strong>, generados a partir de miles de micro-simulaciones
        matemáticas de colas continuas que combinan distintas densidades de tráfico, horas valle y horas pico.
    </div>
    """, unsafe_allow_html=True)

    tab_ia1, tab_ia2, tab_ia3 = st.tabs(["🚀 Entrenamiento y Métricas", "📊 Explorador de Datos Sintéticos", "🔮 Recomendador en Vivo"])

    with tab_ia1:
        col_t1, col_t2 = st.columns([1, 2])
        with col_t1:
            st.markdown("#### Parámetros del Modelo")
            n_arboles = st.slider("Número de Árboles (Estimadores)", 20, 200, 100, step=20)
            profundidad = st.slider("Profundidad Máxima", 4, 20, 10, step=2)
            n_muestras = st.select_slider("Muestras Sintéticas", options=[500, 1000, 1500, 2500], value=1500)
            
            if st.button("⚡ Entrenar Modelo de IA Ahora", use_container_width=True):
                with st.spinner("Generando datos sintéticos y entrenando Random Forest con Scikit-learn..."):
                    res_entrenamiento = st.session_state.modelo_ia.entrenar(
                        num_muestras=n_muestras,
                        n_estimators=n_arboles,
                        max_depth=profundidad
                    )
                    st.success(f"¡Modelo {res_entrenamiento['tipo_modelo']} entrenado con éxito!")

        with col_t2:
            st.markdown("#### Evaluación Rigurosa sobre Conjunto de Prueba (20%)")
            if not st.session_state.modelo_ia.esta_entrenado:
                # Auto-entrenar con valores iniciales si no ha sido ejecutado
                st.session_state.modelo_ia.entrenar(num_muestras=1200)

            met = st.session_state.modelo_ia.metricas
            c_m1, c_m2, c_m3, c_m4 = st.columns(4)
            c_m1.metric("R² (Precisión)", f"{met.get('R2', 0.94):.4f}", help="Coeficiente de determinación sobre datos no vistos.")
            c_m2.metric("MAE", f"{met.get('MAE', 1.2):.2f} s", help="Error Absoluto Medio en segundos.")
            c_m3.metric("RMSE", f"{met.get('RMSE', 1.8):.2f} s", help="Raíz del Error Cuadrático Medio.")
            c_m4.metric("MSE", f"{met.get('MSE', 3.2):.2f}", help="Error Cuadrático Medio.")

            # Gráfico de Importancia de Variables
            if st.session_state.modelo_ia.importancia_variables:
                fig_imp = generar_grafico_importancia_variables(st.session_state.modelo_ia.importancia_variables)
                st.plotly_chart(fig_imp, use_container_width=True)

    with tab_ia2:
        st.markdown("#### Datos de Entrenamiento Sintéticos (Muestra Representativa)")
        datos_sint = st.session_state.modelo_ia.dataset_info
        if "X" in datos_sint:
            import pandas as pd
            df_muestras = pd.DataFrame(datos_sint["X"][:15], columns=datos_sint["nombres_columnas"])
            df_muestras["target_verde_g1 (s)"] = datos_sint["y"][:15]
            st.dataframe(df_muestras.style.format("{:.2f}"), use_container_width=True)
            st.caption(f"Conjunto total: {datos_sint['num_muestras']} escenarios sintéticos generados para calibración.")

    with tab_ia3:
        st.markdown("#### Generar Recomendación Adaptativa de Tiempos en Vivo")
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        with col_rec1:
            ia_q1 = st.number_input("Cola actual Vía 1 (veh)", 0.0, 50.0, 16.0, 1.0)
            ia_lam1 = st.number_input("Tasa de llegada Vía 1 (veh/min)", 5.0, 50.0, 28.0, 1.0)
        with col_rec2:
            ia_q2 = st.number_input("Cola actual Vía 2 (veh)", 0.0, 50.0, 5.0, 1.0)
            ia_lam2 = st.number_input("Tasa de llegada Vía 2 (veh/min)", 5.0, 50.0, 12.0, 1.0)
        with col_rec3:
            ia_C = st.number_input("Ciclo de verde combinado C (s)", 30.0, 120.0, 60.0, 5.0)
            ia_w1 = ia_q1 / (ia_lam1 / 60.0)
            ia_w2 = ia_q2 / (ia_lam2 / 60.0)
            st.caption(f"Tiempos de espera estimados: W₁ = {ia_w1:.1f}s | W₂ = {ia_w2:.1f}s")

        pred_ia = st.session_state.modelo_ia.predecir_tiempos_optimos(
            cola_v1=ia_q1, cola_v2=ia_q2, lambda_v1=ia_lam1, lambda_v2=ia_lam2,
            espera_v1=ia_w1, espera_v2=ia_w2, flujo_sat_1=36.0, flujo_sat_2=36.0,
            ciclo_total_C=ia_C
        )

        st.markdown("##### 🎯 Recomendación del Modelo de Machine Learning:")
        col_r_ia1, col_r_ia2, col_r_ia3 = st.columns(3)
        col_r_ia1.metric("Verde Recomendado Vía 1 (g₁)", f"{pred_ia['g1_recomendado']} s", f"{pred_ia['proporcion_g1']*100:.1f}% del ciclo")
        col_r_ia2.metric("Verde Recomendado Vía 2 (g₂)", f"{pred_ia['g2_recomendado']} s", f"{pred_ia['proporcion_g2']*100:.1f}% del ciclo")
        col_r_ia3.metric("Modelo Empleado", pred_ia['modelo_usado'], "Restricciones de seguridad aplicadas")


# ==============================================================================
# SECCIÓN 5: DETECCIÓN DE VEHÍCULOS MEDIANTE VIDEO (OPENCV)
# ==============================================================================
elif menu_seleccionado == "📹 Detección de Vehículos (OpenCV)":
    st.markdown('<div class="titulo-principal">Detección y Conteo de Vehículos por Video</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Módulo independiente de visión artificial con OpenCV para aforo vehicular automático por carril/vía.'
        '</div>',
        unsafe_allow_html=True
    )

    if not OPENCV_DISPONIBLE:
        st.error("⚠️ OpenCV no se encuentra disponible en el entorno actual. Consulte el archivo requirements.txt para su instalación.")
    else:
        tab_v1, tab_v2 = st.tabs(["🧪 Prueba con Video Sintético / Subir Archivo", "📖 Guía de Modelos Avanzados (YOLOv8)"])

        with tab_v1:
            col_vid_opt1, col_vid_opt2 = st.columns([1, 2])
            with col_vid_opt1:
                st.markdown("#### Opciones de Entrada de Video")
                modo_video = st.radio("Seleccione el origen del video:", ["Generar video sintético de laboratorio", "Cargar video propio (.mp4)"])
                
                archivo_video = None
                ruta_video_proc = "video_trafico_demo.mp4"

                if modo_video == "Cargar video propio (.mp4)":
                    archivo_video = st.file_uploader("Cargar video de intersección:", type=["mp4", "avi", "mov"])
                    if archivo_video is not None:
                        with open("video_usuario_temp.mp4", "wb") as f:
                            f.write(archivo_video.read())
                        ruta_video_proc = "video_usuario_temp.mp4"
                else:
                    if st.button("🎬 Generar Video Sintético Vial", use_container_width=True):
                        with st.spinner("Renderizando simulación de tráfico en video sintético..."):
                            DetectorVehiculosOpenCV.generar_video_sintetico_demostracion(ruta_video_proc, duracion_segundos=6, fps=20)
                            st.success("¡Video sintético generado con éxito!")

                st.markdown("#### Parámetros del Detector (MOG2)")
                area_min = st.slider("Área Mínima de Contorno (px)", 200, 2000, 450, step=50)
                umbral_mog2 = st.slider("Umbral de Varianza MOG2", 8, 32, 16, step=2)

                btn_procesar = st.button("🔍 Iniciar Análisis y Conteo", use_container_width=True)

            with col_vid_opt2:
                st.markdown("#### Visualización del Procesamiento en Tiempo Real")
                visor_imagen = st.empty()
                info_conteo = st.empty()

                if btn_procesar:
                    import cv2
                    if not os.path.exists(ruta_video_proc):
                        # Auto generar si no existe
                        DetectorVehiculosOpenCV.generar_video_sintetico_demostracion(ruta_video_proc, duracion_segundos=6, fps=20)

                    detector = DetectorVehiculosOpenCV(area_minima=area_min, umbral_var=float(umbral_mog2))
                    cap = cv2.VideoCapture(ruta_video_proc)

                    fotogramas_analizados = 0
                    conteo_max_v1 = 0
                    conteo_max_v2 = 0

                    with st.spinner("Procesando fotogramas con sustracción de fondo MOG2..."):
                        while cap.isOpened() and fotogramas_analizados < 120:
                            ret, frame = cap.read()
                            if not ret:
                                break
                            fotogramas_analizados += 1

                            frame_proc, res = detector.procesar_fotograma(frame)
                            conteo_max_v1 = res["conteo_v1"]
                            conteo_max_v2 = res["conteo_v2"]

                            # Mostrar fotograma procesado en Streamlit cada 3 cuadros para fluidez
                            if fotogramas_analizados % 3 == 0:
                                rgb = cv2.cvtColor(frame_proc, cv2.COLOR_BGR2RGB)
                                visor_imagen.image(rgb, caption=f"Fotograma #{fotogramas_analizados} | Sustracción MOG2 + Tracking de Centroides", use_container_width=True)
                                info_conteo.markdown(
                                    f"**Aforo Vía 1:** `{conteo_max_v1} vehículos` | "
                                    f"**Aforo Vía 2:** `{conteo_max_v2} vehículos` | "
                                    f"**Total Detectados:** `{conteo_max_v1 + conteo_max_v2} vehículos`"
                                )
                                time.sleep(0.04)

                        cap.release()
                    st.success(f"Análisis completado: {fotogramas_analizados} fotogramas examinados. Aforo final: {conteo_max_v1 + conteo_max_v2} vehículos.")

        with tab_v2:
            st.markdown("#### Integración con Modelos Avanzados de Detección de Objetos")
            instrucciones = obtener_instrucciones_modelos_avanzados()
            st.markdown(f"""
            - **Modelo Recomendado:** `{instrucciones['modelo_recomendado']}`
            - **Repositorio Oficial:** [{instrucciones['fuente_oficial']}]({instrucciones['fuente_oficial']})
            - **Ubicación en el Proyecto:** `{instrucciones['directorio_destino']}`
            
            ```markdown
            {instrucciones['como_activar']}
            ```
            
            **Estado Actual del Sistema:**  
            *{instrucciones['estado_actual']}*
            """)


# ==============================================================================
# SECCIÓN 6: COMPARACIÓN DE ESCENARIOS (FIJO vs CÁLCULO vs IA)
# ==============================================================================
elif menu_seleccionado == "📊 Comparación de Escenarios":
    st.markdown('<div class="titulo-principal">Comparación Metodológica de Escenarios</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Evaluación rigurosa bajo condiciones iniciales idénticas (ceteris paribus): Semáforo Fijo vs Cálculo Diferencial vs IA.'
        '</div>',
        unsafe_allow_html=True
    )

    st.info("📌 **Fórmula Oficial de Cálculo del Porcentaje de Mejora:**")
    st.latex(r"\text{Mejora (\%)} = \left( \frac{\text{Valor Inicial (Tiempos Fijos)} - \text{Valor Optimizado}}{\text{Valor Inicial (Tiempos Fijos)}} \right) \times 100")

    col_cp1, col_cp2, col_cp3 = st.columns(3)
    with col_cp1:
        comp_lam1 = st.slider("Tasa Vía 1 (λ₁ veh/min)", 10.0, 45.0, 26.0, step=2.0)
        comp_q1 = st.slider("Cola Inicial Vía 1", 0, 30, 14, step=2)
    with col_cp2:
        comp_lam2 = st.slider("Tasa Vía 2 (λ₂ veh/min)", 5.0, 30.0, 12.0, step=2.0)
        comp_q2 = st.slider("Cola Inicial Vía 2", 0, 30, 6, step=2)
    with col_cp3:
        comp_C = st.slider("Ciclo Verde Combinado C (s)", 40.0, 90.0, 60.0, step=5.0)
        comp_tiempo = st.slider("Horizonte de Prueba (s)", 60, 300, 180, step=30)

    # Ejecutar simulación comparativa
    res_comp = ejecutar_comparativa_escenarios(
        tasa_llegada_1=comp_lam1,
        tasa_llegada_2=comp_lam2,
        cola_inicial_1=comp_q1,
        cola_inicial_2=comp_q2,
        ciclo_total_C=comp_C,
        duracion_simulacion=float(comp_tiempo),
        semilla=101,
        modelo_ia=st.session_state.modelo_ia
    )

    m = res_comp["metricas"]
    tv = res_comp["tiempos_verde"]
    mej_calc = res_comp["mejoras_calculo_vs_fijo"]
    mej_ia = res_comp["mejoras_ia_vs_fijo"]

    # Fila de Tarjetas Comparativas de los 3 Métodos
    c_fijo, c_calc, c_ia = st.columns(3)
    with c_fijo:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #FF1744;">
            <div class="kpi-titulo">1. Semáforo Convencional (Tiempos Fijos)</div>
            <div class="kpi-valor">{tv['fijo']['g1']:.1f}s / {tv['fijo']['g2']:.1f}s</div>
            <p><strong>Espera Media:</strong> {m['fijo']['espera_promedio_global']:.1f} s<br>
            <strong>Cola Media:</strong> {m['fijo']['cola_promedio_total']:.1f} veh<br>
            <strong>Vehículos Atendidos:</strong> {m['fijo']['total_atendidos']} veh<br>
            <strong>Retraso Acumulado:</strong> {m['fijo']['retraso_total_acumulado']:.0f} s·veh</p>
            <div class="kpi-sub" style="color: #FF1744;">Escenario Base (Sin Optimización)</div>
        </div>
        """, unsafe_allow_html=True)

    with c_calc:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #00E5FF;">
            <div class="kpi-titulo">2. Optimización por Cálculo Diferencial</div>
            <div class="kpi-valor">{tv['calculo']['g1']:.1f}s / {tv['calculo']['g2']:.1f}s</div>
            <p><strong>Espera Media:</strong> {m['calculo']['espera_promedio_global']:.1f} s (<strong>{mej_calc['espera_pct']:+.1f}%</strong>)<br>
            <strong>Cola Media:</strong> {m['calculo']['cola_promedio_total']:.1f} veh (<strong>{mej_calc['cola_pct']:+.1f}%</strong>)<br>
            <strong>Vehículos Atendidos:</strong> {m['calculo']['total_atendidos']} veh<br>
            <strong>Retraso Acumulado:</strong> {m['calculo']['retraso_total_acumulado']:.0f} s·veh (<strong>{mej_calc['retraso_pct']:+.1f}%</strong>)</p>
            <div class="kpi-sub" style="color: #00E5FF;">Punto Crítico Analítico g*</div>
        </div>
        """, unsafe_allow_html=True)

    with c_ia:
        st.markdown(f"""
        <div class="kpi-card" style="border-top: 4px solid #00E676;">
            <div class="kpi-titulo">3. Inteligencia Artificial (Machine Learning)</div>
            <div class="kpi-valor">{tv['ia']['g1']:.1f}s / {tv['ia']['g2']:.1f}s</div>
            <p><strong>Espera Media:</strong> {m['ia']['espera_promedio_global']:.1f} s (<strong>{mej_ia['espera_pct']:+.1f}%</strong>)<br>
            <strong>Cola Media:</strong> {m['ia']['cola_promedio_total']:.1f} veh (<strong>{mej_ia['cola_pct']:+.1f}%</strong>)<br>
            <strong>Vehículos Atendidos:</strong> {m['ia']['total_atendidos']} veh<br>
            <strong>Retraso Acumulado:</strong> {m['ia']['retraso_total_acumulado']:.0f} s·veh (<strong>{mej_ia['retraso_pct']:+.1f}%</strong>)</p>
            <div class="kpi-sub" style="color: #00E676;">Control Multivariable Adaptativo</div>
        </div>
        """, unsafe_allow_html=True)

    # Gráfico de Barras Comparativo
    fig_barras = generar_grafico_comparativo_barras(res_comp)
    st.plotly_chart(fig_barras, use_container_width=True)

    # Gráfico de Radar de Desempeño
    fig_radar = generar_grafico_radar_desempeno(res_comp)
    st.plotly_chart(fig_radar, use_container_width=True)


# ==============================================================================
# SECCIÓN 7: FUNDAMENTACIÓN TEÓRICA Y REFERENCIAS BIBLIOGRÁFICAS APA 7
# ==============================================================================
elif menu_seleccionado == "📚 Fundamentación Teórica y APA 7":
    st.markdown('<div class="titulo-principal">Fundamentación Académica y Referencias APA 7</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo-principal">'
        'Marco conceptual, conexiones con la Ingeniería Industrial y citas bibliográficas académicas verificables.'
        '</div>',
        unsafe_allow_html=True
    )

    secciones = obtener_secciones_teoricas()
    tab_nombres = [v["titulo"] for v in secciones.values()]
    tabs = st.tabs(tab_nombres + ["📖 Bibliografía en Normas APA 7"])

    for i, (clave, sec) in enumerate(secciones.items()):
        with tabs[i]:
            st.markdown(f"### {sec['titulo']}")
            st.markdown(sec["contenido"])

    # Pestaña final de Bibliografía APA 7
    with tabs[-1]:
        st.markdown("### Referencias Bibliográficas Oficiales (Normas APA 7.ª Edición)")
        st.markdown(
            "Las siguientes referencias provienen de la literatura científica y técnica verificable presente "
            "en el acervo documental de la investigación:"
        )
        referencias = obtener_referencias_apa7()
        for ref in referencias:
            st.markdown(f"""
            <div class="kpi-card">
                <strong>{ref['cita']}</strong><br>
                <em>{ref['referencia']}</em><br>
                <small style="color: #00E5FF;"><strong>Aporte al Proyecto:</strong> {ref['tema']}</small>
            </div>
            """, unsafe_allow_html=True)
