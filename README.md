# TrafficFlow AI: Sistema Inteligente de SimulaciÃ³n y OptimizaciÃ³n del TrÃ¡fico Vehicular

**Proyecto Universitario Interdisciplinario**  
- **Carrera:** IngenierÃ­a Industrial  
- **Asignatura:** CÃ¡lculo Diferencial / InvestigaciÃ³n de Operaciones  
- **Ãrea:** Modelado MatemÃ¡tico, OptimizaciÃ³n de Procesos e Inteligencia Artificial  
- **Idioma del Sistema:** 100% EspaÃ±ol  

---

## 1. DescripciÃ³n del Proyecto

**TrafficFlow AI** es una plataforma cientÃ­fica y visual diseÃ±ada para simular, analizar y optimizar los tiempos de semÃ¡foros en una intersecciÃ³n vehicular de dos vÃ­as. El sistema demuestra de manera prÃ¡ctica y rigurosa cÃ³mo el **CÃ¡lculo Diferencial** (mediante la primera y segunda derivada, anÃ¡lisis de puntos crÃ­ticos y criterios de convexidad) y la **Inteligencia Artificial Supervisada** (algoritmos de ensamble *Random Forest* mediante *Scikit-learn*) permiten optimizar el reparto de tiempos de luz verde, reduciendo las colas de vehÃ­culos, los tiempos de espera y el impacto ambiental por emisiones en ralentÃ­.

---

### 1.1 Nueva Ciudad Inteligente IsomÃ©trica (Visual 2.5D a 60 FPS)

El simulador principal cuenta con un motor grÃ¡fico procedural en HTML5 Canvas con perspectiva isomÃ©trica que recrea una **ciudad inteligente viva e interactiva**, inspirado fielmente en la arquitectura del centro de control urbano:
- **IntersecciÃ³n Central IsomÃ©trica:** Cruce de 4 cuadrantes con calzadas detalladas, pasos peatonales de cebra, lÃ­neas de detenciÃ³n y demarcaciÃ³n vial continua.
- **Entorno ArquitectÃ³nico Urbano:**
  - Edificio corporativo **"TECH CITY"** con rÃ³tulo luminoso neÃ³n y ventanas iluminadas.
  - Establecimiento **"CAFÃ‰"** con terraza exterior y sombrillas rojas/blancas.
  - Centro comercial **"MALL"** con zona de parqueo y vehÃ­culos estacionados.
  - Torres corporativas **"OFFICE PARK"** con textura de cristal.
  - **Parque Urbano:** Gran fuente central circular con partÃ­culas animadas de agua en suspensiÃ³n continua (*spouting fountain*), Ã¡rboles de cerezo en flor rosa (*Sakura*), Ã¡rboles verdes, bancos y paradero de buses con cubierta translÃºcida.
- **Flota Vehicular IsomÃ©trica 3D Multiclase:** Sedanes, SUVs, Taxis con letrero iluminado, Autobuses de transporte pÃºblico, Camionetas pick-up y Deportivos en trÃ¡nsito bidireccional. Cada vehÃ­culo cuenta con sombra proyectada, ruedas, ventanas reflejantes, **faros LED con haz cÃ³nico de luz en Modo Noche** y **luces de freno traseras que se iluminan al desacelerar o detenerse**.
- **SemÃ¡foros IsomÃ©tricos con Viseras, Resplandor Bloom y Temporizador Digital:** Carcasas oscuras con viseras protectoras, lentes con halo de resplandor intenso (*bloom glow*) y **placas de temporizador digital LED** que marcan la cuenta regresiva en segundos sincronizada con el movimiento vehicular.
- **Panel de Control HUD Inteligente:**
  - Tarjeta de telemetrÃ­a izquierda: Conteo en tiempo real de vehÃ­culos en cola, atendidos, tiempo medio de espera y porcentaje de mejora operativa.
  - Minimapa superior derecho con radar semafÃ³rico animado en vivo.
  - Selector superior de modos de operaciÃ³n: **Tiempos Fijos (50/50)**, **CÃ¡lculo Diferencial ($g^*$)** e **Inteligencia Artificial (ML)**.
  - Barra inferior con medidores cromÃ¡ticos de colas por acceso (Norte, Sur, Este, Oeste), recuadro con la fÃ³rmula de optimizaciÃ³n ($g^* = \frac{C\sqrt{A}}{\sqrt{A}+\sqrt{B}}$) y botÃ³n de **+RÃ¡faga de TrÃ¡fico** para pruebas de estrÃ©s.
  - Conmutador interactivo de **DÃ­a / Noche**, pausa/reanudaciÃ³n, reinicio y aceleraciÃ³n a 2x/4x.

