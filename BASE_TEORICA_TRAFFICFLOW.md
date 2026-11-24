# TrafficFlow AI: Sistema Inteligente de Simulación y Optimización del Tráfico Vehicular

## Fundamentación Académica, Modelado Matemático y Vínculos con la Ingeniería Industrial

**Asignatura:** Cálculo Diferencial  
**Carrera:** Ingeniería Industrial  
**Área de Conocimiento:** Optimización Matemática, Modelado de Sistemas e Inteligencia Artificial  
**Formato de Referencias:** Normas APA (7.ª edición)  

---

## Resumen Ejecutivo

El presente documento constituye la base teórica y metodológica del proyecto **TrafficFlow AI**. El proyecto integra los principios fundamentales del **Cálculo Diferencial** (derivadas, puntos críticos, criterios de optimización y análisis de convexidad), la **Teoría de Colas y Modelos de Fluidos Continuos** ($Q'(t) = \lambda - \mu$), y la **Inteligencia Artificial Supervisada** (algoritmos de ensamble mediante *Scikit-learn*) para abordar la congestión vehicular en intersecciones urbanas de dos vías.

A lo largo del documento se demuestra cómo la Ingeniería Industrial emplea herramientas matemáticas cuantitativas para resolver problemas de asignación de recursos escasos (el tiempo de ciclo semafórico), mitigar cuellos de botella y reducir el tiempo improductivo de espera, contribuyendo tanto a la eficiencia económica como a la sostenibilidad ambiental mediante la disminución de emisiones de gases contaminantes en ralentí.

---

## 1. El Problema del Tráfico Urbano y su Impacto en la Ingeniería Industrial

La rápida urbanización y el incremento en el parque automotor han provocado que las intersecciones viales se conviertan en los principales **cuellos de botella** de los sistemas de transporte. En una intersección ortogonal donde confluyen dos vías independientes, los flujos vehiculares compiten por el derecho de paso en un espacio físico compartido.

Desde la perspectiva de la **Ingeniería Industrial**, una intersección regulada por semáforos es equivalente a una estación de trabajo que atiende dos líneas de producción con demandas estocásticas variables en el tiempo. Asignar tiempos de servicio inadecuados (fases de luz verde desproporcionadas) ocasiona:

1. **Aumento de Inventario en Proceso (WIP):** Formación de extensas colas de vehículos detenidos.
2. **Desperdicio de Tiempo (Lead Time):** Demoras excesivas para los usuarios y pérdidas de productividad laboral.
3. **Consumo Ineficiente de Energía:** Mayor consumo de combustible derivado de aceleraciones y frenados repetitivos.
4. **Impacto Ambiental Negativo:** Emisiones intensivas de dióxido de carbono ($CO_2$), monóxido de carbono ($CO$) y óxidos de nitrógeno ($NO_x$) producidas durante el estado de ralentí (*idling*).

La optimización de los intervalos de verde de los semáforos representa un problema clásico de **Investigación de Operaciones** y **Optimización de Procesos**, cuyo objetivo es minimizar el retraso total acumulado del sistema sujeto a restricciones físicas y de seguridad peatonal.

---

## 2. Modelado Matemático del Flujo Vehicular y Dinámica de Colas

### 2.1 Ecuación Diferencial de Conservación de Flujo

El comportamiento dinámico de la acumulación vehicular en el acceso de una intersección se modela a través de la aproximación continua de fluidos (*Fluid Approximation*). La tasa de cambio instantánea de la longitud de la cola $Q(t)$ respecto al tiempo viene dada por la ecuación diferencial ordinaria:

$$\frac{dQ}{dt} = Q'(t) = \lambda(t) - \mu(t)$$

Donde:
- $Q(t)$: Cantidad de vehículos en cola en el instante $t$ (unidades: vehículos).
- $\lambda(t)$: Tasa instantánea de llegada de vehículos al final de la cola (unidades: vehículos/segundo).
- $\mu(t)$: Tasa instantánea de descarga o salida vehicular permitida por el semáforo (unidades: vehículos/segundo).

### 2.2 Restricción de No-Negatividad

En un sistema físico real, una cola no puede asumir valores negativos ($Q(t) \ge 0$). Por consiguiente, la ecuación diferencial gobernante adopta la siguiente forma por tramos:

$$\frac{dQ}{dt} = \begin{cases} \lambda(t) - \mu(t) & \text{si } Q(t) > 0 \text{ o } \lambda(t) \ge \mu(t) \\ 0 & \text{si } Q(t) = 0 \text{ y } \lambda(t) < \mu(t) \end{cases}$$

### 2.3 Capacidad de Descarga según las Fases Semafóricas

La tasa de atención $\mu(t)$ no es constante; depende del estado activo del semáforo:

1. **Fase Verde ($g$):** El semáforo permite el paso libre. La tasa de descarga alcanza el flujo de saturación $S$ ($\mu(t) = S$). Valores típicos oscilan entre $1800$ y $2400 \text{ veh/h}$ por carril ($0.50 \text{ a } 0.67 \text{ veh/s}$).
2. **Fase Amarilla ($y$):** Fase de cambio donde los vehículos que no pueden frenar de forma segura continúan cruzando. Se modela como una capacidad reducida $\mu(t) = \beta \cdot S$, con $\beta \approx 0.35$.
3. **Fase Roja ($r$):** Paso totalmente prohibido ($\mu(t) = 0$). Durante este intervalo, $Q'(t) = \lambda(t) > 0$, lo que implica que la cola crece de forma estrictamente monótona.

### 2.4 La Ley de Little en Sistemas Viales

De acuerdo con el teorema fundamental de colas demostrado por John D. C. Little (1961):

$$L_q = \lambda \cdot W_q$$

Donde:
- $L_q$: Longitud promedio de vehículos en espera en la cola.
- $\lambda$: Tasa promedio de llegada vehicular.
- $W_q$: Tiempo promedio de espera por vehículo.

El retraso total acumulado $D_{\text{total}}$ en un horizonte de tiempo $[0, T]$ equivale a la integral definida de la función de cola:

$$D_{\text{total}} = \int_{0}^{T} Q(t) \, dt$$

---

## 3. Demostración Rigurosa del Cálculo Diferencial en la Optimización del Reparto de Verde

### 3.1 Planteamiento del Modelo Didáctico de Optimización

Para demostrar matemáticamente la aplicación directa de las derivadas en la toma de decisiones, se formula la función objetivo didáctica de costo/retraso combinado $E(g)$ para una intersección de dos fases:

$$E(g) = \frac{A}{g} + \frac{B}{C - g}$$

Donde:
- $g$: Tiempo de luz verde asignado a la Vía 1 (variable de decisión independiente, en segundos).
- $C - g$: Tiempo de luz verde asignado a la Vía 2 (en segundos).
- $C$: Tiempo total de ciclo efectivo disponible para ambas fases ($C = g_1 + g_2$, con $C > 0$).
- $A, B$: Parámetros estrictamente positivos ($A > 0, B > 0$) proporcionales a la intensidad de demanda o flujo de llegada de las Vías 1 y 2, respectivamente.
- **Dominio:** $g \in (0, C)$.

*Nota Pedagógica:* Esta función constituye un modelo didáctico que ilustra con elegancia la optimización unidimensional mediante cálculo diferencial. Permite deducir analíticamente el comportamiento de las curvas de costo y demostrar la convexidad del problema.

---

### 3.2 Paso 1: Cálculo de la Primera Derivada $E'(g)$

Expresamos la función en términos de potencias con exponente negativo:

$$E(g) = A g^{-1} + B (C - g)^{-1}$$

Aplicando las reglas de derivación de potencias y la regla de la cadena para el segundo término $\frac{d}{dg}[(C - g)^{-1}] = -(C - g)^{-2} \cdot (-1) = (C - g)^{-2}$:

$$E'(g) = \frac{d}{dg}[A g^{-1}] + \frac{d}{dg}[B (C - g)^{-1}]$$

$$E'(g) = -A g^{-2} + B (C - g)^{-2}$$

Reescribiendo en forma fraccionaria:

$$E'(g) = -\frac{A}{g^2} + \frac{B}{(C - g)^2}$$

---

### 3.3 Paso 2: Determinación de Puntos Críticos (Condición de Primer Orden)

Los puntos críticos de una función diferenciable ocurren donde la primera derivada es igual a cero ($E'(g) = 0$):

$$-\frac{A}{g^2} + \frac{B}{(C - g)^2} = 0$$

Transponiendo términos:

$$\frac{A}{g^2} = \frac{B}{(C - g)^2}$$

Dado que $g \in (0, C)$, ambos denominadores son estrictamente positivos. Tomamos la raíz cuadrada en ambos miembros:

$$\sqrt{\frac{A}{g^2}} = \sqrt{\frac{B}{(C - g)^2}}$$

$$\frac{\sqrt{A}}{g} = \frac{\sqrt{B}}{C - g}$$

Multiplicando cruzado para resolver algebraicamente para $g$:

$$\sqrt{A}(C - g) = \sqrt{B} \cdot g$$

$$C \sqrt{A} - g\sqrt{A} = g\sqrt{B}$$

Agrupando todos los términos con la variable $g$ en el miembro derecho:

$$C \sqrt{A} = g\sqrt{A} + g\sqrt{B}$$

Factorizando $g$:

$$C \sqrt{A} = g \left(\sqrt{A} + \sqrt{B}\right)$$

Despejando el punto crítico único $g^*$:

$$g^* = \frac{C \sqrt{A}}{\sqrt{A} + \sqrt{B}}$$

---

### 3.4 Paso 3: Cálculo de la Segunda Derivada $E''(g)$

Para evaluar la naturaleza del punto crítico (máximo, mínimo o punto de inflexión), calculamos la segunda derivada derivando $E'(g) = -A g^{-2} + B (C - g)^{-2}$:

$$E''(g) = \frac{d}{dg}\left[ -A g^{-2} \right] + \frac{d}{dg}\left[ B (C - g)^{-2} \right]$$

$$E''(g) = (-A)(-2 g^{-3}) + B(-2(C - g)^{-3})(-1)$$

$$E''(g) = \frac{2A}{g^3} + \frac{2B}{(C - g)^3}$$

---

### 3.5 Paso 4: Criterio de la Segunda Derivada y Demostración del Mínimo Global

Analicemos los signos de cada componente de $E''(g)$ para cualquier valor de $g$ en el dominio abierto $(0, C)$:

1. $A > 0 \implies 2A > 0$.
2. Dado que $g > 0$, se cumple que $g^3 > 0$. Por tanto: $\frac{2A}{g^3} > 0$.
3. $B > 0 \implies 2B > 0$.
4. Dado que $g < C$, se cumple que $C - g > 0$, lo que implica $(C - g)^3 > 0$. Por tanto: $\frac{2B}{(C - g)^3} > 0$.

Como la suma de dos números estrictamente positivos es siempre estrictamente positiva:

$$E''(g) > 0 \quad \forall g \in (0, C)$$

Al evaluarlo específicamente en el punto crítico $g^*$:

$$E''(g^*) > 0$$

**Conclusión Matemática:**  
Por el **Criterio de la Segunda Derivada**, al ser $E'(g^*) = 0$ y $E''(g^*) > 0$, el punto crítico $g^*$ es un **mínimo local**.  
Más aún, como $E''(g) > 0$ en la totalidad del intervalo $(0, C)$, la función $E(g)$ es **estrictamente convexa** en todo su dominio. En consecuencia, el mínimo local $g^*$ es un **MÍNIMO GLOBAL ÚNICO**.

Sustituyendo $g^*$ en la función objetivo original, se obtiene el valor mínimo absoluto de la función:

$$E(g^*) = \frac{(\sqrt{A} + \sqrt{B})^2}{C}$$

---

### 3.6 Paso 5: Optimización con Restricciones Físicas y Operacionales

En la ingeniería de tránsito real (normativa FHWA, 2008), los tiempos de verde no pueden ser arbitrariamente pequeños debido a requerimientos de seguridad para el cruce de peatones y tiempo mínimo de vaciado de vehículos.

Se establecen las siguientes restricciones de cota inferior:
- $g \ge g_{\min}$ (Tiempo de verde mínimo para la Vía 1, típicamente $\ge 10 \text{ s}$).
- $C - g \ge h_{\min} \implies g \le C - h_{\min}$ (Tiempo de verde mínimo para la Vía 2, típicamente $\ge 10 \text{ s}$).

Por tanto, el conjunto de soluciones factibles es el intervalo cerrado y acotado:

$$\mathcal{F} = [g_{\min}, C - h_{\min}]$$

Por el **Teorema del Valor Extremo (Teorema de Weierstrass)**, una función continua sobre un conjunto compacto alcanza garantizadamente su valor mínimo absoluto. Dada la estricta convexidad de $E(g)$:

1. **Caso Interior ($g^* \in [g_{\min}, C - h_{\min}]$):**  
   El óptimo factible coincide exactamente con el punto crítico analítico:
   $$g_{\text{opt}} = g^* = \frac{C \sqrt{A}}{\sqrt{A} + \sqrt{B}}$$

2. **Caso Límite Inferior ($g^* < g_{\min}$):**  
   Como la función es estrictamente creciente para todo $g > g^*$, el menor valor admisible dentro de $\mathcal{F}$ se encuentra en el extremo inferior:
   $$g_{\text{opt}} = g_{\min}$$

3. **Caso Límite Superior ($g^* > C - h_{\min}$):**  
   Como la función es estrictamente decreciente para todo $g < g^*$, el menor valor admisible dentro de $\mathcal{F}$ se encuentra en el extremo superior:
   $$g_{\text{opt}} = C - h_{\min}$$

---

## 4. Inteligencia Artificial y Aprendizaje Automático en la Gestión del Tráfico

### 4.1 Justificación del Modelo de Machine Learning

Si bien el cálculo diferencial proporciona soluciones analíticas exactas para modelos cerrados, las condiciones operativas de una ciudad presentan una alta no linealidad y comportamiento estocástico multivariable:
- Variabilidad aleatoria en los arribos vehiculares (procesos de Poisson).
- Variación en las colas residuales de ciclos anteriores.
- Tiempos de espera heterogéneos entre accesos.

Para complementar la formulación analítica, se incorpora un módulo de **Machine Learning Supervisado** utilizando la biblioteca de código abierto *Scikit-learn*.

### 4.2 Arquitectura y Algoritmo Seleccionado

Se implementa un algoritmo de ensamble basado en árboles de decisión: **Random Forest Regressor** (Breiman, 2001). Este algoritmo ofrece:
1. Capacidad para capturar relaciones no lineales y de interacción entre variables sin imponer supuestos rígidos de distribución.
2. Alta robustez frente al sobreajuste (*overfitting*) gracias al promediado de múltiples árboles entrenados mediante submuestreo de datos (*bootstrap*) y subconjuntos aleatorios de características.
3. Evaluación intrínseca de la importancia de variables (*Feature Importance* por reducción de impureza de Gini).

### 4.3 Espacio de Características (Features) y Variable Objetivo (Target)

El vector de entrada de estado $X \in \mathbb{R}^9$ considera:
1. $Q_1$: Cola actual en la Vía 1 (vehículos).
2. $Q_2$: Cola actual en la Vía 2 (vehículos).
3. $\lambda_1$: Tasa de llegada en la Vía 1 (veh/min).
4. $\lambda_2$: Tasa de llegada en la Vía 2 (veh/min).
5. $W_1$: Tiempo de espera acumulado en la Vía 1 (segundos).
6. $W_2$: Tiempo de espera acumulado en la Vía 2 (segundos).
7. $S_1$: Flujo de saturación en la Vía 1 (veh/min).
8. $S_2$: Flujo de saturación en la Vía 2 (veh/min).
9. $C$: Tiempo de ciclo combinado ($g_1 + g_2$, segundos).

La variable objetivo a predecir es $y = g_1^*$ (tiempo de verde óptimo para la Vía 1), a partir del cual se deduce inmediatamente $g_2^* = C - g_1^*$.

### 4.4 Generación de Datos Sintéticos y Validación

Para el entrenamiento se generan conjuntos de datos sintéticos controlados mediante simulaciones matemáticas de micro-optimización de colas, abarcando escenarios de tráfico balanceado, horas pico desbalanceadas y condiciones de congestión crítica.

El conjunto de datos se divide rigurosamente en:
- **80% Entrenamiento:** Ajuste de los parámetros internos de los estimadores.
- **20% Prueba (Test):** Evaluación objetiva e insesgada sobre datos no observados.

Las métricas estadísticas calculadas para evaluar el modelo son:
- **Error Cuadrático Medio (MSE):** $\text{MSE} = \frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2$
- **Raíz del Error Cuadrático Medio (RMSE):** $\text{RMSE} = \sqrt{\text{MSE}}$
- **Error Absoluto Medio (MAE):** $\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} |y_i - \hat{y}_i|$
- **Coeficiente de Determinación ($R^2$):** $R^2 = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$

---

## 5. Detección y Aforo Vehicular Mediante Visión por Computadora (OpenCV)

Como módulo complementario para la captura automatizada de datos en campo, se incorpora un subsistema de procesamiento digital de imágenes con **OpenCV**.

### 5.1 Algoritmo de Sustracción de Fondo MOG2

El sistema utiliza la técnica de **Mixtura de Gaussianas Adaptativa (MOG2)** (`cv2.createBackgroundSubtractorMOG2`). Este método modela la probabilidad de intensidad de cada píxel de fondo como una mezcla de distribuciones normales, permitiendo:
- Adaptación dinámica a cambios lentos de iluminación ambiental.
- Filtrado efectivo de sombras proyectadas por los vehículos mediante umbralización en espacio de color.

### 5.2 Conteo por Líneas Virtuales de Región de Interés (ROI)

1. **Preprocesamiento:** Conversión a escala de grises y aplicación de filtro Gaussiano $5\times 5$ para mitigar ruido de alta frecuencia.
2. **Morfología Matemática:** Operaciones secuenciales de Cierre (*Closing*) y Apertura (*Opening*) con elemento estructurante rectangular para rellenar huecos en las siluetas vehiculares y eliminar falsos positivos pequeños.
3. **Extracción de Contornos y Centroides:** Cálculo de momentos espaciales para determinar el centroide $(\bar{x}, \bar{y})$ de cada masa vehicular que cumpla con el filtro de área mínima y máxima.
4. **Cruce de Líneas de Aforo:** Detección de intersección temporal de centroides a través de líneas virtuales ortogonales para la Vía 1 y la Vía 2, actualizando el conteo de aforo vehicular en tiempo real.

---

## 6. Comparación Metodológica y Fórmulas de Mejora

Para evaluar el impacto de las técnicas propuestas, se comparan tres filosofías de control bajo condiciones iniciales rigurosamente idénticas (*ceteris paribus*):

1. **Semáforo Convencional con Tiempos Fijos:** Reparto equitativo o empírico estático ($50\% - 50\%$).
2. **Optimización por Cálculo Diferencial:** Asignación proporcional derivada analíticamente del punto crítico $g^*$.
3. **Control Adaptativo por Inteligencia Artificial:** Recomendación multivariable en tiempo real.

El porcentaje formal de mejora en las métricas de rendimiento (espera media, cola media y retraso acumulado) se calcula mediante la fórmula estandarizada:

$$\text{Mejora (\%)} = \left(\frac{\text{Valor Inicial}_{\text{Fijo}} - \text{Valor Optimizado}}{\text{Valor Inicial}_{\text{Fijo}}}\right) \times 100$$

Un valor positivo indica una reducción efectiva del retraso o de la cola vehicular, validando la superioridad de los métodos analíticos e inteligentes frente al control estático.

---

## 7. Referencias Bibliográficas (Normas APA 7.ª Edición)

Baquela, E. G. (2018). *Optimización Matemática y Modelos de Decisión para la Ingeniería*. Universidad Nacional Arturo Jauretche. Editorial UNAJ.

Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32. https://doi.org/10.1023/A:1010933404324

Challenger-Pérez, I., Díaz-Ricardo, Y., & Becerra-García, R. A. (2014). El lenguaje de programación Python. *Ciencias Holguín*, 20(2), 1-13.

Coss Bu, R. (2010). *Simulación: un enfoque práctico*. Editorial Limusa.

Federal Highway Administration. (2008). *Traffic Signal Timing Manual* (Report No. FHWA-HOP-08-024). U.S. Department of Transportation. Washington, D.C.

García Dunna, E., García Reyes, H., & Cárdenas Barrón, L. E. (2013). *Simulación y análisis de sistemas con ProModel* (2.ª ed.). Pearson Educación.

Little, J. D. C. (1961). A Proof for the Queuing Formula: $L = \lambda W$. *Operations Research*, 9(3), 383-387. https://doi.org/10.1287/opre.9.3.383

Newell, G. F. (1982). *Applications of Queueing Theory* (2nd ed.). Chapman and Hall.

Webster, F. V. (1958). *Traffic Signal Settings* (Road Research Technical Paper No. 39). Road Research Laboratory, HMSO. Londres.
