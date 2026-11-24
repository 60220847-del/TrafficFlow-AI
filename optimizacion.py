"""
MÓDULO DE CÁLCULO DIFERENCIAL Y OPTIMIZACIÓN MATEMÁTICA
======================================================
Proyecto: TrafficFlow AI
Carrera: Ingeniería Industrial
Asignatura: Cálculo Diferencial

Este módulo implementa el análisis analítico y numérico del modelo didáctico
de optimización de tiempos de semáforo:
    E(g) = A/g + B/(C - g)

Donde:
    - E(g): Función objetivo que representa el índice de retraso o costo total.
    - A: Parámetro de flujo/demanda en la Vía 1 (A > 0).
    - B: Parámetro de flujo/demanda en la Vía 2 (B > 0).
    - C: Duración del ciclo total asignado al verde combinado (C > 0).
    - g: Tiempo de luz verde asignado a la Vía 1 (g1 = g).
    - C - g: Tiempo de luz verde asignado a la Vía 2 (g2 = C - g).
"""

import math
from typing import Dict, Any, Tuple, List


def funcion_objetivo(g: float, A: float, B: float, C: float) -> float:
    """
    Evalúa la función objetivo E(g) = A/g + B/(C - g).
    
    Parámetros:
        g (float): Tiempo de verde para la vía 1 (segundos).
        A (float): Coeficiente de demanda para la vía 1.
        B (float): Coeficiente de demanda para la vía 2.
        C (float): Ciclo total disponible para ambas fases (segundos).
        
    Retorna:
        float: Valor del índice de retraso E(g).
    """
    if g <= 0 or g >= C:
        return float('inf')
    return (A / g) + (B / (C - g))


def primera_derivada(g: float, A: float, B: float, C: float) -> float:
    """
    Evalúa la primera derivada E'(g) = -A/g^2 + B/(C - g)^2.
    
    Representa la tasa de cambio instantánea del retraso respecto al tiempo de verde.
    """
    if g <= 0 or g >= C:
        return float('nan')
    return -(A / (g ** 2)) + (B / ((C - g) ** 2))


def segunda_derivada(g: float, A: float, B: float, C: float) -> float:
    """
    Evalúa la segunda derivada E''(g) = 2A/g^3 + 2B/(C - g)^3.
    
    Determina la concavidad de la función. Dado que A>0, B>0 y 0 < g < C,
    E''(g) > 0 en todo el dominio, lo que demuestra estricta convexidad.
    """
    if g <= 0 or g >= C:
        return float('nan')
    return (2.0 * A / (g ** 3)) + (2.0 * B / ((C - g) ** 3))


def calcular_punto_critico_teorico(A: float, B: float, C: float) -> float:
    """
    Calcula el punto crítico analítico resolviendo E'(g) = 0:
        g* = C * sqrt(A) / (sqrt(A) + sqrt(B))
    """
    sqrt_A = math.sqrt(A)
    sqrt_B = math.sqrt(B)
    return C * sqrt_A / (sqrt_A + sqrt_B)