### 1.2 Traffic Intelligence Center (Dashboard Ejecutivo y AnalÃ­tico)

El **Traffic Intelligence Center (TIC)** es un centro de comando y analÃ­tica estratÃ©gica diseÃ±ado para la toma de decisiones en ingenierÃ­a de trÃ¡nsito e ingenierÃ­a industrial:
- **5 Indicadores Principales (KPI Cards):** Total de vehÃ­culos generados, vehÃ­culos atendidos, longitud de cola instantÃ¡nea, tiempo medio de espera por conductor y **Nivel de Servicio (HCM LoS A-F)** con grado de saturaciÃ³n $X = \lambda / \mu$.
- **GrÃ¡ficos Interactivos de Alta PrecisiÃ³n:**
  - EvoluciÃ³n temporal de colas $Q_1(t)$ y $Q_2(t)$ en vivo con Ã¡reas sombreadas.
  - Aforos y carga vehicular por acceso (Norte, Sur, Este, Oeste).
  - Comparativa de demoras entre Tiempos Fijos (50/50), CÃ¡lculo Diferencial e IA.
  - Resumen cuantitativo de reducciones porcentuales en demora y colas.
- **AnÃ¡lisis MatemÃ¡tico de CÃ¡lculo Diferencial:**
  - Trazado de la curva de retraso total $E(g) = A/g + B/(C-g)$.
  - Recta tangente horizontal $E'(g^*) = 0$ en el punto crÃ­tico Ã³ptimo $g^* = \frac{C\sqrt{A}}{\sqrt{A}+\sqrt{B}}$.
  - ComprobaciÃ³n analÃ­tica de la segunda derivada $E''(g^*) > 0$ (convexidad estricta y mÃ­nimo global).
- **Inteligencia Artificial Supervisada (Random Forest):**
  - Predicciones adaptativas en tiempo real y cÃ¡lculo de divergencia absoluta $|g^* - g_{IA}|$.
  - GrÃ¡fico de Importancia de Variables (*Feature Importance*) para la ingenierÃ­a de trÃ¡fico.
- **Historial de Simulaciones y Escenarios:**
  - Base de datos en sesiÃ³n con registro de pruebas, parÃ¡metros y resultados.
  - Carga inmediata de escenarios tÃ­picos (Hora Valle, Flujo Balanceado, Hora Pico, SobresaturaciÃ³n).
  - BotÃ³n de exportaciÃ³n a archivo CSV para anÃ¡lisis posterior.

---

## 2. Estructura de Archivos del Proyecto

El repositorio estÃ¡ organizado de forma limpia, modular y desacoplada:

