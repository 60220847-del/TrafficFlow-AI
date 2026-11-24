"""
MÓDULO DE FUNDAMENTACIÓN ACADÉMICA Y MARCO TEÓRICO
=================================================
Proyecto: TrafficFlow AI
Carrera: Ingeniería Industrial
Asignatura: Cálculo Diferencial

Contiene la estructura conceptual, formulación matemática formal,
vínculos con la Ingeniería Industrial y referencias en formato APA 7ma edición.
"""

from typing import Dict, List, Any


def obtener_secciones_teoricas() -> Dict[str, Dict[str, Any]]:
    """Devuelve las secciones académicas completas para la interfaz."""
    return {
        "problema_congestion": {
            "titulo": "1. El Problema del Tráfico Urbano y la Congestión",
            "contenido": (
                "La congestión vehicular en intersecciones semaforizadas constituye uno de los desafíos más críticos "
                "de las ciudades modernas y un problema central de la **Ingeniería Industrial y de Operaciones**. "
                "Cuando la tasa de llegada de vehículos (λ) supera temporalmente la capacidad de descarga del semáforo (μ), "
                "se originan colas que crecen con el tiempo, generando tiempos muertos, consumo innecesario de combustible, "
                "aumento en las emisiones de gases de efecto invernadero (CO₂ y NOx) y estrés en los usuarios.\n\n"
                "Desde el punto de vista de la ingeniería industrial, una intersección semaforizada funciona como un "
                "**sistema de colas con servicio intermitente por fases**, donde el semáforo actúa como un despachador "
                "de capacidad restringida que distribuye el recurso escaso (tiempo de ciclo) entre demandas en conflicto."
            )
        },
        "teoria_colas_y_edo": {
            "titulo": "2. Dinámica de Colas y Ecuación Diferencial del Tráfico",
            "contenido": (
                "El modelo de fluidos continuo describe la tasa instantánea de cambio en la longitud de la cola "
                "vehicular Q(t) mediante la ecuación diferencial fundamental de conservación de flujo:\n\n"
                r"$$\frac{dQ}{dt} = Q'(t) = \lambda(t) - \mu(t), \quad \text{con } Q(t) \ge 0$$"
                "\n\n"
                "**Variables y Parámetros del Modelo:**\n"
                "- **Q(t)**: Longitud de la cola en el instante t (vehículos).\n"
                "- **λ(t)**: Tasa instantánea de llegada (vehículos/segundo).\n"
                "- **μ(t)**: Tasa instantánea de salida o servicio del semáforo (vehículos/segundo).\n\n"
                "**Condiciones de Contorno y Fases del Semáforo:**\n"
                "- **Fase Verde ($g$):** $\mu(t) = S$ (flujo de saturación, típicamente 0.5 a 0.7 veh/s por carril).\n"
                "- **Fase Amarilla ($y$):** $\mu(t) = \beta \cdot S$ (factor de vaciado parcial, $\beta \approx 0.35$).\n"
                "- **Fase Roja ($r$):** $\mu(t) = 0$ (descarga nula, la cola crece estrictamente a razón $\lambda$).\n"
                "- **Condición de No-Negatividad:** Si $Q(t) = 0$ y $\lambda(t) < \mu(t)$, entonces $Q'(t) = 0$.\n\n"
                "**Ley de Little en Ingeniería de Tráfico:**\n"
                r"$$L_q = \lambda \cdot W_q$$"
                "\nDonde $L_q$ es el número promedio de vehículos en espera y $W_q$ es el tiempo medio de demora por vehículo."
            )
        },
        "calculo_diferencial": {
            "titulo": "3. Cálculo Diferencial: Optimización Matemática del Reparto de Verde",
            "contenido": (
                "Para ilustrar de forma rigurosa la potencia del cálculo diferencial en la toma de decisiones, "
                "se formula una función objetivo didáctica de costo/demora combinada entre dos vías perpendiculares:\n\n"
                r"$$E(g) = \frac{A}{g} + \frac{B}{C - g}$$"
                "\n\n"
                "**Definición de Variables:**\n"
                "- **g**: Tiempo de luz verde para la Vía 1 ($g \in (0, C)$).\n"
                "- **C - g**: Tiempo de luz verde restante asignado a la Vía 2.\n"
                "- **C**: Duración total del ciclo disponible para ambas fases de verde.\n"
                "- **A, B**: Coeficientes positivos que representan la intensidad de demanda vehicular en las Vías 1 y 2.\n\n"
                "**Deducción Analítica del Punto Crítico:**\n"
                r"$$E'(g) = -\frac{A}{g^2} + \frac{B}{(C - g)^2}$$"
                "\nIgualando a cero ($E'(g) = 0$):\n"
                r"$$\frac{A}{g^2} = \frac{B}{(C - g)^2} \implies \frac{\sqrt{A}}{g} = \frac{\sqrt{B}}{C - g} \implies g^* = \frac{C \sqrt{A}}{\sqrt{A} + \sqrt{B}}$$"
                "\n\n"
                "**Criterio de la Segunda Derivada:**\n"
                r"$$E''(g) = \frac{2A}{g^3} + \frac{2B}{(C - g)^3} > 0 \quad \forall g \in (0, C)$$"
                "\nAl ser $E''(g^*) > 0$ estrictamente, se demuestra matemáticamente que $g^*$ corresponde a un **MÍNIMO GLOBAL ÚNICO**.\n\n"
                "**Restricciones Físicas y Operacionales:**\n"
                r"$$g_{\min} \le g \le C - h_{\min}$$"
                "\nSi $g^*$ se encuentra fuera de este intervalo cerrado, por el **Teorema de Weierstrass** y la estricta convexidad de la función, "
                "el óptimo factible se ubica exactamente en la frontera activa más cercana ($g_{\min}$ o $C - h_{\min}$)."
            )
        },
        "inteligencia_artificial": {
            "titulo": "4. Inteligencia Artificial y Aprendizaje Automático",
            "contenido": (
                "A diferencia de las reglas rígidas de temporización convencional, la Inteligencia Artificial mediante "
                "**Machine Learning supervisado (Random Forest Regressor)** permite aprender patrones no lineales "
                "complejos a partir de múltiples variables de estado:\n\n"
                "- Colas instantáneas ($Q_1, Q_2$).\n"
                "- Tasas de llegada variables en el tiempo ($\lambda_1, \lambda_2$).\n"
                "- Tiempos de espera acumulados ($W_1, W_2$).\n"
                "- Capacidad y ciclo de servicio ($S_1, S_2, C$).\n\n"
                "El modelo es entrenado con partición 80/20 y evaluado mediante métricas estadísticas reales ($R^2$, MAE, RMSE), "
                "proporcionando recomendaciones adaptativas en tiempo real que respetan los márgenes de seguridad peatonal y vehicular."
            )
        },
        "vinculo_ingenieria_industrial": {
            "titulo": "5. Relación con la Ingeniería Industrial",
            "contenido": (
                "El control semafórico optimizado es un caso de estudio paradigmático de la Ingeniería Industrial:\n\n"
                "- **Investigación de Operaciones:** Modelado matemático, programación matemática con restricciones y teoría de colas aplicada.\n"
                "- **Gestión de Procesos y Capacidad:** Eliminación de cuellos de botella (Bottleneck Management) y sincronización de flujos.\n"
                "- **Teoría de Restricciones (TOC):** Identificar la intersección crítica que limita el flujo de toda la red arterial urbana.\n"
                "- **Mejora Continua y Eficiencia Operacional:** Reducción de variabilidad, desperdicios (tiempos muertos) y costos operativos.\n"
                "- **Sostenibilidad y Huella de Carbono:** Cada segundo de reducción en la espera vehicular disminuye directamente el consumo "
                "de combustible fósil en ralentí y la emisión de contaminantes a la atmósfera."
            )
        }
    }