def optimizar_tiempos_semaforo(
    A: float,
    B: float,
    C: float,
    g_min: float = 10.0,
    h_min: float = 10.0
) -> Dict[str, Any]:
    """
    Ejecuta el análisis completo de optimización, incluyendo restricciones físicas.
    
    Restricciones:
        g >= g_min          (Tiempo mínimo de verde para la Vía 1)
        C - g >= h_min  =>  g <= C - h_min (Tiempo mínimo de verde para la Vía 2)
        
    Retorna un diccionario con:
        - Punto crítico analítico no restringido (g_teorico)
        - Tiempo óptimo factible (g_optimo)
        - Tiempo óptimo vía 2 (g2_optimo = C - g_optimo)
        - Valor mínimo de E (E_min)
        - Valor de la segunda derivada en el óptimo (E_segunda_opt)
        - Estado de restricción ('interior', 'limite_inferior', 'limite_superior')
        - Pasos matemáticos detallados para la exposición.
    """
    # Validaciones iniciales
    if A <= 0 or B <= 0 or C <= 0:
        raise ValueError("Los parámetros A, B y C deben ser estrictamente positivos.")
        
    g_max = C - h_min
    if g_min >= g_max:
        raise ValueError(
            f"Restricciones incompatibles: g_min ({g_min}s) debe ser menor que C - h_min ({g_max}s)."
        )

    # 1. Punto crítico teórico analítico
    g_teorico = calcular_punto_critico_teorico(A, B, C)
    E_teorico = funcion_objetivo(g_teorico, A, B, C)
    E_segunda_teorico = segunda_derivada(g_teorico, A, B, C)

    # 2. Aplicación de restricciones de frontera [g_min, g_max]
    if g_teorico < g_min:
        g_optimo = g_min
        estado_restriccion = "limite_inferior"
        motivo = f"El punto crítico teórico ({g_teorico:.2f} s) es menor que el mínimo de seguridad ({g_min} s)."
    elif g_teorico > g_max:
        g_optimo = g_max
        estado_restriccion = "limite_superior"
        motivo = f"El punto crítico teórico ({g_teorico:.2f} s) excede el máximo permitido ({g_max} s) para garantizar el verde mínimo de la vía 2."
    else:
        g_optimo = g_teorico
        estado_restriccion = "interior"
        motivo = f"El punto crítico teórico ({g_teorico:.2f} s) pertenece al intervalo factible [{g_min} s, {g_max} s]."

    E_optimo = funcion_objetivo(g_optimo, A, B, C)
    E_primera_opt = primera_derivada(g_optimo, A, B, C)
    E_segunda_opt = segunda_derivada(g_optimo, A, B, C)

    g2_optimo = C - g_optimo

    # Relación analítica esperada del valor mínimo teórico:
    # E(g*) = (sqrt(A) + sqrt(B))^2 / C
    E_min_formula_cerrada = ((math.sqrt(A) + math.sqrt(B)) ** 2) / C

    return {
        "A": A,
        "B": B,
        "C": C,
        "g_min": g_min,
        "h_min": h_min,
        "g_max": g_max,
        "g_teorico": g_teorico,
        "E_teorico": E_teorico,
        "E_segunda_teorico": E_segunda_teorico,
        "g_optimo": g_optimo,
        "g2_optimo": g2_optimo,
        "E_optimo": E_optimo,
        "E_primera_opt": E_primera_opt,
        "E_segunda_opt": E_segunda_opt,
        "E_min_formula_cerrada": E_min_formula_cerrada,
        "estado_restriccion": estado_restriccion,
        "motivo_restriccion": motivo,
        "es_minimo": E_segunda_opt > 0,
        "proporcion_g1": g_optimo / C,
        "proporcion_g2": g2_optimo / C,
    }


def generar_datos_curvas(
    A: float,
    B: float,
    C: float,
    puntos: int = 400,
    margen: float = 0.5
) -> Dict[str, List[float]]:
    """
    Genera puntos muestrales discretos para graficar E(g), E'(g) y E''(g).
    Evita asíntotas verticales evaluando en [margen, C - margen].
    """
    g_start = max(0.5, margen)
    g_end = min(C - 0.5, C - margen)
    step = (g_end - g_start) / (puntos - 1)

    g_vals = [g_start + i * step for i in range(puntos)]
    e_vals = [funcion_objetivo(g, A, B, C) for g in g_vals]
    ep_vals = [primera_derivada(g, A, B, C) for g in g_vals]
    epp_vals = [segunda_derivada(g, A, B, C) for g in g_vals]

    return {
        "g": g_vals,
        "E": e_vals,
        "E_prima": ep_vals,
        "E_segunda": epp_vals,
    }


