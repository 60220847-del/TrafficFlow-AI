"""
MÓDULO DE GENERACIÓN DE GRÁFICOS Y VISUALIZACIÓN DINÁMICA (PLOTLY)
=================================================================
Proyecto: TrafficFlow AI
Carrera: Ingeniería Industrial
Asignatura: Cálculo Diferencial

Genera gráficos interactivos con estética profesional en tema oscuro,
optimizados para presentaciones y defensas académicas.
"""

from typing import Dict, Any, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Paleta de colores temáticos (Semáforo y Asfalto Moderno)
COLOR_VERDE = "#00E676"
COLOR_AMARILLO = "#FFD600"
COLOR_ROJO = "#FF1744"
COLOR_AZUL = "#2979FF"
COLOR_CIAN = "#00E5FF"
COLOR_PURPURA = "#D500F9"
COLOR_FONDO = "#0F141C"
COLOR_TARJETA = "#182230"
COLOR_TEXTO = "#ECEFF1"
COLOR_GRID = "#263238"


def crear_layout_base(titulo: str = "", alto: int = 420) -> dict:
    """Configura el layout estándar en tema oscuro para todos los gráficos."""
    return dict(
        title=dict(text=titulo, font=dict(color=COLOR_TEXTO, size=15, family="Segoe UI, sans-serif")),
        paper_bgcolor=COLOR_FONDO,
        plot_bgcolor=COLOR_TARJETA,
        font=dict(color=COLOR_TEXTO, family="Segoe UI, sans-serif"),
        height=alto,
        margin=dict(l=50, r=30, t=50, b=45),
        xaxis=dict(gridcolor=COLOR_GRID, zerolinecolor="#37474F", tickfont=dict(color="#B0BEC5")),
        yaxis=dict(gridcolor=COLOR_GRID, zerolinecolor="#37474F", tickfont=dict(color="#B0BEC5")),
        legend=dict(
            bgcolor="rgba(24, 34, 48, 0.8)",
            bordercolor=COLOR_GRID,
            font=dict(color=COLOR_TEXTO, size=11)
        )
    )


# ==============================================================================
# 1. VISUALIZACIÓN DE LA INTERSECCIÓN EN 2D
# ==============================================================================