def obtener_referencias_apa7() -> List[Dict[str, str]]:
    """
    Retorna la lista de referencias bibliográficas en formato APA 7ma edición,
    sustentadas en los documentos de investigación reales de la carpeta.
    """
    return [
        {
            "cita": "Federal Highway Administration. (2008).",
            "referencia": (
                "Federal Highway Administration. (2008). Traffic Signal Timing Manual "
                "(Report No. FHWA-HOP-08-024). U.S. Department of Transportation. "
                "Washington, D.C."
            ),
            "tema": "Estándares internacionales de diseño de ciclos, intervalos de cambio (amarillo/rojo) y capacidad de saturación."
        },
        {
            "cita": "Baquela, E. G. (2018).",
            "referencia": (
                "Baquela, E. G. (2018). Optimización Matemática y Modelos de Decisión para la Ingeniería. "
                "Universidad Nacional Arturo Jauretche. Editorial UNAJ."
            ),
            "tema": "Fundamentos de cálculo diferencial aplicado, optimización unidimensional, condiciones de primer y segundo orden, convexidad y restricciones."
        },
        {
            "cita": "García Dunna, E., García Reyes, H., & Cárdenas Barrón, L. E. (2013).",
            "referencia": (
                "García Dunna, E., García Reyes, H., & Cárdenas Barrón, L. E. (2013). "
                "Simulación y análisis de sistemas con ProModel (2.ª ed.). Pearson Educación."
            ),
            "tema": "Metodología de simulación de eventos discretos, generación de variables aleatorias y modelos de colas en sistemas productivos y de servicio."
        },
        {
            "cita": "Coss Bu, R. (2010).",
            "referencia": (
                "Coss Bu, R. (2010). Simulación: un enfoque práctico. Editorial Limusa."
            ),
            "tema": "Modelado de líneas de espera, análisis estadístico de salidas de simulación y réplicas independientes."
        },
        {
            "cita": "Challenger-Pérez, I., Díaz-Ricardo, Y., & Becerra-García, R. A. (2014).",
            "referencia": (
                "Challenger-Pérez, I., Díaz-Ricardo, Y., & Becerra-García, R. A. (2014). "
                "El lenguaje de programación Python. Ciencias Holguín, 20(2), 1-13."
            ),
            "tema": "Capacidades computacionales de Python para la resolución de problemas de ingeniería, optimización y cálculo científico."
        },
        {
            "cita": "Little, J. D. C. (1961).",
            "referencia": (
                "Little, J. D. C. (1961). A Proof for the Queuing Formula: L = λW. "
                "Operations Research, 9(3), 383-387. https://doi.org/10.1287/opre.9.3.383"
            ),
            "tema": "Demostración matemática de la relación invariante entre el inventario en cola, la tasa de flujo y el tiempo de residencia."
        },
        {
            "cita": "Webster, F. V. (1958).",
            "referencia": (
                "Webster, F. V. (1958). Traffic Signal Settings (Road Research Technical Paper No. 39). "
                "Road Research Laboratory, HMSO. Londres."
            ),
            "tema": "Formulación clásica del retraso vehicular y optimización analítica de tiempos fijos de semáforo."
        }
    ]