```text
TrafficFlow/
â”‚
â”œâ”€â”€ app.py                         # AplicaciÃ³n principal interactiva en Streamlit (UI con 8 secciones)
â”œâ”€â”€ dashboard_intelligence.py      # Traffic Intelligence Center (Dashboard ejecutivo con KPIs, LoS y anÃ¡lisis)
â”œâ”€â”€ simulador_visual.py            # Ciudad Inteligente IsomÃ©trica 2.5D a 60 FPS (Canvas/JS)
â”œâ”€â”€ simulacion.py                  # Motor hÃ­brido de simulaciÃ³n continua (EDO Q'=Î»-Î¼), vehÃ­culos bidireccionales
â”œâ”€â”€ optimizacion.py                # Modelo analÃ­tico de CÃ¡lculo Diferencial, derivadas y restricciones
â”œâ”€â”€ inteligencia_artificial.py     # MÃ³dulo de Machine Learning (Scikit-learn, datos sintÃ©ticos, mÃ©tricas)
â”œâ”€â”€ deteccion_vehiculos.py         # MÃ³dulo de visiÃ³n por computadora (OpenCV MOG2, conteo por ROI)
â”œâ”€â”€ comparacion.py                 # Evaluador ceteris paribus de los 3 mÃ©todos y cÃ¡lculo de mejoras (%)
â”œâ”€â”€ graficos.py                    # Visualizaciones interactivas en Plotly (mapa vectorial detallado, curvas, radar)
â”œâ”€â”€ teoria.py                      # Contenido acadÃ©mico formal, variables, vÃ­nculos industriales y citas
â”‚
â”œâ”€â”€ BASE_TEORICA_TRAFFICFLOW.md    # Documento monogrÃ¡fico formal con marco teÃ³rico y deducciones matemÃ¡ticas
â”œâ”€â”€ README.md                      # Manual tÃ©cnico, guÃ­a de ejecuciÃ³n y libreto para la exposiciÃ³n
â”œâ”€â”€ requirements.txt               # Lista de dependencias del proyecto
â”œâ”€â”€ run_app.bat                    # Script de inicio rÃ¡pido para Windows
â”œâ”€â”€ run_app.ps1                    # Script de inicio para PowerShell
â”‚
â”œâ”€â”€ pruebas/                       # Banco de pruebas unitarias automatizadas
â”‚   â”œâ”€â”€ test_matematicas.py        # ValidaciÃ³n analÃ­tica de derivadas, convexidad y puntos crÃ­ticos
â”‚   â”œâ”€â”€ test_simulacion.py         # ValidaciÃ³n de conservaciÃ³n de flujo y no negatividad (Q >= 0)
â”‚   â””â”€â”€ test_ia.py                 # ValidaciÃ³n de entrenamiento de IA, mÃ©tricas RÂ² y restricciones
â”‚
â””â”€â”€ [Documentos de InvestigaciÃ³n Originales] (PDFs acadÃ©micos conservados intactos)
```

---

## 3. Compatibilidad de Entorno y Bibliotecas

El proyecto ha sido diseÃ±ado y verificado para la versiÃ³n de Python del usuario (**Python 3.15.2** de 64 bits en Windows), asÃ­ como para versiones estÃ¡ndar de Python 3.10, 3.11 y 3.12.

### Dependencias Principales (`requirements.txt`):
- `streamlit`: Interfaz web interactiva profesional con tema oscuro y componentes reactivos.
- `plotly`: GrÃ¡ficos cientÃ­ficos interactivos con trazado vectorial de la intersecciÃ³n 2D y curvas de derivadas.
- `numpy`: CÃ¡lculo matricial, evaluaciÃ³n de vectores de estado y operaciones de tensores.
- `scipy`: ValidaciÃ³n numÃ©rica de optimizaciÃ³n y funciones continuas.
- `scikit-learn`: Entrenamiento del modelo supervisado (*Random Forest Regressor*), particiÃ³n 80/20 y evaluaciÃ³n con mÃ©tricas reales ($R^2$, MAE, RMSE).
- `opencv-python`: Procesamiento digital de video, sustracciÃ³n de fondo adaptativa MOG2 y seguimiento por centroides.
- `pandas`: Manejo estructurado de conjuntos de datos operacionales.
- `pillow`: Soporte de imÃ¡genes para la interfaz.

---

## 4. Instrucciones de InstalaciÃ³n y EjecuciÃ³n en PowerShell

Para ejecutar la aplicaciÃ³n en su mÃ¡quina Windows, siga estos sencillos pasos desde la consola de **PowerShell**:

### Paso 1: Abrir PowerShell en la carpeta del proyecto
Presione `Shift + Clic derecho` en la carpeta `TrafficFlow` y seleccione **"Abrir ventana de PowerShell aquÃ­"** (o navegue con `cd D:\TrafficFlow`).

### Paso 2: Instalar las dependencias (si aÃºn no las tiene)
Ejecute el siguiente comando para instalar las bibliotecas requeridas:

```powershell
pip install -r requirements.txt
```

### Paso 3: Iniciar la AplicaciÃ³n TrafficFlow AI
Ejecute el comando de inicio de Streamlit:

