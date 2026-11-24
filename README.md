# TrafficFlow AI: Sistema Inteligente de Simulación y Optimización del Tráfico Vehicular

**Proyecto Universitario Interdisciplinario**  
- **Carrera:** Ingeniería Industrial  
- **Asignatura:** Cálculo Diferencial / Investigación de Operaciones  
- **Área:** Modelado Matemático, Optimización de Procesos e Inteligencia Artificial  
- **Idioma del Sistema:** 100% Español  

---

## 1. Descripción del Proyecto

**TrafficFlow AI** es una plataforma científica y visual diseñada para simular, analizar y optimizar los tiempos de semáforos en una intersección vehicular de dos vías. El sistema demuestra de manera práctica y rigurosa cómo el **Cálculo Diferencial** (mediante la primera y segunda derivada, análisis de puntos críticos y criterios de convexidad) y la **Inteligencia Artificial Supervisada** (algoritmos de ensamble *Random Forest* mediante *Scikit-learn*) permiten optimizar el reparto de tiempos de luz verde, reduciendo las colas de vehículos, los tiempos de espera y el impacto ambiental por emisiones en ralentí.

---

### 1.1 Nueva Ciudad Inteligente Isométrica (Visual 2.5D a 60 FPS)

El simulador principal cuenta con un motor gráfico procedural en HTML5 Canvas con perspectiva isométrica que recrea una **ciudad inteligente viva e interactiva**, inspirado fielmente en la arquitectura del centro de control urbano:
- **Intersección Central Isométrica:** Cruce de 4 cuadrantes con calzadas detalladas, pasos peatonales de cebra, líneas de detención y demarcación vial continua.
- **Entorno Arquitectónico Urbano:**
  - Edificio corporativo **"TECH CITY"** con rótulo luminoso neón y ventanas iluminadas.
  - Establecimiento **"CAFÉ"** con terraza exterior y sombrillas rojas/blancas.
  - Centro comercial **"MALL"** con zona de parqueo y vehículos estacionados.
  - Torres corporativas **"OFFICE PARK"** con textura de cristal.
  - **Parque Urbano:** Gran fuente central circular con partículas animadas de agua en suspensión continua (*spouting fountain*), árboles de cerezo en flor rosa (*Sakura*), árboles verdes, bancos y paradero de buses con cubierta translúcida.
- **Flota Vehicular Isométrica 3D Multiclase:** Sedanes, SUVs, Taxis con letrero iluminado, Autobuses de transporte público, Camionetas pick-up y Deportivos en tránsito bidireccional. Cada vehículo cuenta con sombra proyectada, ruedas, ventanas reflejantes, **faros LED con haz cónico de luz en Modo Noche** y **luces de freno traseras que se iluminan al desacelerar o detenerse**.
- **Semáforos Isométricos con Viseras, Resplandor Bloom y Temporizador Digital:** Carcasas oscuras con viseras protectoras, lentes con halo de resplandor intenso (*bloom glow*) y **placas de temporizador digital LED** que marcan la cuenta regresiva en segundos sincronizada con el movimiento vehicular.
- **Panel de Control HUD Inteligente:**
  - Tarjeta de telemetría izquierda: Conteo en tiempo real de vehículos en cola, atendidos, tiempo medio de espera y porcentaje de mejora operativa.
  - Minimapa superior derecho con radar semafórico animado en vivo.
  - Selector superior de modos de operación: **Tiempos Fijos (50/50)**, **Cálculo Diferencial ($g^*$)** e **Inteligencia Artificial (ML)**.
  - Barra inferior con medidores cromáticos de colas por acceso (Norte, Sur, Este, Oeste), recuadro con la fórmula de optimización ($g^* = \frac{C\sqrt{A}}{\sqrt{A}+\sqrt{B}}$) y botón de **+Ráfaga de Tráfico** para pruebas de estrés.
  - Conmutador interactivo de **Día / Noche**, pausa/reanudación, reinicio y aceleración a 2x/4x.

### 1.2 Traffic Intelligence Center (Dashboard Ejecutivo y Analítico)

