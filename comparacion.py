"""
MÓDULO DE COMPARACIÓN DE ESCENARIOS OPERACIONALES
================================================
Proyecto: TrafficFlow AI
Carrera: Ingeniería Industrial
Asignatura: Cálculo Diferencial

Este módulo evalúa y compara el desempeño del sistema bajo 3 paradigmas de control:
1. Semáforo Convencional (Tiempos Fijos predeterminados).
2. Optimización Matemática (Cálculo Diferencial con punto crítico analítico).
3. Inteligencia Artificial (Recomendador por Machine Learning).

Garantiza condiciones iniciales idénticas (ceteris paribus) para una comparación
científicamente válida en ingeniería de tránsito.
"""

from typing import Dict, Any, List
from simulacion import SimuladorInterseccion, ConfiguracionSemaforo
from optimizacion import optimizar_tiempos_semaforo
from inteligencia_artificial import ModeloRecomendadorTraficoIA


def ejecutar_comparativa_escenarios(
    tasa_llegada_1: float = 24.0,   # veh/min
    tasa_llegada_2: float = 12.0,   # veh/min
    flujo_sat_1: float = 36.0,      # veh/min
    flujo_sat_2: float = 36.0,      # veh/min
    cola_inicial_1: int = 12,
    cola_inicial_2: int = 6,
    ciclo_total_C: float = 60.0,    # segundos de verde combinado
    duracion_simulacion: float = 180.0, # segundos totales de prueba
    g_min: float = 10.0,
    h_min: float = 10.0,
    semilla: int = 101,
    modelo_ia: ModeloRecomendadorTraficoIA = None
) -> Dict[str, Any]:
    """
    Ejecuta 3 simulaciones independientes con condiciones iniciales exactamente iguales:
    - Escenario 1: Tiempos Fijos (Reparto 50% / 50% = C/2 para cada vía)
    - Escenario 2: Cálculo Diferencial (g* derivado de la función E(g) = A/g + B/(C-g))
    - Escenario 3: Inteligencia Artificial (Recomendación supervisada entrenada)
    
    Retorna métricas comparativas detalladas y cálculo formal de porcentajes de mejora.
    """

    # 1. Configuración de tiempos para cada método
    # ---------------------------------------------
    # Método 1: Tiempos Fijos (Reparto equitativo 50% - 50%)
    g1_fijo = ciclo_total_C / 2.0
    g2_fijo = ciclo_total_C - g1_fijo

    # Método 2: Cálculo Diferencial
    # Parámetros A y B proporcionales al volumen de llegada de cada vía
    res_opt = optimizar_tiempos_semaforo(
        A=tasa_llegada_1,
        B=tasa_llegada_2,
        C=ciclo_total_C,
        g_min=g_min,
        h_min=h_min
    )
    g1_calculo = res_opt["g_optimo"]
    g2_calculo = res_opt["g2_optimo"]

    # Método 3: Inteligencia Artificial
    if modelo_ia is None:
        modelo_ia = ModeloRecomendadorTraficoIA()
        modelo_ia.entrenar(num_muestras=1200, semilla=semilla)

    res_ia = modelo_ia.predecir_tiempos_optimos(
        cola_v1=float(cola_inicial_1),
        cola_v2=float(cola_inicial_2),
        lambda_v1=tasa_llegada_1,
        lambda_v2=tasa_llegada_2,
        espera_v1=float(cola_inicial_1) / max(0.1, tasa_llegada_1 / 60.0),
        espera_v2=float(cola_inicial_2) / max(0.1, tasa_llegada_2 / 60.0),
        flujo_sat_1=flujo_sat_1,
        flujo_sat_2=flujo_sat_2,
        ciclo_total_C=ciclo_total_C,
        g_min=g_min,
        h_min=h_min
    )
    g1_ia = res_ia["g1_recomendado"]
    g2_ia = res_ia["g2_recomendado"]

    # 2. Ejecutar Simulación 1: Tiempos Fijos
    sim_fijo = SimuladorInterseccion(
        config_semaforo=ConfiguracionSemaforo(
            tiempo_verde_1=g1_fijo,
            tiempo_verde_2=g2_fijo,
            tiempo_amarillo_1=3.0,
            tiempo_amarillo_2=3.0,
            tiempo_todo_rojo=1.0
        ),
        tasa_llegada_1=tasa_llegada_1,
        tasa_llegada_2=tasa_llegada_2,
        flujo_saturacion_1=flujo_sat_1,
        flujo_saturacion_2=flujo_sat_2,
        cola_inicial_1=cola_inicial_1,
        cola_inicial_2=cola_inicial_2,
        es_estocastico=False,  # Comparación determinista rigurosa
        semilla=semilla
    )
    metricas_fijo = sim_fijo.simular_horizonte(duracion_simulacion)

    # 3. Ejecutar Simulación 2: Cálculo Diferencial
    sim_calculo = SimuladorInterseccion(
        config_semaforo=ConfiguracionSemaforo(
            tiempo_verde_1=g1_calculo,
            tiempo_verde_2=g2_calculo,
            tiempo_amarillo_1=3.0,
            tiempo_amarillo_2=3.0,
            tiempo_todo_rojo=1.0
        ),
        tasa_llegada_1=tasa_llegada_1,
        tasa_llegada_2=tasa_llegada_2,
        flujo_saturacion_1=flujo_sat_1,
        flujo_saturacion_2=flujo_sat_2,
        cola_inicial_1=cola_inicial_1,
        cola_inicial_2=cola_inicial_2,
        es_estocastico=False,
        semilla=semilla
    )
    metricas_calculo = sim_calculo.simular_horizonte(duracion_simulacion)

    # 4. Ejecutar Simulación 3: Inteligencia Artificial
    sim_ia = SimuladorInterseccion(
        config_semaforo=ConfiguracionSemaforo(
            tiempo_verde_1=g1_ia,
            tiempo_verde_2=g2_ia,
            tiempo_amarillo_1=3.0,
            tiempo_amarillo_2=3.0,
            tiempo_todo_rojo=1.0
        ),
        tasa_llegada_1=tasa_llegada_1,
        tasa_llegada_2=tasa_llegada_2,
        flujo_saturacion_1=flujo_sat_1,
        flujo_saturacion_2=flujo_sat_2,
        cola_inicial_1=cola_inicial_1,
        cola_inicial_2=cola_inicial_2,
        es_estocastico=False,
        semilla=semilla
    )
    metricas_ia = sim_ia.simular_horizonte(duracion_simulacion)

    # 5. Cálculo formal de porcentajes de mejora
    # Mejora (%) = ((Valor Inicial - Valor Optimizado) / Valor Inicial) * 100
    def calcular_mejora(inicial: float, optimizado: float, menor_es_mejor: bool = True) -> float:
        if abs(inicial) < 1e-6:
            return 0.0
        if menor_es_mejor:
            return ((inicial - optimizado) / inicial) * 100.0
        else:
            return ((optimizado - inicial) / inicial) * 100.0

    # Mejoras del Cálculo Diferencial respecto al Fijo
    mejora_espera_calc = calcular_mejora(
        metricas_fijo["espera_promedio_global"],
        metricas_calculo["espera_promedio_global"],
        menor_es_mejor=True
    )
    mejora_cola_calc = calcular_mejora(
        metricas_fijo["cola_promedio_total"],
        metricas_calculo["cola_promedio_total"],
        menor_es_mejor=True
    )
    mejora_retraso_calc = calcular_mejora(
        metricas_fijo["retraso_total_acumulado"],
        metricas_calculo["retraso_total_acumulado"],
        menor_es_mejor=True
    )

    # Mejoras de la Inteligencia Artificial respecto al Fijo
    mejora_espera_ia = calcular_mejora(
        metricas_fijo["espera_promedio_global"],
        metricas_ia["espera_promedio_global"],
        menor_es_mejor=True
    )
    mejora_cola_ia = calcular_mejora(
        metricas_fijo["cola_promedio_total"],
        metricas_ia["cola_promedio_total"],
        menor_es_mejor=True
    )
    mejora_retraso_ia = calcular_mejora(
        metricas_fijo["retraso_total_acumulado"],
        metricas_ia["retraso_total_acumulado"],
        menor_es_mejor=True
    )

    return {
        "configuracion": {
            "tasa_llegada_1": tasa_llegada_1,
            "tasa_llegada_2": tasa_llegada_2,
            "cola_inicial_1": cola_inicial_1,
            "cola_inicial_2": cola_inicial_2,
            "ciclo_total_C": ciclo_total_C,
            "duracion_simulacion": duracion_simulacion
        },
        "tiempos_verde": {
            "fijo": {"g1": g1_fijo, "g2": g2_fijo},
            "calculo": {"g1": g1_calculo, "g2": g2_calculo},
            "ia": {"g1": g1_ia, "g2": g2_ia}
        },
        "metricas": {
            "fijo": metricas_fijo,
            "calculo": metricas_calculo,
            "ia": metricas_ia
        },
        "mejoras_calculo_vs_fijo": {
            "espera_pct": round(mejora_espera_calc, 2),
            "cola_pct": round(mejora_cola_calc, 2),
            "retraso_pct": round(mejora_retraso_calc, 2)
        },
        "mejoras_ia_vs_fijo": {
            "espera_pct": round(mejora_espera_ia, 2),
            "cola_pct": round(mejora_cola_ia, 2),
            "retraso_pct": round(mejora_retraso_ia, 2)
        },
        "series_temporales": {
            "tiempo": sim_fijo.historial["tiempo"],
            "cola1_fijo": sim_fijo.historial["cola_1"],
            "cola2_fijo": sim_fijo.historial["cola_2"],
            "cola1_calc": sim_calculo.historial["cola_1"],
            "cola2_calc": sim_calculo.historial["cola_2"],
            "cola1_ia": sim_ia.historial["cola_1"],
            "cola2_ia": sim_ia.historial["cola_2"],
        }
    }