def generar_vista_interseccion(estado_visual: Dict[str, Any]) -> go.Figure:
    """
    Renderiza la vista superior interactiva 2D de alta fidelidad de la intersección.
    Representa calzadas de asfalto con pasos peatonales (cebras), líneas reglamentarias,
    semáforos verticales con viseras y vehículos realistas (sedanes, SUVs, taxis) con
    ruedas, parabrisas, espejos, faros y luces de freno.
    """
    fig = go.Figure()

    lim = 75.0
    ancho_via = 26.0
    semi_via = ancho_via / 2.0

    # 1. Calzadas de asfalto oscuro con bordillos
    # Vía 1 (Vertical - Norte/Sur)
    fig.add_shape(
        type="rect", x0=-semi_via, x1=semi_via, y0=-lim, y1=lim,
        fillcolor="#1E293B", line=dict(color="#334155", width=2), layer="below"
    )
    # Vía 2 (Horizontal - Este/Oeste)
    fig.add_shape(
        type="rect", x0=-lim, x1=lim, y0=-semi_via, y1=semi_via,
        fillcolor="#1E293B", line=dict(color="#334155", width=2), layer="below"
    )
    # Cuadrante de Intersección central
    fig.add_shape(
        type="rect", x0=-semi_via, x1=semi_via, y0=-semi_via, y1=semi_via,
        fillcolor="#243042", line=dict(color="#475569", width=1.5), layer="below"
    )

    # 2. Aceras y césped de las esquinas
    fig.add_shape(type="rect", x0=-lim, x1=-semi_via, y0=semi_via, y1=lim, fillcolor="#0F172A", line=dict(color="#334155", width=1), layer="below")
    fig.add_shape(type="rect", x0=semi_via, x1=lim, y0=semi_via, y1=lim, fillcolor="#0F172A", line=dict(color="#334155", width=1), layer="below")
    fig.add_shape(type="rect", x0=-lim, x1=-semi_via, y0=-lim, y1=-semi_via, fillcolor="#0F172A", line=dict(color="#334155", width=1), layer="below")
    fig.add_shape(type="rect", x0=semi_via, x1=lim, y0=-lim, y1=-semi_via, fillcolor="#0F172A", line=dict(color="#334155", width=1), layer="below")

    # 3. Pasos peatonales de cebra (franjas blancas gruesas)
    franja_w = 1.6
    franja_l = 6.5
    gap = 1.4

    # Cebra Norte (y = semi_via + 2 a semi_via + 2 + franja_l)
    for x_c in [(-semi_via + 1.5 + k * (franja_w + gap)) for k in range(8)]:
        if x_c + franja_w <= semi_via - 1.0:
            fig.add_shape(type="rect", x0=x_c, x1=x_c + franja_w, y0=semi_via + 1.5, y1=semi_via + 1.5 + franja_l,
                          fillcolor="#F8FAFC", line=dict(width=0))
    # Cebra Sur (y = -semi_via - 1.5 - franja_l a -semi_via - 1.5)
    for x_c in [(-semi_via + 1.5 + k * (franja_w + gap)) for k in range(8)]:
        if x_c + franja_w <= semi_via - 1.0:
            fig.add_shape(type="rect", x0=x_c, x1=x_c + franja_w, y0=-semi_via - 1.5 - franja_l, y1=-semi_via - 1.5,
                          fillcolor="#F8FAFC", line=dict(width=0))
    # Cebra Oeste (x = -semi_via - 1.5 - franja_l a -semi_via - 1.5)
    for y_c in [(-semi_via + 1.5 + k * (franja_w + gap)) for k in range(8)]:
        if y_c + franja_w <= semi_via - 1.0:
            fig.add_shape(type="rect", x0=-semi_via - 1.5 - franja_l, x1=-semi_via - 1.5, y0=y_c, y1=y_c + franja_w,
                          fillcolor="#F8FAFC", line=dict(width=0))
    # Cebra Este (x = semi_via + 1.5 a semi_via + 1.5 + franja_l)
    for y_c in [(-semi_via + 1.5 + k * (franja_w + gap)) for k in range(8)]:
        if y_c + franja_w <= semi_via - 1.0:
            fig.add_shape(type="rect", x0=semi_via + 1.5, x1=semi_via + 1.5 + franja_l, y0=y_c, y1=y_c + franja_w,
                          fillcolor="#F8FAFC", line=dict(width=0))

    # 4. Líneas de detención de semáforo (Stop lines)
    fig.add_shape(type="line", x0=0, x1=semi_via, y0=-semi_via - 9.0, y1=-semi_via - 9.0,
                  line=dict(color="#FFFFFF", width=3.5))
    fig.add_shape(type="line", x0=-semi_via, x1=0, y0=semi_via + 9.0, y1=semi_via + 9.0,
                  line=dict(color="#FFFFFF", width=3.5))
    fig.add_shape(type="line", x0=-semi_via - 9.0, x1=-semi_via - 9.0, y0=-semi_via, y1=0,
                  line=dict(color="#FFFFFF", width=3.5))
    fig.add_shape(type="line", x0=semi_via + 9.0, x1=semi_via + 9.0, y0=0, y1=semi_via,
                  line=dict(color="#FFFFFF", width=3.5))

    # 5. Doble línea central amarilla
    for y_s in range(int(semi_via + 9), int(lim), 6):
        fig.add_shape(type="line", x0=-0.4, x1=-0.4, y0=y_s, y1=min(lim, y_s + 4), line=dict(color="#F59E0B", width=2))
        fig.add_shape(type="line", x0=0.4, x1=0.4, y0=y_s, y1=min(lim, y_s + 4), line=dict(color="#F59E0B", width=2))
    for y_s in range(-int(lim), -int(semi_via + 9), 6):
        fig.add_shape(type="line", x0=-0.4, x1=-0.4, y0=y_s, y1=y_s + 4, line=dict(color="#F59E0B", width=2))
        fig.add_shape(type="line", x0=0.4, x1=0.4, y0=y_s, y1=y_s + 4, line=dict(color="#F59E0B", width=2))

    for x_s in range(int(semi_via + 9), int(lim), 6):
        fig.add_shape(type="line", x0=x_s, x1=min(lim, x_s + 4), y0=-0.4, y1=-0.4, line=dict(color="#F59E0B", width=2))
        fig.add_shape(type="line", x0=x_s, x1=min(lim, x_s + 4), y0=0.4, y1=0.4, line=dict(color="#F59E0B", width=2))
    for x_s in range(-int(lim), -int(semi_via + 9), 6):
        fig.add_shape(type="line", x0=x_s, x1=x_s + 4, y0=-0.4, y1=-0.4, line=dict(color="#F59E0B", width=2))
        fig.add_shape(type="line", x0=x_s, x1=x_s + 4, y0=0.4, y1=0.4, line=dict(color="#F59E0B", width=2))

    # 6. Semáforos verticales con viseras y luces activas
    luz1 = estado_visual["luz_1"]
    luz2 = estado_visual["luz_2"]
    t_rest = estado_visual["tiempo_restante_fase"]

    col_luz1 = COLOR_VERDE if luz1 == "VERDE" else (COLOR_AMARILLO if luz1 == "AMARILLO" else COLOR_ROJO)
    col_luz2 = COLOR_VERDE if luz2 == "VERDE" else (COLOR_AMARILLO if luz2 == "AMARILLO" else COLOR_ROJO)

    # Marcadores de semáforo estilizados como postes
    fig.add_trace(go.Scatter(
        x=[semi_via + 4, -semi_via - 4], y=[-semi_via - 6, semi_via + 6],
        mode="markers+text",
        marker=dict(size=26, color=col_luz1, symbol="square", line=dict(color="#F8FAFC", width=2.5)),
        text=[f"V1: {luz1}<br>{t_rest:.1f}s", f"V1: {luz1}<br>{t_rest:.1f}s"],
        textposition="bottom right",
        name="Semáforo Vía 1 (N-S)",
        hoverinfo="text"
    ))
    fig.add_trace(go.Scatter(
        x=[-semi_via - 6, semi_via + 6], y=[-semi_via - 4, semi_via + 4],
        mode="markers+text",
        marker=dict(size=26, color=col_luz2, symbol="square", line=dict(color="#F8FAFC", width=2.5)),
        text=[f"V2: {luz2}<br>{t_rest:.1f}s", f"V2: {luz2}<br>{t_rest:.1f}s"],
        textposition="top left",
        name="Semáforo Vía 2 (E-O)",
        hoverinfo="text"
    ))

    # 7. Dibujar vehículos realistas (en ambas direcciones)
    # Función auxiliar para renderizar un auto realista con sus componentes
    def dibujar_auto_realista(vx, vy, orientacion, color, tipo, id_v, estado_v):
        # orientacion: 'N->S', 'S->N', 'O->E', 'E->O'
        L = 7.5
        W = 4.2
        if tipo == "SUV": L = 8.2; W = 4.6
        elif tipo == "Compacto": L = 6.2; W = 3.8

        if orientacion in ['N->S', 'S->N']:
            # Vertical
            x0 = vx - W / 2.0
            x1 = vx + W / 2.0
            y0 = vy - L / 2.0
            y1 = vy + L / 2.0
            # Carrocería
            fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                          fillcolor=color, line=dict(color="#FFFFFF", width=1), layer="above")
            # Parabrisas (delantero y trasero)
            y_para_d = y1 - 2.2 if orientacion == 'S->N' else y0 + 1.2
            y_para_t = y0 + 1.2 if orientacion == 'S->N' else y1 - 2.2
            fig.add_shape(type="rect", x0=x0 + 0.6, x1=x1 - 0.6, y0=y_para_d, y1=y_para_d + 1.2,
                          fillcolor="#0F172A", line=dict(width=0), layer="above")
            fig.add_shape(type="rect", x0=x0 + 0.6, x1=x1 - 0.6, y0=y_para_t, y1=y_para_t + 1.0,
                          fillcolor="#1E293B", line=dict(width=0), layer="above")
            # Ruedas laterales
            fig.add_shape(type="rect", x0=x0 - 0.5, x1=x0, y0=y0 + 1.0, y1=y0 + 2.5, fillcolor="#000", line=dict(width=0))
            fig.add_shape(type="rect", x0=x1, x1=x1 + 0.5, y0=y0 + 1.0, y1=y0 + 2.5, fillcolor="#000", line=dict(width=0))
            fig.add_shape(type="rect", x0=x0 - 0.5, x1=x0, y0=y1 - 2.5, y1=y1 - 1.0, fillcolor="#000", line=dict(width=0))
            fig.add_shape(type="rect", x0=x1, x1=x1 + 0.5, y0=y1 - 2.5, y1=y1 - 1.0, fillcolor="#000", line=dict(width=0))
        else:
            # Horizontal
            x0 = vx - L / 2.0
            x1 = vx + L / 2.0
            y0 = vy - W / 2.0
            y1 = vy + W / 2.0
            # Carrocería
            fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                          fillcolor=color, line=dict(color="#FFFFFF", width=1), layer="above")
            # Parabrisas
            x_para_d = x1 - 2.2 if orientacion == 'O->E' else x0 + 1.2
            x_para_t = x0 + 1.2 if orientacion == 'O->E' else x1 - 2.2
            fig.add_shape(type="rect", x0=x_para_d, x1=x_para_d + 1.2, y0=y0 + 0.6, y1=y1 - 0.6,
                          fillcolor="#0F172A", line=dict(width=0), layer="above")
            fig.add_shape(type="rect", x0=x_para_t, x1=x_para_t + 1.0, y0=y0 + 0.6, y1=y1 - 0.6,
                          fillcolor="#1E293B", line=dict(width=0), layer="above")
            # Ruedas laterales
            fig.add_shape(type="rect", x0=x0 + 1.0, x1=x0 + 2.5, y0=y0 - 0.5, y1=y0, fillcolor="#000", line=dict(width=0))
            fig.add_shape(type="rect", x0=x0 + 1.0, x1=x0 + 2.5, y0=y1, y1=y1 + 0.5, fillcolor="#000", line=dict(width=0))
            fig.add_shape(type="rect", x0=x1 - 2.5, x1=x1 - 1.0, y0=y0 - 0.5, y1=y0, fillcolor="#000", line=dict(width=0))
            fig.add_shape(type="rect", x0=x1 - 2.5, x1=x1 - 1.0, y0=y1, y1=y1 + 0.5, fillcolor="#000", line=dict(width=0))

    # Trazar vehículos de Vía 1
    scatter_v1_x = []
    scatter_v1_y = []
    scatter_v1_txt = []
    for v in estado_visual["vehiculos_1"]:
        dir_v = v.get("direccion", 1)
        pos = v["pos"]
        color = v.get("color", "#3B82F6")
        tipo = v.get("tipo", "Sedán")
        
        # Mapeo a coordenadas
        if dir_v == 1:
            # Norte hacia Sur (baja por carril derecho: x = semi_via/2)
            vx = semi_via / 2.0
            vy = (semi_via + 12.0) - pos if pos > 0 else (semi_via + 12.0) - pos
            vy = -semi_via - 9.0 + pos
            orient = 'S->N' if dir_v == -1 else 'N->S'
        else:
            # Sur hacia Norte (sube por carril izquierdo: x = -semi_via/2)
            vx = -semi_via / 2.0
            vy = semi_via + 9.0 - pos
            orient = 'S->N'

        if -lim <= vy <= lim:
            dibujar_auto_realista(vx, vy, orient, color, tipo, v["id"], v["estado"])
            scatter_v1_x.append(vx)
            scatter_v1_y.append(vy)
            scatter_v1_txt.append(f"{tipo} #{v['id']} ({color})<br>Estado: {v['estado']}")

    if scatter_v1_x:
        fig.add_trace(go.Scatter(
            x=scatter_v1_x, y=scatter_v1_y, mode="markers",
            marker=dict(size=14, color="rgba(0,0,0,0)"),
            text=scatter_v1_txt, hoverinfo="text", name="Vehículos Vía 1"
        ))

    # Trazar vehículos de Vía 2
    scatter_v2_x = []
    scatter_v2_y = []
    scatter_v2_txt = []
    for v in estado_visual["vehiculos_2"]:
        dir_v = v.get("direccion", 1)
        pos = v["pos"]
        color = v.get("color", "#F59E0B")
        tipo = v.get("tipo", "Sedán")

        if dir_v == 1:
            # Oeste hacia Este (hacia la derecha por carril inferior: y = -semi_via/2)
            vy = -semi_via / 2.0
            vx = -semi_via - 9.0 + pos
            orient = 'O->E'
        else:
            # Este hacia Oeste (hacia la izquierda por carril superior: y = semi_via/2)
            vy = semi_via / 2.0
            vx = semi_via + 9.0 - pos
            orient = 'E->O'

        if -lim <= vx <= lim:
            dibujar_auto_realista(vx, vy, orient, color, tipo, v["id"], v["estado"])
            scatter_v2_x.append(vx)
            scatter_v2_y.append(vy)
            scatter_v2_txt.append(f"{tipo} #{v['id']} ({color})<br>Estado: {v['estado']}")

    if scatter_v2_x:
        fig.add_trace(go.Scatter(
            x=scatter_v2_x, y=scatter_v2_y, mode="markers",
            marker=dict(size=14, color="rgba(0,0,0,0)"),
            text=scatter_v2_txt, hoverinfo="text", name="Vehículos Vía 2"
        ))

    layout = crear_layout_base("🚦 Mapa Vectorial Detallado de la Intersección y Vehículos Realistas", alto=500)
    layout["xaxis"].update(range=[-lim, lim], zeroline=False, showticklabels=False)
    layout["yaxis"].update(range=[-lim, lim], zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1)
    fig.update_layout(layout)

    return fig