El **Traffic Intelligence Center (TIC)** es un centro de comando y analítica estratégica diseñado para la toma de decisiones en ingeniería de tránsito e ingeniería industrial:
- **5 Indicadores Principales (KPI Cards):** Total de vehículos generados, vehículos atendidos, longitud de cola instantánea, tiempo medio de espera por conductor y **Nivel de Servicio (HCM LoS A-F)** con grado de saturación $X = \lambda / \mu$.
- **Gráficos Interactivos de Alta Precisión:**
  - Evolución temporal de colas $Q_1(t)$ y $Q_2(t)$ en vivo con áreas sombreadas.
  - Aforos y carga vehicular por acceso (Norte, Sur, Este, Oeste).
  - Comparativa de demoras entre Tiempos Fijos (50/50), Cálculo Diferencial e IA.
  - Resumen cuantitativo de reducciones porcentuales en demora y colas.
- **Análisis Matemático de Cálculo Diferencial:**
  - Trazado de la curva de retraso total $E(g) = A/g + B/(C-g)$.
  - Recta tangente horizontal $E'(g^*) = 0$ en el punto crítico óptimo $g^* = \frac{C\sqrt{A}}{\sqrt{A}+\sqrt{B}}$.
  - Comprobación analítica de la segunda derivada $E''(g^*) > 0$ (convexidad estricta y mínimo global).
- **Inteligencia Artificial Supervisada (Random Forest):**
  - Predicciones adaptativas en tiempo real y cálculo de divergencia absoluta $|g^* - g_{IA}|$.
  - Gráfico de Importancia de Variables (*Feature Importance*) para la ingeniería de tráfico.
- **Historial de Simulaciones y Escenarios:**
  - Base de datos en sesión con registro de pruebas, parámetros y resultados.
  - Carga inmediata de escenarios típicos (Hora Valle, Flujo Balanceado, Hora Pico, Sobresaturación).
  - Botón de exportación a archivo CSV para análisis posterior.

---

## 2. Estructura de Archivos del Proyecto

El repositorio está organizado de forma limpia, modular y desacoplada:

```text
TrafficFlow/
│
├── app.py                         # Aplicación principal interactiva en Streamlit (UI con 8 secciones)
├── dashboard_intelligence.py      # Traffic Intelligence Center (Dashboard ejecutivo con KPIs, LoS y análisis)
├── simulador_visual.py            # Ciudad Inteligente Isométrica 2.5D a 60 FPS (Canvas/JS)
├── simulacion.py                  # Motor híbrido de simulación continua (EDO Q'=λ-μ), vehículos bidireccionales
├── optimizacion.py                # Modelo analítico de Cálculo Diferencial, derivadas y restricciones
├── inteligencia_artificial.py     # Módulo de Machine Learning (Scikit-learn, datos sintéticos, métricas)
├── deteccion_vehiculos.py         # Módulo de visión por computadora (OpenCV MOG2, conteo por ROI)
├── comparacion.py                 # Evaluador ceteris paribus de los 3 métodos y cálculo de mejoras (%)
├── graficos.py                    # Visualizaciones interactivas en Plotly (mapa vectorial detallado, curvas, radar)
├── teoria.py                      # Contenido académico formal, variables, vínculos industriales y citas
│
├── BASE_TEORICA_TRAFFICFLOW.md    # Documento monográfico formal con marco teórico y deducciones matemáticas
├── README.md                      # Manual técnico, guía de ejecución y libreto para la exposición
├── requirements.txt               # Lista de dependencias del proyecto
├── run_app.bat                    # Script de inicio rápido para Windows
├── run_app.ps1                    # Script de inicio para PowerShell
│
├── pruebas/                       # Banco de pruebas unitarias automatizadas
│   ├── test_matematicas.py        # Validación analítica de derivadas, convexidad y puntos críticos
│   ├── test_simulacion.py         # Validación de conservación de flujo y no negatividad (Q >= 0)
│   └── test_ia.py                 # Validación de entrenamiento de IA, métricas R² y restricciones
│
└── [Documentos de Investigación Originales] (PDFs académicos conservados intactos)
```

---

## 3. Compatibilidad de Entorno y Bibliotecas