```powershell
streamlit run app.py
```

O bien mediante el mÃ³dulo de Python:

```powershell
python -m streamlit run app.py
```

TambiÃ©n puede simplemente hacer doble clic en el archivo `run_app.bat` o ejecutar `./run_app.ps1`.

El navegador web se abrirÃ¡ automÃ¡ticamente en la direcciÃ³n:
`http://localhost:8501`

---

## 5. EjecuciÃ³n de las Pruebas Unitarias

Para comprobar la validez matemÃ¡tica y lÃ³gica de todo el sistema antes de la presentaciÃ³n, puede ejecutar las pruebas directamente desde PowerShell:

```powershell
# Probar cÃ¡lculo diferencial y puntos crÃ­ticos
python pruebas/test_matematicas.py

# Probar simulaciÃ³n vehicular y ecuaciÃ³n de colas
python pruebas/test_simulacion.py

# Probar modelo de inteligencia artificial
python pruebas/test_ia.py
```

Todas las pruebas deben finalizar con mensaje de Ã©xito: `âœ… Todas las pruebas pasaron exitosamente`.

---

## 6. Funcionalidades del Sistema y Estado de OperaciÃ³n

| Funcionalidad | Estado | DescripciÃ³n TÃ©cnica |
| :--- | :---: | :--- |
| **Centro de Control y SimulaciÃ³n 2D** | **100% Funcional** | AnimaciÃ³n a 60 FPS con autos realistas (ruedas, parabrisas, faros con haces de luz, luces de freno reactivas), semÃ¡foros verticales con viseras, halo bloom y temporizador digital LED, trÃ¡fico bidireccional y cambio dinÃ¡mico entre Fijo, CÃ¡lculo e IA. Incluye mapa vectorial en Plotly. |
| **DinÃ¡mica de Colas (EDO)** | **100% Funcional** | IntegraciÃ³n numÃ©rica de $Q'(t) = \lambda - \mu$ con restricciÃ³n de no-negatividad $Q(t) \ge 0$ y Ley de Little. |
| **CÃ¡lculo Diferencial y OptimizaciÃ³n** | **100% Funcional** | DeducciÃ³n matemÃ¡tica completa paso a paso con LaTeX, cÃ¡lculo de primera derivada $E'(g)$, segunda derivada $E''(g) > 0$, punto crÃ­tico analÃ­tico $g^*$ y evaluaciÃ³n de lÃ­mites normativos $[g_{\min}, C - h_{\min}]$. |
| **Inteligencia Artificial (ML)** | **100% Funcional** | Algoritmo *Random Forest Regressor* con Scikit-learn sobre escenarios sintÃ©ticos, evaluaciÃ³n con $R^2$, MAE, RMSE y recomendador en vivo. |
| **DetecciÃ³n de VehÃ­culos (OpenCV)** | **100% Funcional** | SustracciÃ³n de fondo MOG2 con filtro de sombras, operaciones morfolÃ³gicas, seguimiento por centroides y lÃ­neas de aforo virtual (ROI). Incluye generador de video de prueba autÃ³nomo. |
| **DetecciÃ³n Avanzada (YOLOv8)** | *Preparado / Opcional* | El mÃ³dulo cuenta con arquitectura para cargar pesos `yolov8n.onnx` si se descargan externamente en la carpeta `modelos/`. |
| **ComparaciÃ³n de Escenarios** | **100% Funcional** | Comparativa *ceteris paribus* entre SemÃ¡foro Fijo, CÃ¡lculo Diferencial e IA, con cÃ¡lculo formal del porcentaje de mejora y grÃ¡fico de radar. |
| **FundamentaciÃ³n TeÃ³rica y APA 7** | **100% Funcional** | 5 capÃ­tulos teÃ³ricos vinculados a la IngenierÃ­a Industrial y referencias bibliogrÃ¡ficas en formato APA 7ma ediciÃ³n verificadas. |

---

## 7. GuÃ­a y Libreto para la ExposiciÃ³n ante el Docente