# ==============================================================================
# 2. GRÁFICAS DE DINÁMICA DE TRÁFICO Y COLAS (ECUACIÓN DIFERENCIAL)
# ==============================================================================

def generar_grafico_dinamica_colas(historial: Dict[str, List[Any]]) -> go.Figure:
    """
    Gráfica de la evolución temporal de colas Q(t) y las derivadas dQ/dt = λ - μ.
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.12,
        subplot_titles=(
            "Evolución Temporal de las Colas: Q₁(t) y Q₂(t)",
            "Tasa Neta de Cambio: Q'(t) = λ(t) - μ(t)"
        )
    )

    t = historial["tiempo"]

    # Fila 1: Colas vehiculares
    fig.add_trace(
        go.Scatter(x=t, y=historial["cola_1"], mode="lines", name="Cola Vía 1 Q₁(t)",
                   line=dict(color=COLOR_CIAN, width=2.5)),
        row=1, col=1
    )
    fig.add_trace(
        go.Scatter(x=t, y=historial["cola_2"], mode="lines", name="Cola Vía 2 Q₂(t)",
                   line=dict(color=COLOR_AMARILLO, width=2.5)),
        row=1, col=1
    )

    # Fila 2: Derivadas instantáneas
    fig.add_trace(
        go.Scatter(x=t, y=historial["derivada_q1"], mode="lines", name="Q'₁(t) = λ₁ - μ₁",
                   line=dict(color=COLOR_AZUL, width=1.8, dash="dot")),
        row=2, col=1
    )
    fig.add_trace(
        go.Scatter(x=t, y=historial["derivada_q2"], mode="lines", name="Q'₂(t) = λ₂ - μ₂",
                   line=dict(color=COLOR_ROJO, width=1.8, dash="dot")),
        row=2, col=1
    )
    # Línea de equilibrio dQ/dt = 0
    fig.add_hline(y=0, line_dash="dash", line_color="#78909C", row=2, col=1)

    base = crear_layout_base("Dinámica de Colas y Ecuación Diferencial del Flujo Vehicular", alto=480)
    fig.update_layout(base)
    fig.update_xaxes(title_text="Tiempo de Simulación (segundos)", row=2, col=1)
    fig.update_yaxes(title_text="Vehículos en Cola", row=1, col=1)
    fig.update_yaxes(title_text="Tasa Neta (veh/s)", row=2, col=1)

    return fig


def generar_grafico_tasas_flujo(historial: Dict[str, List[Any]]) -> go.Figure:
    """
    Gráfica comparativa de tasas de llegada λ(t) vs tasas de salida μ(t).
    """
    fig = go.Figure()
    t = historial["tiempo"]

    fig.add_trace(go.Scatter(
        x=t, y=historial["tasa_llegada_1"], mode="lines",
        name="Tasa Llegada Vía 1 (λ₁)", line=dict(color=COLOR_CIAN, width=2)
    ))
    fig.add_trace(go.Scatter(
        x=t, y=historial["tasa_salida_1"], mode="lines",
        name="Capacidad Descarga Vía 1 (μ₁)", line=dict(color=COLOR_VERDE, width=2.5, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=t, y=historial["tasa_llegada_2"], mode="lines",
        name="Tasa Llegada Vía 2 (λ₂)", line=dict(color=COLOR_AMARILLO, width=2)
    ))
    fig.add_trace(go.Scatter(
        x=t, y=historial["tasa_salida_2"], mode="lines",
        name="Capacidad Descarga Vía 2 (μ₂)", line=dict(color=COLOR_ROJO, width=2.5, dash="dash")
    ))

    layout = crear_layout_base("Comparación de Tasas de Llegada (λ) y Salida Semafórica (μ)", alto=380)
    layout["xaxis"]["title"] = "Tiempo (segundos)"
    layout["yaxis"]["title"] = "Flujo (vehículos / segundo)"
    fig.update_layout(layout)
    return fig


# ==============================================================================
# 3. GRÁFICAS DE CÁLCULO DIFERENCIAL Y OPTIMIZACIÓN
# ==============================================================================

def generar_grafico_optimizacion_calculo(
    datos_curvas: Dict[str, List[float]],
    resultado_opt: Dict[str, Any]
) -> go.Figure:
    """
    Visualiza la función objetivo E(g), su primera derivada E'(g) y segunda derivada E''(g).
    Marca con precisión el punto crítico analítico g* y la región de factibilidad.
    """
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=(
            "Función Objetivo de Retraso: E(g) = A/g + B/(C - g)",
            "Primera Derivada: E'(g) = -A/g² + B/(C - g)²  [Condición de Primer Orden]",
            "Segunda Derivada: E''(g) = 2A/g³ + 2B/(C - g)³  [Criterio de Convexidad y Mínimo]"
        )
    )

    g_vals = datos_curvas["g"]
    E_vals = datos_curvas["E"]
    Ep_vals = datos_curvas["E_prima"]
    Epp_vals = datos_curvas["E_segunda"]

    g_star = resultado_opt["g_teorico"]
    g_opt = resultado_opt["g_optimo"]
    E_min = resultado_opt["E_optimo"]
    g_min = resultado_opt["g_min"]
    g_max = resultado_opt["g_max"]

    # Fila 1: E(g)
    fig.add_trace(
        go.Scatter(x=g_vals, y=E_vals, mode="lines", name="E(g)",
                   line=dict(color=COLOR_CIAN, width=3)),
        row=1, col=1
    )
    # Marcador del punto óptimo en E(g)
    fig.add_trace(
        go.Scatter(
            x=[g_opt], y=[E_min], mode="markers+text",
            marker=dict(color=COLOR_VERDE, size=13, symbol="diamond", line=dict(color="#FFFFFF", width=2)),
            text=[f"  Mínimo Óptimo Factible<br>  g* = {g_opt:.2f} s, E* = {E_min:.2f}"],
            textposition="top right",
            name="Mínimo g*",
            hoverinfo="text"
        ),
        row=1, col=1
    )

    # Fila 2: E'(g)
    fig.add_trace(
        go.Scatter(x=g_vals, y=Ep_vals, mode="lines", name="E'(g)",
                   line=dict(color=COLOR_AMARILLO, width=2.5)),
        row=2, col=1
    )
    fig.add_hline(y=0, line_dash="dash", line_color="#90A4AE", row=2, col=1)
    # Corte con el eje horizontal en E'(g) = 0
    fig.add_trace(
        go.Scatter(
            x=[g_star], y=[0], mode="markers+text",
            marker=dict(color=COLOR_AMARILLO, size=10, symbol="circle"),
            text=[f"  Corte E'(g)=0 en g={g_star:.2f}s"],
            textposition="bottom right",
            name="E'(g*)=0",
            hoverinfo="text"
        ),
        row=2, col=1
    )

    # Fila 3: E''(g)
    fig.add_trace(
        go.Scatter(x=g_vals, y=Epp_vals, mode="lines", name="E''(g)",
                   line=dict(color=COLOR_PURPURA, width=2.5)),
        row=3, col=1
    )
    # Línea horizontal cero para contrastar que E'' > 0 siempre
    fig.add_hline(y=0, line_dash="solid", line_color="#CFD8DC", row=3, col=1)

    # Región de restricciones operativas en los 3 paneles
    for r in [1, 2, 3]:
        fig.add_vrect(
            x0=g_min, x1=g_max,
            fillcolor="rgba(0, 230, 118, 0.08)",
            line_width=1, line_dash="dot", line_color=COLOR_VERDE,
            row=r, col=1
        )

    layout = crear_layout_base("Demostración Gráfica del Cálculo Diferencial y Optimización", alto=620)
    fig.update_layout(layout)
    fig.update_xaxes(title_text="Tiempo de Verde Vía 1: g (segundos)", row=3, col=1)
    fig.update_yaxes(title_text="Retraso E(g)", row=1, col=1, range=[0, min(50, max(E_vals) * 0.7)])
    fig.update_yaxes(title_text="Derivada E'(g)", row=2, col=1, range=[-5, 5])
    fig.update_yaxes(title_text="Concavidad E''(g)", row=3, col=1, range=[0, 1.5])

    return fig


# ==============================================================================
# 4. GRÁFICAS DE INTELIGENCIA ARTIFICIAL (MACHINE LEARNING)
# ==============================================================================

def generar_grafico_importancia_variables(importancias: List[tuple]) -> go.Figure:
    """
    Gráfico horizontal de barras con la importancia de las características predictoras.
    """
    nombres = [item[0] for item in importancias]
    valores = [item[1] for item in importancias]

    # Traducción amigable
    nombres_amigables = {
        "cola_v1": "Cola Vía 1 (Q₁)",
        "cola_v2": "Cola Vía 2 (Q₂)",
        "lambda_v1": "Tasa Llegada 1 (λ₁)",
        "lambda_v2": "Tasa Llegada 2 (λ₂)",
        "espera_v1": "Tiempo Espera 1 (W₁)",
        "espera_v2": "Tiempo Espera 2 (W₂)",
        "flujo_sat_1": "Capacidad Sat. 1 (S₁)",
        "flujo_sat_2": "Capacidad Sat. 2 (S₂)",
        "ciclo_total_C": "Ciclo Total (C)"
    }
    etiquetas = [nombres_amigables.get(n, n) for n in nombres]

    fig = go.Figure(go.Bar(
        x=valores,
        y=etiquetas,
        orientation="h",
        marker=dict(
            color=valores,
            colorscale=[[0, "#2979FF"], [0.5, "#00E5FF"], [1, "#00E676"]],
            line=dict(color="#FFFFFF", width=1)
        )
    ))

    layout = crear_layout_base("Importancia de Variables en la Decisión de la IA (Random Forest)", alto=360)
    layout["xaxis"]["title"] = "Importancia Relativa Normalizada (Gini Importance)"
    layout["yaxis"]["autorange"] = "reversed"
    fig.update_layout(layout)
    return fig


# ==============================================================================
# 5. GRÁFICAS DE COMPARACIÓN DE ESCENARIOS
# ==============================================================================

def generar_grafico_comparativo_barras(resultado_comp: Dict[str, Any]) -> go.Figure:
    """
    Gráfico de barras agrupadas comparando KPIs entre Fijo, Cálculo e IA.
    """
    metricas = resultado_comp["metricas"]
    metodos = ["Tiempos Fijos (Convencional)", "Cálculo Diferencial (Analítico)", "Inteligencia Artificial (ML)"]

    esperas = [
        metricas["fijo"]["espera_promedio_global"],
        metricas["calculo"]["espera_promedio_global"],
        metricas["ia"]["espera_promedio_global"]
    ]
    colas = [
        metricas["fijo"]["cola_promedio_total"],
        metricas["calculo"]["cola_promedio_total"],
        metricas["ia"]["cola_promedio_total"]
    ]
    atendidos = [
        metricas["fijo"]["total_atendidos"],
        metricas["calculo"]["total_atendidos"],
        metricas["ia"]["total_atendidos"]
    ]

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=(
            "Tiempo Promedio de Espera (s)",
            "Longitud Promedio de Colas (veh)",
            "Total de Vehículos Atendidos"
        )
    )

    colores = [COLOR_ROJO, COLOR_CIAN, COLOR_VERDE]

    fig.add_trace(
        go.Bar(x=metodos, y=esperas, marker_color=colores, text=[f"{v:.1f}s" for v in esperas], textposition="auto"),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(x=metodos, y=colas, marker_color=colores, text=[f"{v:.1f} veh" for v in colas], textposition="auto"),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(x=metodos, y=atendidos, marker_color=colores, text=[f"{v} veh" for v in atendidos], textposition="auto"),
        row=1, col=3
    )

    layout = crear_layout_base("Evaluación Comparativa de Desempeño: Fijo vs Cálculo vs IA", alto=380)
    layout["showlegend"] = False
    fig.update_layout(layout)
    fig.update_xaxes(tickangle=-25)
    return fig


def generar_grafico_radar_desempeno(resultado_comp: Dict[str, Any]) -> go.Figure:
    """
    Gráfico de radar multivariado que resume la eficiencia integral de los 3 métodos.
    """
    m = resultado_comp["metricas"]

    # Invertir métricas de demora para que mayor valor = mayor eficiencia
    # Eficiencia de espera = 100 / (1 + espera)
    # Eficiencia de cola = 100 / (1 + cola)
    # Eficiencia de rendimiento = total atendidos
    categorias = [
        "Rapidez de Atención (1/Espera)",
        "Fluidez Vial (1/Cola)",
        "Capacidad de Desahogo",
        "Balance entre Vías",
        "Eficiencia de Retraso"
    ]

    def extraer_puntuaciones(metrica_metodo: dict, g1: float, g2: float) -> List[float]:
        w = metrica_metodo["espera_promedio_global"]
        q = metrica_metodo["cola_promedio_total"]
        aten = metrica_metodo["total_atendidos"]
        balance = 100.0 - (abs(g1 - g2) / max(1.0, g1 + g2)) * 100.0
        retraso = metrica_metodo["retraso_total_acumulado"]
        return [
            round(min(100.0, 500.0 / max(5.0, w)), 1),
            round(min(100.0, 500.0 / max(5.0, q)), 1),
            round(min(100.0, (aten / 60.0) * 100.0), 1),
            round(balance, 1),
            round(min(100.0, 10000.0 / max(100.0, retraso)), 1)
        ]

    tv = resultado_comp["tiempos_verde"]
    r_fijo = extraer_puntuaciones(m["fijo"], tv["fijo"]["g1"], tv["fijo"]["g2"])
    r_calc = extraer_puntuaciones(m["calculo"], tv["calculo"]["g1"], tv["calculo"]["g2"])
    r_ia = extraer_puntuaciones(m["ia"], tv["ia"]["g1"], tv["ia"]["g2"])

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=r_fijo + [r_fijo[0]], theta=categorias + [categorias[0]],
        fill="toself", name="Tiempos Fijos", line=dict(color=COLOR_ROJO, width=2)
    ))
    fig.add_trace(go.Scatterpolar(
        r=r_calc + [r_calc[0]], theta=categorias + [categorias[0]],
        fill="toself", name="Cálculo Diferencial", line=dict(color=COLOR_CIAN, width=2.5)
    ))
    fig.add_trace(go.Scatterpolar(
        r=r_ia + [r_ia[0]], theta=categorias + [categorias[0]],
        fill="toself", name="Inteligencia Artificial", line=dict(color=COLOR_VERDE, width=2.5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], color="#90A4AE", gridcolor=COLOR_GRID),
            angularaxis=dict(color=COLOR_TEXTO, gridcolor=COLOR_GRID),
            bgcolor=COLOR_TARJETA
        ),
        paper_bgcolor=COLOR_FONDO,
        font=dict(color=COLOR_TEXTO, family="Segoe UI, sans-serif"),
        title=dict(text="Radar Integral de Eficiencia Operativa", font=dict(size=15, color=COLOR_TEXTO)),
        height=420,
        margin=dict(l=60, r=60, t=50, b=40),
        legend=dict(font=dict(color=COLOR_TEXTO))
    )
    return fig