El proyecto ha sido diseñado y verificado para la versión de Python del usuario (**Python 3.15.2** de 64 bits en Windows), así como para versiones estándar de Python 3.10, 3.11 y 3.12.

### Dependencias Principales (`requirements.txt`):
- `streamlit`: Interfaz web interactiva profesional con tema oscuro y componentes reactivos.
- `plotly`: Gráficos científicos interactivos con trazado vectorial de la intersección 2D y curvas de derivadas.
- `numpy`: Cálculo matricial, evaluación de vectores de estado y operaciones de tensores.
- `scipy`: Validación numérica de optimización y funciones continuas.
- `scikit-learn`: Entrenamiento del modelo supervisado (*Random Forest Regressor*), partición 80/20 y evaluación con métricas reales ($R^2$, MAE, RMSE).
- `opencv-python`: Procesamiento digital de video, sustracción de fondo adaptativa MOG2 y seguimiento por centroides.
- `pandas`: Manejo estructurado de conjuntos de datos operacionales.
- `pillow`: Soporte de imágenes para la interfaz.

---

## 4. Instrucciones de Instalación y Ejecución en PowerShell

Para ejecutar la aplicación en su máquina Windows, siga estos sencillos pasos desde la consola de **PowerShell**:

### Paso 1: Abrir PowerShell en la carpeta del proyecto
Presione `Shift + Clic derecho` en la carpeta `TrafficFlow` y seleccione **"Abrir ventana de PowerShell aquí"** (o navegue con `cd D:\TrafficFlow`).

### Paso 2: Instalar las dependencias (si aún no las tiene)
Ejecute el siguiente comando para instalar las bibliotecas requeridas:

```powershell
pip install -r requirements.txt
```

### Paso 3: Iniciar la Aplicación TrafficFlow AI
Ejecute el comando de inicio de Streamlit:

```powershell
streamlit run app.py
```

O bien mediante el módulo de Python:

```powershell
python -m streamlit run app.py
```

También puede simplemente hacer doble clic en el archivo `run_app.bat` o ejecutar `./run_app.ps1`.

El navegador web se abrirá automáticamente en la dirección:
`http://localhost:8501`

---

## 5. Ejecución de las Pruebas Unitarias

Para comprobar la validez matemática y lógica de todo el sistema antes de la presentación, puede ejecutar las pruebas directamente desde PowerShell:

```powershell
# Probar cálculo diferencial y puntos críticos
python pruebas/test_matematicas.py

# Probar simulación vehicular y ecuación de colas
python pruebas/test_simulacion.py

# Probar modelo de inteligencia artificial
python pruebas/test_ia.py
```

Todas las pruebas deben finalizar con mensaje de éxito: `✅ Todas las pruebas pasaron exitosamente`.

---

## 6. Funcionalidades del Sistema y Estado de Operación

| Funcionalidad | Estado | Descripción Técnica |
| :--- | :---: | :--- |
| **Centro de Control y Simulación 2D** | **100% Funcional** | Animación a 60 FPS con autos realistas (ruedas, parabrisas, faros con haces de luz, luces de freno reactivas), semáforos verticales con viseras, halo bloom y temporizador digital LED, tráfico bidireccional y cambio dinámico entre Fijo, Cálculo e IA. Incluye mapa vectorial en Plotly. |
| **Dinámica de Colas (EDO)** | **100% Funcional** | Integración numérica de $Q'(t) = \lambda - \mu$ con restricción de no-negatividad $Q(t) \ge 0$ y Ley de Little. |
| **Cálculo Diferencial y Optimización** | **100% Funcional** | Deducción matemática completa paso a paso con LaTeX, cálculo de primera derivada $E'(g)$, segunda derivada $E''(g) > 0$, punto crítico analítico $g^*$ y evaluación de límites normativos $[g_{\min}, C - h_{\min}]$. |
| **Inteligencia Artificial (ML)** | **100% Funcional** | Algoritmo *Random Forest Regressor* con Scikit-learn sobre escenarios sintéticos, evaluación con $R^2$, MAE, RMSE y recomendador en vivo. |
| **Detección de Vehículos (OpenCV)** | **100% Funcional** | Sustracción de fondo MOG2 con filtro de sombras, operaciones morfológicas, seguimiento por centroides y líneas de aforo virtual (ROI). Incluye generador de video de prueba autónomo. |
| **Detección Avanzada (YOLOv8)** | *Preparado / Opcional* | El módulo cuenta con arquitectura para cargar pesos `yolov8n.onnx` si se descargan externamente en la carpeta `modelos/`. |
| **Comparación de Escenarios** | **100% Funcional** | Comparativa *ceteris paribus* entre Semáforo Fijo, Cálculo Diferencial e IA, con cálculo formal del porcentaje de mejora y gráfico de radar. |
| **Fundamentación Teórica y APA 7** | **100% Funcional** | 5 capítulos teóricos vinculados a la Ingeniería Industrial y referencias bibliográficas en formato APA 7ma edición verificadas. |