Para defender el proyecto con mÃ¡xima calificaciÃ³n ante su profesor de **CÃ¡lculo Diferencial** e **IngenierÃ­a Industrial**, se recomienda estructurar la presentaciÃ³n en 4 momentos clave:

### Momento 1: Planteamiento del Problema (IngenierÃ­a Industrial)
1. Inicie en la secciÃ³n **"ðŸ“š FundamentaciÃ³n TeÃ³rica"**.
2. Explique que una intersecciÃ³n semaforizada es anÃ¡loga a un **cuello de botella** en una lÃ­nea de producciÃ³n donde dos flujos compiten por un recurso escaso: el tiempo de ciclo verde.
3. Mencione que el retraso vehicular genera pÃ©rdidas de productividad laboral y emisiones innecesarias de $CO_2$ durante el ralentÃ­.

### Momento 2: El NÃºcleo de CÃ¡lculo Diferencial (La Clave de la EvaluaciÃ³n)
1. DirÃ­jase a la secciÃ³n **"ðŸ§® CÃ¡lculo Diferencial y OptimizaciÃ³n"**.
2. Muestre la funciÃ³n objetivo didÃ¡ctica:
   $$E(g) = \frac{A}{g} + \frac{B}{C - g}$$
3. Explique la primera derivada:
   $$E'(g) = -\frac{A}{g^2} + \frac{B}{(C - g)^2}$$
4. Demuestre cÃ³mo al igualar $E'(g) = 0$ se obtiene el punto crÃ­tico analÃ­tico:
   $$g^* = \frac{C \sqrt{A}}{\sqrt{A} + \sqrt{B}}$$
5. Presente la segunda derivada:
   $$E''(g) = \frac{2A}{g^3} + \frac{2B}{(C - g)^3}$$
6. **Argumento contundente:** Explique por quÃ© el criterio de la segunda derivada garantiza un mÃ­nimo: como $A>0$, $B>0$, $g>0$ y $C-g>0$, ambos tÃ©rminos son estrictamente positivos ($E''(g^*) > 0$), lo que prueba matemÃ¡ticamente que la funciÃ³n es **estrictamente convexa** y el punto crÃ­tico es un **mÃ­nimo global Ãºnico**.
7. Mueva los controles deslizantes interactivos para mostrar cÃ³mo la grÃ¡fica de Plotly recalcula las curvas y cÃ³mo se evalÃºan las restricciones cuando el punto crÃ­tico supera los lÃ­mites permitidos ($[g_{\min}, C - h_{\min}]$).
8. Recuerde aclarar al docente el aviso metodolÃ³gico: es un modelo didÃ¡ctico formal para la demostraciÃ³n del cÃ¡lculo diferencial.

### Momento 3: SimulaciÃ³n DinÃ¡mica y Modelo de Colas
1. Pase a la secciÃ³n **"ðŸš¦ SimulaciÃ³n Interactiva"**.
2. Ejecute pasos de simulaciÃ³n con el botÃ³n `â–¶ï¸ Avanzar Paso` o `â© Ciclo Completo`.
3. Muestre cÃ³mo los vehÃ­culos se acumulan en rojo y se vacÃ­an en verde siguiendo la ecuaciÃ³n diferencial $Q'(t) = \lambda - \mu$.

### Momento 4: ComparaciÃ³n CientÃ­fica de Resultados (Cierre de Alto Impacto)
1. Ingrese a la secciÃ³n **"ðŸ“Š ComparaciÃ³n de Escenarios"**.
2. Muestre la tabla y el grÃ¡fico de radar comparando el semÃ¡foro convencional (tiempos fijos) frente al **CÃ¡lculo Diferencial** y la **Inteligencia Artificial**.
3. Destaque el cÃ¡lculo formal de mejora:
   $$\text{Mejora (\%)} = \left(\frac{\text{Valor Inicial} - \text{Valor Optimizado}}{\text{Valor Inicial}}\right) \times 100$$
4. Concluya demostrando que la optimizaciÃ³n matemÃ¡tica logra reducciones significativas en los tiempos de espera y colas vehiculares, validando la aplicaciÃ³n directa de la matemÃ¡tica en la ingenierÃ­a.

# TrafficFlow-AI