def obtener_demostracion_paso_a_paso(A: float, B: float, C: float) -> List[Dict[str, str]]:
    """
    Genera la demostración matemática formal paso a paso en español con formato LaTeX.
    Ideal para la defensa oral del proyecto ante el docente.
    """
    sqrt_A = math.sqrt(A)
    sqrt_B = math.sqrt(B)
    g_star = C * sqrt_A / (sqrt_A + sqrt_B)
    e_star = ((sqrt_A + sqrt_B) ** 2) / C

    pasos = [
        {
            "titulo": "Paso 1: Planteamiento de la Función Objetivo",
            "descripcion": (
                "Se formula el modelo didáctico de retraso total E(g), donde el tiempo verde para la Vía 1 es g "
                "y para la Vía 2 es (C - g), con parámetros positivos A y B proporcionales al flujo vehicular:"
            ),
            "latex": r"E(g) = \frac{A}{g} + \frac{B}{C - g}, \quad \text{con } g \in (0, C)"
        },
        {
            "titulo": "Paso 2: Cálculo de la Primera Derivada",
            "descripcion": (
                "Aplicando las reglas de derivación para potencias de exponente negativo (d/dg[g^{-1}] = -g^{-2}) "
                "y la regla de la cadena para (C - g)^{-1}:"
            ),
            "latex": r"E'(g) = \frac{d}{dg}\left[ A g^{-1} + B (C - g)^{-1} \right] = -\frac{A}{g^2} + \frac{B}{(C - g)^2}"
        },
        {
            "titulo": "Paso 3: Condición de Primer Orden (Puntos Críticos)",
            "descripcion": (
                "Para encontrar los puntos críticos donde la pendiente de la recta tangente es nula, "
                "se iguala la primera derivada a cero:"
            ),
            "latex": r"E'(g) = 0 \iff -\frac{A}{g^2} + \frac{B}{(C - g)^2} = 0 \iff \frac{A}{g^2} = \frac{B}{(C - g)^2}"
        },
        {
            "titulo": "Paso 4: Despeje Analítico del Punto Crítico g*",
            "descripcion": (
                "Dado que g > 0 y (C - g) > 0, extraemos la raíz cuadrada a ambos lados de la igualdad "
                "y despejamos algebraicamente la variable g:"
            ),
            "latex": (
                r"\begin{aligned} "
                r"\frac{\sqrt{A}}{g} &= \frac{\sqrt{B}}{C - g} \\ "
                r"\sqrt{A}(C - g) &= g\sqrt{B} \\ "
                r"C\sqrt{A} - g\sqrt{A} &= g\sqrt{B} \\ "
                r"g\left(\sqrt{A} + \sqrt{B}\right) &= C\sqrt{A} \\ "
                rf"g^* &= \frac{{C \sqrt{{A}}}}{{\sqrt{{A}} + \sqrt{{B}}}} \approx {g_star:.2f} \text{{ s}} "
                r"\end{aligned}"
            )
        },
        {
            "titulo": "Paso 5: Cálculo de la Segunda Derivada",
            "descripcion": (
                "Derivamos nuevamente E'(g) respecto a g para analizar la concavidad de la función objetivo:"
            ),
            "latex": (
                r"E''(g) = \frac{d}{dg}\left[ -A g^{-2} + B (C - g)^{-2} \right] = "
                r"\frac{2A}{g^3} + \frac{2B}{(C - g)^3}"
            )
        },
        {
            "titulo": "Paso 6: Criterio de la Segunda Derivada (Demostración del Mínimo)",
            "descripcion": (
                "Dado que A > 0, B > 0 y para todo g en el dominio factible (0, C) se cumple que g³ > 0 y (C - g)³ > 0, "
                "ambos sumandos son estrictamente positivos. Por tanto, E''(g) > 0 en todo el dominio:"
            ),
            "latex": (
                r"E''(g) > 0 \quad \forall g \in (0, C) \implies E''(g^*) > 0"
            )
        },
        {
            "titulo": "Paso 7: Conclusión de Convexidad y Valor Óptimo",
            "descripcion": (
                "La función E(g) es estrictamente convexa en todo el intervalo abierto (0, C). Por el Criterio "
                "de la Segunda Derivada, el punto crítico g* es un MÍNIMO GLOBAL ÚNICO. El valor mínimo de retraso es:"
            ),
            "latex": (
                rf"E(g^*) = \frac{{(\sqrt{{A}} + \sqrt{{B}})^2}}{{C}} \approx {e_star:.2f}"
            )
        }
    ]
    return pasos