---

## 7. Guía y Libreto para la Exposición ante el Docente

Para defender el proyecto con máxima calificación ante su profesor de **Cálculo Diferencial** e **Ingeniería Industrial**, se recomienda estructurar la presentación en 4 momentos clave:

### Momento 1: Planteamiento del Problema (Ingeniería Industrial)
1. Inicie en la sección **"📚 Fundamentación Teórica"**.
2. Explique que una intersección semaforizada es análoga a un **cuello de botella** en una línea de producción donde dos flujos compiten por un recurso escaso: el tiempo de ciclo verde.
3. Mencione que el retraso vehicular genera pérdidas de productividad laboral y emisiones innecesarias de $CO_2$ durante el ralentí.

### Momento 2: El Núcleo de Cálculo Diferencial (La Clave de la Evaluación)
1. Diríjase a la sección **"🧮 Cálculo Diferencial y Optimización"**.
2. Muestre la función objetivo didáctica:
   $$E(g) = \frac{A}{g} + \frac{B}{C - g}$$
3. Explique la primera derivada:
   $$E'(g) = -\frac{A}{g^2} + \frac{B}{(C - g)^2}$$
4. Demuestre cómo al igualar $E'(g) = 0$ se obtiene el punto crítico analítico:
   $$g^* = \frac{C \sqrt{A}}{\sqrt{A} + \sqrt{B}}$$
5. Presente la segunda derivada:
   $$E''(g) = \frac{2A}{g^3} + \frac{2B}{(C - g)^3}$$
6. **Argumento contundente:** Explique por qué el criterio de la segunda derivada garantiza un mínimo: como $A>0$, $B>0$, $g>0$ y $C-g>0$, ambos términos son estrictamente positivos ($E''(g^*) > 0$), lo que prueba matemáticamente que la función es **estrictamente convexa** y el punto crítico es un **mínimo global único**.
7. Mueva los controles deslizantes interactivos para mostrar cómo la gráfica de Plotly recalcula las curvas y cómo se evalúan las restricciones cuando el punto crítico supera los límites permitidos ($[g_{\min}, C - h_{\min}]$).
8. Recuerde aclarar al docente el aviso metodológico: es un modelo didáctico formal para la demostración del cálculo diferencial.

### Momento 3: Simulación Dinámica y Modelo de Colas
1. Pase a la sección **"🚦 Simulación Interactiva"**.
2. Ejecute pasos de simulación con el botón `▶️ Avanzar Paso` o `⏩ Ciclo Completo`.
3. Muestre cómo los vehículos se acumulan en rojo y se vacían en verde siguiendo la ecuación diferencial $Q'(t) = \lambda - \mu$.

### Momento 4: Comparación Científica de Resultados (Cierre de Alto Impacto)
1. Ingrese a la sección **"📊 Comparación de Escenarios"**.
2. Muestre la tabla y el gráfico de radar comparando el semáforo convencional (tiempos fijos) frente al **Cálculo Diferencial** y la **Inteligencia Artificial**.
3. Destaque el cálculo formal de mejora:
   $$\text{Mejora (\%)} = \left(\frac{\text{Valor Inicial} - \text{Valor Optimizado}}{\text{Valor Inicial}}\right) \times 100$$
4. Concluya demostrando que la optimización matemática logra reducciones significativas en los tiempos de espera y colas vehiculares, validando la aplicación directa de la matemática en la ingeniería.
