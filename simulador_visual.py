"""
MÓDULO DE SIMULACIÓN VISUAL AVANZADA: CIUDAD INTELIGENTE ISOMÉTRICA (TRAFFICFLOW AI)
==================================================================================
Proyecto: TrafficFlow AI
Carrera: Ingeniería Industrial | Asignatura: Cálculo Diferencial

Renderiza un simulador de tráfico urbano en perspectiva ISOMÉTRICA 2.5D a 60 FPS con:
- Proyección isométrica formal 2:1 (Eje X: Noroeste-Sureste, Eje Y: Noreste-Suroeste).
- Separación geométrica estricta: Calzadas, veredas con bordillos 3D y 4 manzanas urbanas.
- Cola unificada de renderizado con ordenamiento por profundidad (Z-sorting por x + y)
  para eliminar de raíz cualquier superposición incorrecta de vehículos sobre edificios.
- Arquitectura urbana realista: Torre empresarial "TECH TOWER", Mall comercial con
  estacionamiento y vehículos aparcados, Café Bistro con terraza exterior y sombrillas,
  y Gran Parque Urbano con fuente de agua animada (física de partículas), cerezos sakura y gazebo.
- Vehículos isométricos 3D proporcionados (Sedanes, SUVs, Taxis, Buses urbanos, Pickups, Deportivos)
  con sombras proyectadas, faros LED en Modo Noche y luces de freno reactivas.
- Semáforos verticales isométricos sobre las veredas con viseras, resplandor bloom y
  temporizador digital LED con cuenta regresiva en segundos.
- Panel de control HUD: telemetría en tiempo real, minimapa dinámico, medidores de colas
  por acceso y caja de fórmula analítica g* = C√A / (√A + √B).
- Modos operativos: Tiempos Fijos (50/50), Cálculo Diferencial (g*) e Inteligencia Artificial (ML).
"""

import json
from typing import Dict, Any, Optional


def generar_componente_simulador_html(
    tiempo_verde_1: float = 30.0,
    tiempo_verde_2: float = 30.0,
    tiempo_amarillo: float = 3.0,
    tiempo_todo_rojo: float = 1.0,
    lambda_1: float = 22.0,
    lambda_2: float = 14.0,
    g_calculo: float = 34.5,
    g_ia: float = 33.0,
    ciclo_C: float = 60.0,
    modo_inicial: str = "calculo"
) -> str:
    """
    Genera el código HTML5 / Canvas / JavaScript para renderizar la Ciudad Inteligente Isométrica
    a 60 FPS con enlace directo a los modelos matemáticos y de IA de TrafficFlow.
    """

    config_json = json.dumps({
        "g1_fijo": float(tiempo_verde_1),
        "g2_fijo": float(tiempo_verde_2),
        "g1_calc": float(g_calculo),
        "g2_calc": float(max(10.0, ciclo_C - g_calculo)),
        "g1_ia": float(g_ia),
        "g2_ia": float(max(10.0, ciclo_C - g_ia)),
        "amarillo": float(tiempo_amarillo),
        "todo_rojo": float(tiempo_todo_rojo),
        "lambda_1": float(lambda_1),
        "lambda_2": float(lambda_2),
        "ciclo_C": float(ciclo_C),
        "modo_inicial": modo_inicial
    })

    html_code = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
                user-select: none;
            }}
            body {{
                background-color: #060B14;
                color: #E2E8F0;
                overflow: hidden;
            }}
            #city-command-center {{
                position: relative;
                width: 100%;
                background: #080E1A;
                border: 1px solid #1E293B;
                border-radius: 14px;
                overflow: hidden;
                box-shadow: 0 12px 40px rgba(0,0,0,0.8);
            }}

            /* BARRA SUPERIOR (HEADER) */
            .hud-topbar {{
                position: absolute;
                top: 12px;
                left: 12px;
                right: 12px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                z-index: 20;
                pointer-events: none;
                flex-wrap: wrap;
                gap: 8px;
            }}
            .brand-badge {{
                pointer-events: auto;
                display: flex;
                align-items: center;
                gap: 10px;
                background: rgba(10, 17, 30, 0.90);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(0, 229, 255, 0.3);
                padding: 7px 14px;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0, 229, 255, 0.15);
            }}
            .brand-icon {{
                font-size: 1.35rem;
                filter: drop-shadow(0 0 6px #00E5FF);
            }}
            .brand-text h1 {{
                font-size: 1.0rem;
                font-weight: 800;
                letter-spacing: 0.5px;
                background: linear-gradient(90deg, #FFFFFF, #00E5FF);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .brand-text p {{
                font-size: 0.65rem;
                color: #94A3B8;
                font-weight: 500;
            }}
            .sys-status {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 0.7rem;
                color: #00E676;
                font-weight: 700;
                border-left: 1px solid #334155;
                padding-left: 10px;
                margin-left: 4px;
            }}
            .dot-pulse {{
                width: 7px;
                height: 7px;
                background: #00E676;
                border-radius: 50%;
                box-shadow: 0 0 8px #00E676;
                animation: pulse 1.4s infinite;
            }}
            @keyframes pulse {{
                0% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.4; transform: scale(1.3); }}
                100% {{ opacity: 1; transform: scale(1); }}
            }}

            /* SELECTOR DE MODOS */
            .mode-selector {{
                pointer-events: auto;
                display: flex;
                background: rgba(15, 23, 42, 0.92);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(51, 65, 85, 0.85);
                border-radius: 10px;
                padding: 4px;
                gap: 4px;
            }}
            .mode-pill {{
                background: transparent;
                border: none;
                color: #94A3B8;
                padding: 6px 12px;
                font-size: 0.75rem;
                font-weight: 700;
                border-radius: 7px;
                cursor: pointer;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .mode-pill:hover {{
                color: #FFFFFF;
                background: rgba(255, 255, 255, 0.05);
            }}
            .mode-pill.active.fijo {{
                background: #2563EB;
                color: #FFFFFF;
                box-shadow: 0 0 12px rgba(37, 99, 235, 0.5);
            }}
            .mode-pill.active.calc {{
                background: linear-gradient(135deg, #0284C7, #00E5FF);
                color: #060B14;
                box-shadow: 0 0 14px rgba(0, 229, 255, 0.5);
            }}
            .mode-pill.active.ia {{
                background: linear-gradient(135deg, #059669, #00E676);
                color: #060B14;
                box-shadow: 0 0 14px rgba(0, 230, 118, 0.5);
            }}

            /* HERRAMIENTAS SUPERIORES */
            .tools-box {{
                pointer-events: auto;
                display: flex;
                align-items: center;
                gap: 6px;
                background: rgba(15, 23, 42, 0.92);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(51, 65, 85, 0.85);
                border-radius: 10px;
                padding: 4px 8px;
            }}
            .tool-btn {{
                background: transparent;
                border: none;
                color: #CBD5E1;
                padding: 5px 8px;
                font-size: 0.75rem;
                font-weight: 600;
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.15s;
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            .tool-btn:hover {{
                background: rgba(255, 255, 255, 0.1);
                color: #00E5FF;
            }}

            /* TARJETA DE TELEMETRÍA LATERAL IZQUIERDA */
            .hud-leftcard {{
                position: absolute;
                top: 72px;
                left: 14px;
                z-index: 20;
                width: 178px;
                background: rgba(10, 17, 30, 0.88);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(0, 229, 255, 0.28);
                border-radius: 12px;
                padding: 12px 14px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.65);
                display: flex;
                flex-direction: column;
                gap: 10px;
                pointer-events: none;
            }}
            .stat-row {{
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .stat-icon {{
                font-size: 1.15rem;
                opacity: 0.9;
            }}
            .stat-data {{
                display: flex;
                flex-direction: column;
            }}
            .stat-label {{
                font-size: 0.62rem;
                color: #94A3B8;
                text-transform: uppercase;
                letter-spacing: 0.4px;
                font-weight: 600;
            }}
            .stat-val {{
                font-size: 1.05rem;
                font-weight: 800;
                color: #F8FAFC;
                line-height: 1.2;
            }}
            .stat-sub {{
                font-size: 0.58rem;
                color: #64748B;
            }}

            /* MINIMAPA SUPERIOR DERECHO */
            .hud-minimap {{
                position: absolute;
                top: 72px;
                right: 14px;
                z-index: 20;
                width: 132px;
                height: 132px;
                background: rgba(10, 17, 30, 0.88);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(0, 229, 255, 0.28);
                border-radius: 12px;
                padding: 8px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.65);
                display: flex;
                flex-direction: column;
                align-items: center;
                pointer-events: none;
            }}
            .minimap-title {{
                font-size: 0.62rem;
                color: #00E5FF;
                font-weight: 700;
                margin-bottom: 4px;
                display: flex;
                align-items: center;
                gap: 4px;
            }}
            #minimapCanvas {{
                width: 100px;
                height: 100px;
            }}

            /* BARRA INFERIOR DE COLAS Y FÓRMULA MATEMÁTICA */
            .hud-bottombar {{
                position: absolute;
                bottom: 12px;
                left: 12px;
                right: 12px;
                z-index: 20;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 10px;
                pointer-events: none;
                flex-wrap: wrap;
            }}
            .queue-meters {{
                display: flex;
                gap: 8px;
                background: rgba(10, 17, 30, 0.90);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(51, 65, 85, 0.85);
                border-radius: 10px;
                padding: 8px 12px;
            }}
            .q-box {{
                display: flex;
                flex-direction: column;
                gap: 3px;
                min-width: 75px;
            }}
            .q-lbl {{
                font-size: 0.62rem;
                color: #94A3B8;
                font-weight: 600;
            }}
            .q-val {{
                font-size: 0.88rem;
                font-weight: 800;
                color: #F8FAFC;
            }}
            .q-bar {{
                width: 100%;
                height: 4px;
                background: #1E293B;
                border-radius: 2px;
                overflow: hidden;
            }}
            .q-fill {{
                height: 100%;
                width: 30%;
                border-radius: 2px;
                transition: width 0.3s;
            }}

            /* CAJA DE FÓRMULA DE OPTIMIZACIÓN */
            .formula-callout {{
                display: flex;
                align-items: center;
                gap: 12px;
                background: rgba(10, 17, 30, 0.90);
                backdrop-filter: blur(12px);
                border: 1px solid rgba(0, 229, 255, 0.35);
                border-radius: 10px;
                padding: 8px 16px;
                box-shadow: 0 4px 15px rgba(0, 229, 255, 0.1);
            }}
            .formula-math {{
                font-size: 0.95rem;
                font-weight: 700;
                color: #00E5FF;
                letter-spacing: 0.5px;
                font-family: 'Cambria Math', 'Georgia', serif;
            }}
            .formula-stat {{
                display: flex;
                flex-direction: column;
                border-left: 1px solid #334155;
                padding-left: 10px;
            }}
            .f-lbl {{
                font-size: 0.62rem;
                color: #94A3B8;
                text-transform: uppercase;
            }}
            .f-val {{
                font-size: 0.95rem;
                font-weight: 800;
                color: #F8FAFC;
            }}

            /* BOTÓN RÁFAGA DE TRÁFICO */
            .btn-burst {{
                pointer-events: auto;
                background: linear-gradient(135deg, #2563EB, #0284C7);
                border: 1px solid #38BDF8;
                color: #FFFFFF;
                font-size: 0.78rem;
                font-weight: 700;
                padding: 10px 16px;
                border-radius: 10px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
                display: flex;
                align-items: center;
                gap: 6px;
                transition: transform 0.15s, box-shadow 0.15s;
            }}
            .btn-burst:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6);
            }}
            .btn-burst:active {{
                transform: translateY(0);
            }}

            /* LIENZO PRINCIPAL */
            #isometricCanvas {{
                display: block;
                width: 100%;
                height: 640px;
                cursor: grab;
            }}
        </style>
    </head>
    <body>
        <div id="city-command-center">
            <!-- BARRA SUPERIOR -->
            <div class="hud-topbar">
                <div class="brand-badge">
                    <span class="brand-icon">🚗</span>
                    <div class="brand-text">
                        <h1>TrafficFlow AI</h1>
                        <p>Ciudad Inteligente Isométrica 2.5D</p>
                    </div>
                    <div class="sys-status">
                        <div class="dot-pulse"></div>
                        <span>SISTEMA EN LÍNEA</span>
                        <span style="color:#64748B; margin-left:4px;" id="sim-clock">14:37:25</span>
                    </div>
                </div>

                <div class="mode-selector">
                    <button class="mode-pill fijo" id="btn-fijo" onclick="setModo('fijo')">
                        ⏱️ Tiempos Fijos (50/50)
                    </button>
                    <button class="mode-pill calc active" id="btn-calc" onclick="setModo('calculo')">
                        ∑ Cálculo Diferencial (g*)
                    </button>
                    <button class="mode-pill ia" id="btn-ia" onclick="setModo('ia')">
                        🤖 Inteligencia Artificial (ML)
                    </button>
                </div>

                <div class="tools-box">
                    <button class="tool-btn" id="btn-time-mode" onclick="toggleDiaNoche()">
                        🌙 Noche
                    </button>
                    <button class="tool-btn" id="btn-play-pause" onclick="togglePlayPause()">
                        ⏸️
                    </button>
                    <button class="tool-btn" onclick="reiniciarSimulacion()">
                        🔄
                    </button>
                    <button class="tool-btn" id="btn-speed" onclick="toggleVelocidad()">
                        1x
                    </button>
                </div>
            </div>

            <!-- TARJETA LATERAL IZQUIERDA -->
            <div class="hud-leftcard">
                <div class="stat-row">
                    <span class="stat-icon">🚗</span>
                    <div class="stat-data">
                        <span class="stat-label">Vehículos en Cola</span>
                        <span class="stat-val" id="hud-cola-total">0</span>
                    </div>
                </div>
                <div class="stat-row">
                    <span class="stat-icon">🏁</span>
                    <div class="stat-data">
                        <span class="stat-label">Vehículos Atendidos</span>
                        <span class="stat-val" id="hud-atendidos">0</span>
                    </div>
                </div>
                <div class="stat-row">
                    <span class="stat-icon">⏱️</span>
                    <div class="stat-data">
                        <span class="stat-label">Tiempo Promedio</span>
                        <span class="stat-val" id="hud-espera">0.0 s</span>
                    </div>
                </div>
                <div class="stat-row">
                    <span class="stat-icon">📈</span>
                    <div class="stat-data">
                        <span class="stat-label">Mejora Operativa</span>
                        <span class="stat-val" style="color:#00E676;" id="hud-mejora">+31.2%</span>
                        <span class="stat-sub">Reducción de demora</span>
                    </div>
                </div>
            </div>

            <!-- MINIMAPA DE INTERSECCIÓN -->
            <div class="hud-minimap">
                <div class="minimap-title">
                    <span>🧭</span> Radar Semáforos
                </div>
                <canvas id="minimapCanvas" width="100" height="100"></canvas>
            </div>

            <!-- LIENZO ISOMÉTRICO 3D -->
            <canvas id="isometricCanvas"></canvas>

            <!-- BARRA INFERIOR DE ESTADO Y OPTIMIZACIÓN -->
            <div class="hud-bottombar">
                <div class="queue-meters">
                    <div class="q-box">
                        <span class="q-lbl">Cola Norte (V1)</span>
                        <span class="q-val" id="q-norte">0 veh</span>
                        <div class="q-bar"><div class="q-fill" id="bar-norte" style="background:#00E5FF; width:15%;"></div></div>
                    </div>
                    <div class="q-box">
                        <span class="q-lbl">Cola Sur (V1)</span>
                        <span class="q-val" id="q-sur">0 veh</span>
                        <div class="q-bar"><div class="q-fill" id="bar-sur" style="background:#F97316; width:15%;"></div></div>
                    </div>
                    <div class="q-box">
                        <span class="q-lbl">Cola Este (V2)</span>
                        <span class="q-val" id="q-este">0 veh</span>
                        <div class="q-bar"><div class="q-fill" id="bar-este" style="background:#00E676; width:15%;"></div></div>
                    </div>
                    <div class="q-box">
                        <span class="q-lbl">Cola Oeste (V2)</span>
                        <span class="q-val" id="q-oeste">0 veh</span>
                        <div class="q-bar"><div class="q-fill" id="bar-oeste" style="background:#A855F7; width:15%;"></div></div>
                    </div>
                </div>

                <div class="formula-callout">
                    <div class="formula-math">
                        g* = (C · √A) / (√A + √B)
                    </div>
                    <div class="formula-stat">
                        <span class="f-lbl">Tiempo Óptimo</span>
                        <span class="f-val" id="hud-g-star">34.5 s</span>
                    </div>
                </div>

                <button class="btn-burst" onclick="inyectarRafaga()">
                    <span>🚗</span> +Ráfaga de Tráfico
                </button>
            </div>
        </div>

        <script>
            // =================================================================
            // CONFIGURACIÓN MATEMÁTICA Y PARÁMETROS GLOBALES
            // =================================================================
            const CONFIG = {config_json};

            const canvas = document.getElementById('isometricCanvas');
            const ctx = canvas.getContext('2d');
            const minimapCanvas = document.getElementById('minimapCanvas');
            const miniCtx = minimapCanvas.getContext('2d');

            function resizeCanvas() {{
                const rect = canvas.getBoundingClientRect();
                canvas.width = rect.width * window.devicePixelRatio;
                canvas.height = rect.height * window.devicePixelRatio;
                ctx.setTransform(1, 0, 0, 1, 0, 0);
                ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
            }}
            window.addEventListener('resize', resizeCanvas);
            resizeCanvas();

            // Estado de simulación
            let simulando = true;
            let velocidad = 1.0;
            let esNoche = false; // Modo Día por defecto (fiel a la referencia)
            let modoControl = CONFIG.modo_inicial || 'calculo';

            let g1_duracion = CONFIG.g1_calc;
            let g2_duracion = CONFIG.g2_calc;
            let tiempoAmarillo = CONFIG.amarillo;
            let tiempoTodoRojo = CONFIG.todo_rojo;

            // Fases: 0: Verde V1, 1: Amarillo V1, 2: Todo Rojo 1, 3: Verde V2, 4: Amarillo V2, 5: Todo Rojo 2
            let faseActual = 0;
            let tiempoEnFase = 0.0;
            let tiempoTotalSimulado = 0.0;

            let vehiculosAtendidos = 0;
            let sumaTiemposEspera = 0;
            let contadorVehiculos = 0;

            // =================================================================
            // MOTOR DE PROYECCIÓN ISOMÉTRICA FORMAL 2:1 (DIMÉTRICA)
            // =================================================================
            // Eje X: Noroeste -> Sureste (Down-Right: +cos30, +sin30)
            // Eje Y: Noreste  -> Suroeste (Down-Left:  -cos30, +sin30)
            // Eje Z: Altura vertical      (Straight Up: -z)
            // Profundidad de ordenamiento (Z-sorting depth): D = x + y
            const cos30 = 0.8660254; // cos(30 deg)
            const sin30 = 0.5000000; // sin(30 deg)
            const S = 0.94;          // Escala global uniforme

            function iso(x, y, z = 0) {{
                const w = canvas.getBoundingClientRect().width;
                const h = canvas.getBoundingClientRect().height;
                const ox = w / 2;
                const oy = h / 2 - 20;

                const sx = ox + (x - y) * cos30 * S;
                const sy = oy + (x + y) * sin30 * S - z * S;
                return {{ x: sx, y: sy }};
            }}

            // Geometría urbana estricta
            const W_ROAD = 40;       // Semiancho de calzada (Total vía = 80 unidades)
            const W_WALK = 16;       // Ancho de vereda peatonal
            const BOUND_BLOCK = 56;  // Inicio de manzana urbana (|x| >= 56 y |y| >= 56)
            const MAP_LIM = 280;     // Límite visible del mapa

            // =================================================================
            // FLOTA VEHICULAR MULTICLASE Y COLORES REALISTAS
            // =================================================================
            const TIPOS_VEHICULOS = [
                {{ tipo: 'Sedán',    largo: 19, ancho: 9.5, alto: 7.5, peso: 0.35 }},
                {{ tipo: 'SUV',      largo: 21, ancho: 10.5, alto: 9.5, peso: 0.25 }},
                {{ tipo: 'Taxi',     largo: 19, ancho: 9.5, alto: 7.5, peso: 0.15 }},
                {{ tipo: 'Bus',      largo: 36, ancho: 11.0, alto: 13.0, peso: 0.10 }},
                {{ tipo: 'Camioneta',largo: 22, ancho: 10.5, alto: 8.5, peso: 0.10 }},
                {{ tipo: 'Deportivo',largo: 20, ancho: 10.0, alto: 6.5, peso: 0.05 }}
            ];

            const COLORES_AUTOS = [
                '#DC2626', '#2563EB', '#F8FAFC', '#1E293B', '#475569',
                '#0284C7', '#16A34A', '#E11D48', '#D97706', '#9333EA'
            ];

            let vehiculos = [];

            class VehiculoIsometrico {{
                constructor(via, dir, carril) {{
                    this.id = ++contadorVehiculos;
                    this.via = via;       // 1: Avenida 1 (Eje X: NW-SE), 2: Avenida 2 (Eje Y: NE-SW)
                    this.dir = dir;       // 1: Sentido positivo (+x o +y), -1: Sentido negativo (-x o -y)
                    this.carril = carril; // 0: Interior (cerca a la línea central), 1: Exterior (cerca a la acera)

                    // Seleccionar clase
                    const r = Math.random();
                    let acum = 0;
                    this.tipoData = TIPOS_VEHICULOS[0];
                    for (let t of TIPOS_VEHICULOS) {{
                        acum += t.peso;
                        if (r <= acum) {{
                            this.tipoData = t;
                            break;
                        }}
                    }}

                    this.tipo = this.tipoData.tipo;
                    this.largo = this.tipoData.largo;
                    this.ancho = this.tipoData.ancho;
                    this.alto = this.tipoData.alto;

                    if (this.tipo === 'Taxi') this.color = '#F59E0B';
                    else if (this.tipo === 'Bus') this.color = '#0284C7';
                    else this.color = COLORES_AUTOS[Math.floor(Math.random() * COLORES_AUTOS.length)];

                    this.tiempoLlegada = tiempoTotalSimulado;
                    this.velocidadMaxima = (this.tipo === 'Bus') ? 1.6 : (2.2 + Math.random() * 0.5);
                    this.velocidad = this.velocidadMaxima;
                    this.frenando = false;

                    // Posicionamiento riguroso estrictamente dentro de los carriles:
                    // Calzada: [-40, +40]. Doble línea en 0. Carril 0 en offset 10, Carril 1 en offset 26.
                    const offsetLateral = (this.carril === 0) ? 11 : 26;

                    if (this.via === 1) {{
                        // Vía 1: Desplazamiento sobre Eje X
                        if (this.dir === 1) {{
                            // Hacia el Sureste (+x): Carril derecho (y > 0)
                            this.x = -MAP_LIM - Math.random() * 60;
                            this.y = offsetLateral;
                        }} else {{
                            // Hacia el Noroeste (-x): Carril contrario (y < 0)
                            this.x = MAP_LIM + Math.random() * 60;
                            this.y = -offsetLateral;
                        }}
                    }} else {{
                        // Vía 2: Desplazamiento sobre Eje Y
                        if (this.dir === 1) {{
                            // Hacia el Suroeste (+y): Carril derecho (x > 0)
                            this.y = -MAP_LIM - Math.random() * 60;
                            this.x = offsetLateral;
                        }} else {{
                            // Hacia el Noreste (-y): Carril contrario (x < 0)
                            this.y = MAP_LIM + Math.random() * 60;
                            this.x = -offsetLateral;
                        }}
                    }}
                }}

                actualizar(dt, sem1, sem2) {{
                    const stopLineDist = 48; // Distancia de la línea de parada desde el centro
                    let distALinea = 9999;
                    let yaCruzo = false;

                    if (this.via === 1) {{
                        if (this.dir === 1) {{
                            distALinea = -stopLineDist - this.x;
                            yaCruzo = (this.x > -stopLineDist + 5);
                        }} else {{
                            distALinea = this.x - stopLineDist;
                            yaCruzo = (this.x < stopLineDist - 5);
                        }}
                    }} else {{
                        if (this.dir === 1) {{
                            distALinea = -stopLineDist - this.y;
                            yaCruzo = (this.y > -stopLineDist + 5);
                        }} else {{
                            distALinea = this.y - stopLineDist;
                            yaCruzo = (this.y < stopLineDist - 5);
                        }}
                    }}

                    const semaforoPropio = (this.via === 1) ? sem1 : sem2;
                    let debeFrenar = false;

                    // 1. Respeto de Semáforo
                    if (!yaCruzo && distALinea > 0 && distALinea < 85) {{
                        if (semaforoPropio === 'ROJO') debeFrenar = true;
                        else if (semaforoPropio === 'AMARILLO' && distALinea > 22) debeFrenar = true;
                    }}

                    // 2. Modelo de Seguimiento Vehicular (Car-Following en el mismo carril)
                    let distVehiculoDelante = 9999;
                    for (let otro of vehiculos) {{
                        if (otro.id === this.id || otro.via !== this.via || otro.dir !== this.dir || otro.carril !== this.carril) continue;

                        let d = 9999;
                        if (this.via === 1) {{
                            d = (this.dir === 1) ? (otro.x - this.x) : (this.x - otro.x);
                        }} else {{
                            d = (this.dir === 1) ? (otro.y - this.y) : (this.y - otro.y);
                        }}

                        if (d > 0 && d < distVehiculoDelante) {{
                            distVehiculoDelante = d;
                        }}
                    }}

                    const distSeguridad = this.largo + 8;
                    if (distVehiculoDelante < distSeguridad + 40) {{
                        debeFrenar = true;
                    }}

                    // Cinemática de aceleración y desaceleración
                    this.frenando = debeFrenar;
                    if (debeFrenar) {{
                        let tasaFrenado = 3.6;
                        if (distVehiculoDelante < distSeguridad + 4 || distALinea < 6) tasaFrenado = 6.0;
                        this.velocidad = Math.max(0, this.velocidad - tasaFrenado * dt);
                    }} else {{
                        this.velocidad = Math.min(this.velocidadMaxima, this.velocidad + 1.8 * dt);
                    }}
                    if (this.velocidad < 0.04) this.velocidad = 0;

                    // Desplazamiento longitudinal dentro de la vía
                    if (this.via === 1) this.x += this.dir * this.velocidad * dt * 28;
                    else this.y += this.dir * this.velocidad * dt * 28;
                }}

                estaFuera() {{
                    return (Math.abs(this.x) > MAP_LIM + 40 || Math.abs(this.y) > MAP_LIM + 40);
                }}

                dibujar(ctx, esNoche) {{
                    const x = this.x;
                    const y = this.y;
                    const L = this.largo;
                    const W = this.ancho;
                    const H = this.alto;

                    // Definir semidimensiones según eje de circulación:
                    // Vía 1 (corre en X): largo en eje X, ancho en eje Y
                    // Vía 2 (corre en Y): largo en eje Y, ancho en eje X
                    const lx = (this.via === 1) ? (L / 2) : (W / 2);
                    const ly = (this.via === 1) ? (W / 2) : (L / 2);

                    const p0 = iso(x - lx, y - ly, 0);
                    const p1 = iso(x + lx, y - ly, 0);
                    const p2 = iso(x + lx, y + ly, 0);
                    const p3 = iso(x - lx, y + ly, 0);

                    const p4 = iso(x - lx, y - ly, H);
                    const p5 = iso(x + lx, y - ly, H);
                    const p6 = iso(x + lx, y + ly, H);
                    const p7 = iso(x - lx, y + ly, H);

                    // 1. Sombra suave sobre el asfalto
                    ctx.fillStyle = esNoche ? 'rgba(0, 0, 0, 0.45)' : 'rgba(0, 0, 0, 0.22)';
                    ctx.beginPath();
                    ctx.moveTo(p0.x + 2, p0.y + 2);
                    ctx.lineTo(p1.x + 2, p1.y + 2);
                    ctx.lineTo(p2.x + 2, p2.y + 2);
                    ctx.lineTo(p3.x + 2, p3.y + 2);
                    ctx.closePath();
                    ctx.fill();

                    // 2. Ruedas (cilindros oscuros)
                    ctx.fillStyle = '#0F172A';
                    const rSize = 2.8;
                    ctx.beginPath();
                    ctx.arc((p0.x + p1.x) / 2 - 3, (p0.y + p1.y) / 2 + 1, rSize, 0, Math.PI * 2);
                    ctx.arc((p0.x + p1.x) / 2 + 6, (p0.y + p1.y) / 2 + 1, rSize, 0, Math.PI * 2);
                    ctx.fill();

                    // 3. Caras del chasis según iluminación natural
                    // Cara lateral izquierda (orientada al sol)
                    ctx.fillStyle = oscurecerColor(this.color, 0.85);
                    ctx.beginPath();
                    ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y); ctx.lineTo(p5.x, p5.y); ctx.lineTo(p4.x, p4.y);
                    ctx.closePath();
                    ctx.fill();

                    // Cara frontal / trasera
                    ctx.fillStyle = oscurecerColor(this.color, 0.72);
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.lineTo(p6.x, p6.y); ctx.lineTo(p5.x, p5.y);
                    ctx.closePath();
                    ctx.fill();

                    // Cara superior (Techo y capó)
                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.moveTo(p4.x, p4.y); ctx.lineTo(p5.x, p5.y); ctx.lineTo(p6.x, p6.y); ctx.lineTo(p7.x, p7.y);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = 'rgba(255,255,255,0.18)';
                    ctx.stroke();

                    // 4. Parabrisas y Cabina (Vidrio con reflejos)
                    const clx = lx * 0.65;
                    const cly = ly * 0.75;
                    const c0 = iso(x - clx, y - cly, H + 0.3);
                    const c1 = iso(x + clx, y - cly, H + 0.3);
                    const c2 = iso(x + clx, y + cly, H + 0.3);
                    const c3 = iso(x - clx, y + cly, H + 0.3);

                    ctx.fillStyle = esNoche ? '#0F172A' : '#1E293B';
                    ctx.beginPath();
                    ctx.moveTo(c0.x, c0.y); ctx.lineTo(c1.x, c1.y); ctx.lineTo(c2.x, c2.y); ctx.lineTo(c3.x, c3.y);
                    ctx.closePath();
                    ctx.fill();

                    // Techo de cabina superior
                    const t0 = iso(x - clx * 0.8, y - cly * 0.8, H + 3.2);
                    const t1 = iso(x + clx * 0.8, y - cly * 0.8, H + 3.2);
                    const t2 = iso(x + clx * 0.8, y + cly * 0.8, H + 3.2);
                    const t3 = iso(x - clx * 0.8, y + cly * 0.8, H + 3.2);

                    ctx.fillStyle = this.color;
                    ctx.beginPath();
                    ctx.moveTo(t0.x, t0.y); ctx.lineTo(t1.x, t1.y); ctx.lineTo(t2.x, t2.y); ctx.lineTo(t3.x, t3.y);
                    ctx.closePath();
                    ctx.fill();

                    // 5. Letrero de Taxi si aplica
                    if (this.tipo === 'Taxi') {{
                        const tx = iso(x, y, H + 5.5);
                        ctx.fillStyle = '#FFFFFF';
                        ctx.fillRect(tx.x - 4, tx.y - 2.5, 8, 4);
                        ctx.fillStyle = '#000000';
                        ctx.font = 'bold 4px Arial';
                        ctx.textAlign = 'center';
                        ctx.fillText('TAXI', tx.x, tx.y + 1);
                    }}

                    // 6. Faros delanteros y luces de freno
                    let fx = x + (this.via === 1 ? this.dir * (lx + 1) : 0);
                    let fy = y + (this.via === 2 ? this.dir * (ly + 1) : 0);
                    const pFaro = iso(fx, fy, 2.5);

                    if (esNoche) {{
                        // Haz de luz cónico nocturno proyectado en el asfalto
                        ctx.save();
                        let txEnd = fx + (this.via === 1 ? this.dir * 38 : 0);
                        let tyEnd = fy + (this.via === 2 ? this.dir * 38 : 0);
                        const pFin = iso(txEnd, tyEnd, 0);

                        const grad = ctx.createRadialGradient(pFaro.x, pFaro.y, 3, pFin.x, pFin.y, 25);
                        grad.addColorStop(0, 'rgba(254, 240, 138, 0.40)');
                        grad.addColorStop(0.5, 'rgba(254, 240, 138, 0.12)');
                        grad.addColorStop(1, 'rgba(254, 240, 138, 0.0)');

                        ctx.fillStyle = grad;
                        ctx.beginPath();
                        ctx.arc(pFin.x, pFin.y, 20, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.restore();
                    }}

                    // Luces de freno traseras (se encienden en rojo brillante al frenar)
                    let bx = x - (this.via === 1 ? this.dir * (lx + 1) : 0);
                    let by = y - (this.via === 2 ? this.dir * (ly + 1) : 0);
                    const pFreno = iso(bx, by, 2.5);

                    if (this.frenando || this.velocidad < 0.15) {{
                        ctx.save();
                        ctx.fillStyle = '#FF1744';
                        ctx.shadowColor = '#FF1744';
                        ctx.shadowBlur = 8;
                        ctx.beginPath();
                        ctx.arc(pFreno.x, pFreno.y, 2.8, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.restore();
                    }}
                }}
            }}

            // Función para modular sombras de color
            function oscurecerColor(col, factor) {{
                if (col.startsWith('#')) {{
                    let c = parseInt(col.slice(1), 16);
                    let r = Math.floor(((c >> 16) & 255) * factor);
                    let g = Math.floor(((c >> 8) & 255) * factor);
                    let b = Math.floor((c & 255) * factor);
                    return `rgb(${{r}},${{g}},${{b}})`;
                }}
                return col;
            }}

            // =================================================================
            // FUENTE DE AGUA ANIMADA CON FÍSICA DE GRAVEDAD
            // =================================================================
            const particulasAgua = [];
            for (let i = 0; i < 40; i++) {{
                particulasAgua.push({{
                    x: 135 + (Math.random() - 0.5) * 4,
                    y: 135 + (Math.random() - 0.5) * 4,
                    z: 2 + Math.random() * 8,
                    vz: 1.8 + Math.random() * 1.5,
                    vel: 0.12 + Math.random() * 0.18,
                    ang: Math.random() * Math.PI * 2
                }});
            }}

            // =================================================================
            // CAPA 1: DIBUJADO DEL SUELO, VÍAS, VEREDAS Y SEÑALIZACIÓN (Z = 0)
            // =================================================================
            function dibujarSueloYVias(ctx) {{
                const LIM = MAP_LIM;

                // 1. TERRENO BASE (Césped natural o tono nocturno)
                ctx.fillStyle = esNoche ? '#081710' : '#15803D';
                dibujarPoligonoIso(ctx, [
                    iso(-LIM, -LIM, 0), iso(LIM, -LIM, 0),
                    iso(LIM, LIM, 0), iso(-LIM, LIM, 0)
                ], esNoche ? '#081710' : '#15803D');

                // 2. BASES DE MANZANAS URBANAS (Granito y pavimento peatonal)
                const colPlaza = esNoche ? '#0F172A' : '#E2E8F0';
                // Manzana Norte (x <= -56, y <= -56)
                dibujarPoligonoIso(ctx, [
                    iso(-LIM, -LIM, 0), iso(-BOUND_BLOCK, -LIM, 0),
                    iso(-BOUND_BLOCK, -BOUND_BLOCK, 0), iso(-LIM, -BOUND_BLOCK, 0)
                ], colPlaza);
                // Manzana Oeste (x >= 56, y <= -56)
                dibujarPoligonoIso(ctx, [
                    iso(BOUND_BLOCK, -LIM, 0), iso(LIM, -LIM, 0),
                    iso(LIM, -BOUND_BLOCK, 0), iso(BOUND_BLOCK, -BOUND_BLOCK, 0)
                ], colPlaza);
                // Manzana Este (x <= -56, y >= 56)
                dibujarPoligonoIso(ctx, [
                    iso(-LIM, BOUND_BLOCK, 0), iso(-BOUND_BLOCK, BOUND_BLOCK, 0),
                    iso(-BOUND_BLOCK, LIM, 0), iso(-LIM, LIM, 0)
                ], colPlaza);
                // Manzana Sur (x >= 56, y >= 56: Parque Urbano)
                dibujarPoligonoIso(ctx, [
                    iso(BOUND_BLOCK, BOUND_BLOCK, 0), iso(LIM, BOUND_BLOCK, 0),
                    iso(LIM, LIM, 0), iso(BOUND_BLOCK, LIM, 0)
                ], esNoche ? '#062013' : '#166534');

                // 3. CALZADAS ASFALTADAS (Vía 1 y Vía 2)
                const colAsfalto = esNoche ? '#131B26' : '#242D3D';
                // Avenida 1: corre a lo largo del eje X, entre y = -W_ROAD y y = +W_ROAD
                dibujarPoligonoIso(ctx, [
                    iso(-LIM, -W_ROAD, 0), iso(LIM, -W_ROAD, 0),
                    iso(LIM, W_ROAD, 0), iso(-LIM, W_ROAD, 0)
                ], colAsfalto);
                // Avenida 2: corre a lo largo del eje Y, entre x = -W_ROAD y x = +W_ROAD
                dibujarPoligonoIso(ctx, [
                    iso(-W_ROAD, -LIM, 0), iso(W_ROAD, -LIM, 0),
                    iso(W_ROAD, LIM, 0), iso(-W_ROAD, LIM, 0)
                ], colAsfalto);

                // Cuadrante central de la intersección
                dibujarPoligonoIso(ctx, [
                    iso(-W_ROAD, -W_ROAD, 0), iso(W_ROAD, -W_ROAD, 0),
                    iso(W_ROAD, W_ROAD, 0), iso(-W_ROAD, W_ROAD, 0)
                ], esNoche ? '#172230' : '#2A3649');

                // 4. VEREDAS ELEVADAS CON BORDILLOS 3D (z = 2.0)
                const colBordillo = esNoche ? '#1E293B' : '#94A3B8';
                const colVeredaTop = esNoche ? '#0F172A' : '#CBD5E1';

                // Bordillo de vereda en las 4 esquinas del cruce
                function dibujarVeredaEsquina(x0, x1, y0, y1) {{
                    // Borde superior vereda a z = 2
                    dibujarPoligonoIso(ctx, [
                        iso(x0, y0, 2), iso(x1, y0, 2),
                        iso(x1, y1, 2), iso(x0, y1, 2)
                    ], colVeredaTop);
                }}

                dibujarVeredaEsquina(-LIM, -W_ROAD, -BOUND_BLOCK, -W_ROAD);
                dibujarVeredaEsquina(W_ROAD, LIM, -BOUND_BLOCK, -W_ROAD);
                dibujarVeredaEsquina(-LIM, -W_ROAD, W_ROAD, BOUND_BLOCK);
                dibujarVeredaEsquina(W_ROAD, LIM, W_ROAD, BOUND_BLOCK);

                dibujarVeredaEsquina(-BOUND_BLOCK, -W_ROAD, -LIM, -W_ROAD);
                dibujarVeredaEsquina(W_ROAD, BOUND_BLOCK, -LIM, -W_ROAD);
                dibujarVeredaEsquina(-BOUND_BLOCK, -W_ROAD, W_ROAD, LIM);
                dibujarVeredaEsquina(W_ROAD, BOUND_BLOCK, W_ROAD, LIM);

                // 5. SEÑALIZACIÓN VIAL (Líneas divisorias y pasos de cebra)
                // Doble línea central amarilla continua
                ctx.strokeStyle = '#F59E0B';
                ctx.lineWidth = 1.6;
                dibujarLineaIso(ctx, -LIM, 0, -W_ROAD - 8, 0, 1.6, '#F59E0B');
                dibujarLineaIso(ctx, W_ROAD + 8, 0, LIM, 0, 1.6, '#F59E0B');
                dibujarLineaIso(ctx, 0, -LIM, 0, -W_ROAD - 8, 1.6, '#F59E0B');
                dibujarLineaIso(ctx, 0, W_ROAD + 8, 0, LIM, 1.6, '#F59E0B');

                // Líneas blancas punteadas entre carriles (carril interior y exterior)
                dibujarLineaDiscontinuaIso(ctx, -LIM, 18, -W_ROAD - 8, 18, '#FFFFFF');
                dibujarLineaDiscontinuaIso(ctx, -LIM, -18, -W_ROAD - 8, -18, '#FFFFFF');
                dibujarLineaDiscontinuaIso(ctx, W_ROAD + 8, 18, LIM, 18, '#FFFFFF');
                dibujarLineaDiscontinuaIso(ctx, W_ROAD + 8, -18, LIM, -18, '#FFFFFF');

                dibujarLineaDiscontinuaIso(ctx, 18, -LIM, 18, -W_ROAD - 8, '#FFFFFF');
                dibujarLineaDiscontinuaIso(ctx, -18, -LIM, -18, -W_ROAD - 8, '#FFFFFF');
                dibujarLineaDiscontinuaIso(ctx, 18, W_ROAD + 8, 18, LIM, '#FFFFFF');
                dibujarLineaDiscontinuaIso(ctx, -18, W_ROAD + 8, -18, LIM, '#FFFFFF');

                // Líneas de parada blancas de semáforo (Stop lines)
                dibujarLineaIso(ctx, -48, 0, -48, W_ROAD, 2.5, '#FFFFFF');
                dibujarLineaIso(ctx, 48, -W_ROAD, 48, 0, 2.5, '#FFFFFF');
                dibujarLineaIso(ctx, 0, -48, W_ROAD, -48, 2.5, '#FFFFFF');
                dibujarLineaIso(ctx, -W_ROAD, 48, 0, 48, 2.5, '#FFFFFF');

                // Pasos peatonales de cebra en las 4 entradas
                const zW = 2.4;
                // Cebra NW (Avenida 1)
                for (let y = -W_ROAD + 2; y <= W_ROAD - 2; y += 5.5) {{
                    dibujarPoligonoIso(ctx, [
                        iso(-46, y, 0.2), iso(-41, y, 0.2),
                        iso(-41, y + zW, 0.2), iso(-46, y + zW, 0.2)
                    ], '#FFFFFF');
                }}
                // Cebra SE (Avenida 1)
                for (let y = -W_ROAD + 2; y <= W_ROAD - 2; y += 5.5) {{
                    dibujarPoligonoIso(ctx, [
                        iso(41, y, 0.2), iso(46, y, 0.2),
                        iso(46, y + zW, 0.2), iso(41, y + zW, 0.2)
                    ], '#FFFFFF');
                }}
                // Cebra NE (Avenida 2)
                for (let x = -W_ROAD + 2; x <= W_ROAD - 2; x += 5.5) {{
                    dibujarPoligonoIso(ctx, [
                        iso(x, -46, 0.2), iso(x + zW, -46, 0.2),
                        iso(x + zW, -41, 0.2), iso(x, -41, 0.2)
                    ], '#FFFFFF');
                }}
                // Cebra SW (Avenida 2)
                for (let x = -W_ROAD + 2; x <= W_ROAD - 2; x += 5.5) {{
                    dibujarPoligonoIso(ctx, [
                        iso(x, 41, 0.2), iso(x + zW, 41, 0.2),
                        iso(x + zW, 46, 0.2), iso(x, 46, 0.2)
                    ], '#FFFFFF');
                }}
            }}

            function dibujarPoligonoIso(ctx, puntos, col) {{
                ctx.fillStyle = col;
                ctx.beginPath();
                ctx.moveTo(puntos[0].x, puntos[0].y);
                for (let i = 1; i < puntos.length; i++) {{
                    ctx.lineTo(puntos[i].x, puntos[i].y);
                }}
                ctx.closePath();
                ctx.fill();
            }}

            function dibujarLineaIso(ctx, x0, y0, x1, y1, w, col) {{
                const p0 = iso(x0, y0, 0);
                const p1 = iso(x1, y1, 0);
                ctx.strokeStyle = col;
                ctx.lineWidth = w;
                ctx.beginPath();
                ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y);
                ctx.stroke();
            }}

            function dibujarLineaDiscontinuaIso(ctx, x0, y0, x1, y1, col) {{
                const p0 = iso(x0, y0, 0);
                const p1 = iso(x1, y1, 0);
                ctx.save();
                ctx.strokeStyle = col;
                ctx.lineWidth = 1.2;
                ctx.setLineDash([5, 5]);
                ctx.beginPath();
                ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y);
                ctx.stroke();
                ctx.restore();
            }}

            // =================================================================
            // ENTIDADES 3D CON ORDENAMIENTO DE PROFUNDIDAD (Z-SORTING D = x + y)
            // =================================================================

            // 1. EDIFICIO PRISMÁTICO CON FACHADAS Y VENTANAS
            class Edificio3D {{
                constructor(x0, y0, x1, y1, h, colBase, colLuz, rotulo = '') {{
                    this.x0 = Math.min(x0, x1);
                    this.y0 = Math.min(y0, y1);
                    this.x1 = Math.max(x0, x1);
                    this.y1 = Math.max(y0, y1);
                    this.h = h;
                    this.colBase = colBase;
                    this.colLuz = colLuz;
                    this.rotulo = rotulo;
                    // Profundidad base en el vértice más cercano a la cámara:
                    this.depth = this.x1 + this.y1;
                }}

                draw(ctx) {{
                    const x0 = this.x0, y0 = this.y0, x1 = this.x1, y1 = this.y1, h = this.h;

                    // Sombra proyectada en el suelo
                    ctx.fillStyle = esNoche ? 'rgba(0, 0, 0, 0.40)' : 'rgba(0, 0, 0, 0.20)';
                    const s0 = iso(x0 + 8, y0 + 8, 0);
                    const s1 = iso(x1 + 18, y0 + 8, 0);
                    const s2 = iso(x1 + 18, y1 + 18, 0);
                    const s3 = iso(x0 + 8, y1 + 18, 0);
                    ctx.beginPath();
                    ctx.moveTo(s0.x, s0.y); ctx.lineTo(s1.x, s1.y); ctx.lineTo(s2.x, s2.y); ctx.lineTo(s3.x, s3.y);
                    ctx.closePath();
                    ctx.fill();

                    // Vértices 3D
                    const b0 = iso(x0, y0, 0); const b1 = iso(x1, y0, 0);
                    const b2 = iso(x1, y1, 0); const b3 = iso(x0, y1, 0);

                    const t0 = iso(x0, y0, h); const t1 = iso(x1, y0, h);
                    const t2 = iso(x1, y1, h); const t3 = iso(x0, y1, h);

                    // Fachada Izquierda (da hacia el Suroeste / orientada a la luz)
                    ctx.fillStyle = this.colLuz;
                    ctx.beginPath();
                    ctx.moveTo(b3.x, b3.y); ctx.lineTo(b2.x, b2.y); ctx.lineTo(t2.x, t2.y); ctx.lineTo(t3.x, t3.y);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = 'rgba(0,0,0,0.15)';
                    ctx.stroke();

                    // Fachada Derecha (da hacia el Sureste / cara lateral sombreada)
                    ctx.fillStyle = this.colBase;
                    ctx.beginPath();
                    ctx.moveTo(b1.x, b1.y); ctx.lineTo(b2.x, b2.y); ctx.lineTo(t2.x, t2.y); ctx.lineTo(t1.x, t1.y);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = 'rgba(0,0,0,0.15)';
                    ctx.stroke();

                    // Techo horizontal
                    ctx.fillStyle = oscurecerColor(this.colLuz, 1.15);
                    ctx.beginPath();
                    ctx.moveTo(t0.x, t0.y); ctx.lineTo(t1.x, t1.y); ctx.lineTo(t2.x, t2.y); ctx.lineTo(t3.x, t3.y);
                    ctx.closePath();
                    ctx.fill();
                    ctx.strokeStyle = 'rgba(255,255,255,0.25)';
                    ctx.stroke();

                    // Ventanas arquitectónicas regulares en la fachada visible
                    const colWin = esNoche ? '#FDE047' : '#93C5FD';
                    const numPisos = Math.floor(h / 14);
                    for (let p = 1; p <= numPisos; p++) {{
                        const zPiso = p * 12;
                        for (let vx = x0 + 12; vx < x1 - 8; vx += 18) {{
                            const wp = iso(vx, y1, zPiso);
                            ctx.fillStyle = colWin;
                            if (esNoche) {{
                                ctx.shadowColor = '#FDE047';
                                ctx.shadowBlur = 5;
                            }}
                            ctx.fillRect(wp.x - 3, wp.y - 3, 6, 6);
                            ctx.shadowBlur = 0;
                        }}
                    }}

                    // Rótulo luminoso si aplica (ej. "TECH TOWER")
                    if (this.rotulo) {{
                        const pRotulo = iso((x0 + x1) / 2, (y0 + y1) / 2, h + 12);
                        ctx.save();
                        ctx.fillStyle = '#0F172A';
                        ctx.fillRect(pRotulo.x - 36, pRotulo.y - 10, 72, 16);
                        ctx.strokeStyle = '#00E5FF';
                        ctx.lineWidth = 1;
                        ctx.strokeRect(pRotulo.x - 36, pRotulo.y - 10, 72, 16);

                        ctx.shadowColor = '#00E5FF';
                        ctx.shadowBlur = esNoche ? 10 : 4;
                        ctx.fillStyle = '#00E5FF';
                        ctx.font = 'bold 9px sans-serif';
                        ctx.textAlign = 'center';
                        ctx.fillText(this.rotulo, pRotulo.x, pRotulo.y + 2);
                        ctx.restore();
                    }}
                }}
            }}

            // 2. CAFÉ BISTRO CON TERRAZA Y SOMBRILLAS
            class CafeBistro3D {{
                constructor(x0, y0, x1, y1) {{
                    this.edificio = new Edificio3D(x0, y0, x1, y1, 32, '#78350F', '#B45309', '');
                    this.x0 = x0; this.y0 = y0; this.x1 = x1; this.y1 = y1;
                    this.depth = x1 + y1 + 10;
                }}

                draw(ctx) {{
                    this.edificio.draw(ctx);

                    // Letrero del Café
                    const pSign = iso((this.x0 + this.x1) / 2, this.y1, 24);
                    ctx.save();
                    ctx.fillStyle = '#FFB800';
                    ctx.shadowColor = '#FFB800';
                    ctx.shadowBlur = 6;
                    ctx.font = 'bold 8px sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('☕ CAFÉ BISTRO', pSign.x, pSign.y);
                    ctx.restore();

                    // Sombrillas rojas y blancas en la terraza exterior
                    const sombrillas = [
                        {{ x: this.x1 + 14, y: this.y0 + 10 }},
                        {{ x: this.x1 + 24, y: this.y0 + 22 }}
                    ];
                    for (let s of sombrillas) {{
                        const pb = iso(s.x, s.y, 0);
                        const pt = iso(s.x, s.y, 12);
                        ctx.strokeStyle = '#475569';
                        ctx.lineWidth = 1.5;
                        ctx.beginPath();
                        ctx.moveTo(pb.x, pb.y); ctx.lineTo(pt.x, pt.y);
                        ctx.stroke();

                        ctx.fillStyle = '#EF4444';
                        ctx.beginPath();
                        ctx.arc(pt.x, pt.y, 7, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.fillStyle = '#FFFFFF';
                        ctx.beginPath();
                        ctx.arc(pt.x, pt.y, 2.5, 0, Math.PI * 2);
                        ctx.fill();
                    }}
                }}
            }}

            // 3. MALL COMERCIAL CON PARQUEO
            class MallComercial3D {{
                constructor(x0, y0, x1, y1) {{
                    this.edificio = new Edificio3D(x0, y0, x1, y1, 48, '#1E293B', '#334155', 'METRO MALL');
                    this.x0 = x0; this.y0 = y0; this.x1 = x1; this.y1 = y1;
                    this.depth = x1 + y1;
                }}

                draw(ctx) {{
                    this.edificio.draw(ctx);

                    // Autos estacionados en las bahías de parqueo
                    dibujarAutoAparcado(ctx, this.x1 + 18, this.y0 + 12, '#EF4444');
                    dibujarAutoAparcado(ctx, this.x1 + 18, this.y0 + 32, '#3B82F6');
                }}
            }}

            function dibujarAutoAparcado(ctx, x, y, col) {{
                const p0 = iso(x - 8, y - 5, 0);
                const p1 = iso(x + 8, y - 5, 0);
                const p2 = iso(x + 8, y + 5, 0);
                const p3 = iso(x - 8, y + 5, 0);
                const pt = iso(x, y, 5);

                ctx.fillStyle = col;
                ctx.beginPath();
                ctx.moveTo(p0.x, p0.y); ctx.lineTo(p1.x, p1.y); ctx.lineTo(p2.x, p2.y); ctx.lineTo(p3.x, p3.y);
                ctx.closePath();
                ctx.fill();

                ctx.fillStyle = '#0F172A';
                ctx.beginPath();
                ctx.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
                ctx.fill();
            }}

            // 4. ÁRBOL ISOMÉTRICO TRIDIMENSIONAL
            class Arbol3D {{
                constructor(x, y, colorCopa, altura = 20) {{
                    this.x = x;
                    this.y = y;
                    this.colorCopa = colorCopa;
                    this.altura = altura;
                    this.depth = x + y;
                }}

                draw(ctx) {{
                    const pBase = iso(this.x, this.y, 0);
                    const pCopa = iso(this.x, this.y, this.altura);

                    // Sombra
                    ctx.fillStyle = esNoche ? 'rgba(0,0,0,0.30)' : 'rgba(0,0,0,0.18)';
                    ctx.beginPath();
                    ctx.ellipse(pBase.x + 2, pBase.y + 1, 9, 5, 0, 0, Math.PI * 2);
                    ctx.fill();

                    // Tronco
                    ctx.strokeStyle = '#78350F';
                    ctx.lineWidth = 2.8;
                    ctx.beginPath();
                    ctx.moveTo(pBase.x, pBase.y); ctx.lineTo(pCopa.x, pCopa.y);
                    ctx.stroke();

                    // Copa de hojas
                    ctx.fillStyle = this.colorCopa;
                    ctx.beginPath();
                    ctx.arc(pCopa.x, pCopa.y, 9, 0, Math.PI * 2);
                    ctx.arc(pCopa.x - 5, pCopa.y + 2, 7, 0, Math.PI * 2);
                    ctx.arc(pCopa.x + 5, pCopa.y + 2, 7, 0, Math.PI * 2);
                    ctx.arc(pCopa.x, pCopa.y - 5, 7.5, 0, Math.PI * 2);
                    ctx.fill();
                }}
            }}

            // 5. FUENTE DE AGUA DEL PARQUE CENTRAL
            class FuenteAgua3D {{
                constructor(x, y) {{
                    this.x = x;
                    this.y = y;
                    this.depth = x + y;
                }}

                draw(ctx) {{
                    const pC = iso(this.x, this.y, 1);

                    // Anillo de piedra
                    ctx.fillStyle = '#94A3B8';
                    ctx.beginPath();
                    ctx.ellipse(pC.x, pC.y, 28, 16, 0, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = '#475569';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();

                    // Agua azul
                    ctx.fillStyle = esNoche ? '#0284C7' : '#38BDF8';
                    if (esNoche) {{
                        ctx.shadowColor = '#00E5FF';
                        ctx.shadowBlur = 10;
                    }}
                    ctx.beginPath();
                    ctx.ellipse(pC.x, pC.y, 22, 12, 0, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.shadowBlur = 0;

                    // Gotas de agua animadas
                    ctx.fillStyle = '#E0F2FE';
                    for (let pt of particulasAgua) {{
                        pt.z += pt.vz * 0.14;
                        pt.vz -= 0.10; // gravedad
                        pt.x += Math.cos(pt.ang) * pt.vel;
                        pt.y += Math.sin(pt.ang) * pt.vel;

                        if (pt.z <= 0) {{
                            pt.z = 2;
                            pt.vz = 1.6 + Math.random() * 1.5;
                            pt.x = this.x + (Math.random() - 0.5) * 3;
                            pt.y = this.y + (Math.random() - 0.5) * 3;
                        }}
                        const sp = iso(pt.x, pt.y, pt.z);
                        ctx.beginPath();
                        ctx.arc(sp.x, sp.y, 1.4, 0, Math.PI * 2);
                        ctx.fill();
                    }}
                }}
            }}

            // 6. SEMÁFORO VERTICAL ISOMÉTRICO CON CUENTA REGRESIVA LED
            class SemaforoVertical3D {{
                constructor(x, y, viaAsociada, orientacionTimer = 'izq') {{
                    this.x = x;
                    this.y = y;
                    this.via = viaAsociada; // 1: Vía 1, 2: Vía 2
                    this.orient = orientacionTimer;
                    this.depth = x + y;
                }}

                draw(ctx, est) {{
                    const pBase = iso(this.x, this.y, 0);
                    const pTop = iso(this.x, this.y, 36);

                    // Poste
                    ctx.strokeStyle = '#334155';
                    ctx.lineWidth = 2.8;
                    ctx.beginPath();
                    ctx.moveTo(pBase.x, pBase.y); ctx.lineTo(pTop.x, pTop.y);
                    ctx.stroke();

                    // Carcasa vertical
                    const cX = pTop.x;
                    const cY = pTop.y;
                    const sW = 12;
                    const sH = 30;

                    ctx.fillStyle = '#0F172A';
                    ctx.strokeStyle = '#475569';
                    ctx.lineWidth = 1.2;
                    ctx.beginPath();
                    ctx.roundRect(cX - sW / 2, cY - sH / 2, sW, sH, 3);
                    ctx.fill();
                    ctx.stroke();

                    const estadoLuz = (this.via === 1) ? est.luzV1 : est.luzV2;
                    const segRestantes = est.restante;

                    const yR = cY - 9;
                    const yA = cY;
                    const yV = cY + 9;
                    const rLuz = 3.6;

                    function pintarLuz(yPos, col, activo) {{
                        ctx.save();
                        if (activo) {{
                            ctx.shadowColor = col;
                            ctx.shadowBlur = 16; // Halo de resplandor bloom
                            ctx.fillStyle = col;
                            ctx.beginPath();
                            ctx.arc(cX, yPos, rLuz, 0, Math.PI * 2);
                            ctx.fill();

                            ctx.fillStyle = '#FFFFFF';
                            ctx.beginPath();
                            ctx.arc(cX, yPos, rLuz * 0.4, 0, Math.PI * 2);
                            ctx.fill();
                        }} else {{
                            ctx.fillStyle = 'rgba(15, 23, 42, 0.7)';
                            ctx.beginPath();
                            ctx.arc(cX, yPos, rLuz - 0.4, 0, Math.PI * 2);
                            ctx.fill();
                        }}
                        ctx.restore();
                    }}

                    pintarLuz(yR, '#FF1744', estadoLuz === 'ROJO');
                    pintarLuz(yA, '#FFD600', estadoLuz === 'AMARILLO');
                    pintarLuz(yV, '#00E676', estadoLuz === 'VERDE');

                    // Placa del Temporizador Digital LED adjunta
                    const colTimer = (estadoLuz === 'VERDE') ? '#00E676' : ((estadoLuz === 'AMARILLO') ? '#FFD600' : '#FF1744');
                    const tX = cX + (this.orient === 'izq' ? -16 : 16);
                    const tY = cY - 11;

                    ctx.save();
                    ctx.fillStyle = '#020617';
                    ctx.strokeStyle = colTimer;
                    ctx.lineWidth = 1;
                    ctx.beginPath();
                    ctx.roundRect(tX - 9, tY - 7, 18, 14, 2);
                    ctx.fill();
                    ctx.stroke();

                    ctx.shadowColor = colTimer;
                    ctx.shadowBlur = 6;
                    ctx.fillStyle = colTimer;
                    ctx.font = 'bold 9px monospace';
                    ctx.textAlign = 'center';
                    ctx.fillText(Math.ceil(segRestantes), tX, tY + 3.5);
                    ctx.restore();
                }}
            }}

            // Instancias estáticas de la ciudad
            const edificiosEstaticos = [
                // Manzana Norte: Gran Torre Tech y Corporativo
                new Edificio3D(-180, -170, -90, -90, 125, '#1E3A8A', '#0284C7', 'TECH TOWER'),
                new Edificio3D(-240, -160, -195, -85, 75, '#334155', '#475569', 'OFFICE PARK'),

                // Manzana Oeste: Centro Comercial y Café
                new MallComercial3D(90, -180, 200, -90),
                new CafeBistro3D(75, -85, 130, -60),

                // Manzana Este: Condominio Residencial y Civico
                new Edificio3D(-190, 100, -110, 190, 75, '#475569', '#64748B', 'CENTRO CÍVICO'),

                // Manzana Sur: Fuente Central
                new FuenteAgua3D(135, 135)
            ];

            const arbolesEstaticos = [
                // Parque Urbano (Manzana Sur): Cerezos Sakura y verde
                new Arbol3D(95, 95, '#F472B6', 22),
                new Arbol3D(95, 175, '#EC4899', 24),
                new Arbol3D(175, 95, '#10B981', 25),
                new Arbol3D(180, 175, '#059669', 24),

                // Borde de veredas en Manzanas Norte y Este
                new Arbol3D(-85, -50, '#10B981', 18),
                new Arbol3D(-145, -50, '#059669', 18),
                new Arbol3D(-50, 95, '#10B981', 18),
                new Arbol3D(-50, 155, '#059669', 18)
            ];

            const semaforosEstaticos = [
                // 4 Semáforos ubicados rigurosamente sobre las veredas en las esquinas
                new SemaforoVertical3D(-52, 44, 1, 'izq'),  // Controla Av. 1 desde NW
                new SemaforoVertical3D(52, -44, 1, 'der'),  // Controla Av. 1 desde SE
                new SemaforoVertical3D(44, -52, 2, 'izq'),  // Controla Av. 2 desde NE
                new SemaforoVertical3D(-44, 52, 2, 'der')   // Controla Av. 2 desde SW
            ];

            // =================================================================
            // LÓGICA DE CONTROL DE SEMÁFOROS
            // =================================================================
            function getEstadoSemaforos() {{
                let luzV1 = 'ROJO';
                let luzV2 = 'ROJO';
                let dur = 30;

                if (faseActual === 0) {{ luzV1 = 'VERDE'; luzV2 = 'ROJO'; dur = g1_duracion; }}
                else if (faseActual === 1) {{ luzV1 = 'AMARILLO'; luzV2 = 'ROJO'; dur = tiempoAmarillo; }}
                else if (faseActual === 2) {{ luzV1 = 'ROJO'; luzV2 = 'ROJO'; dur = tiempoTodoRojo; }}
                else if (faseActual === 3) {{ luzV1 = 'ROJO'; luzV2 = 'VERDE'; dur = g2_duracion; }}
                else if (faseActual === 4) {{ luzV1 = 'ROJO'; luzV2 = 'AMARILLO'; dur = tiempoAmarillo; }}
                else if (faseActual === 5) {{ luzV1 = 'ROJO'; luzV2 = 'ROJO'; dur = tiempoTodoRojo; }}

                const restante = Math.max(0, dur - tiempoEnFase);
                return {{ luzV1, luzV2, duracion: dur, restante }};
            }}

            // Generador estocástico de llegadas vehiculares
            let acumLleg1 = 0;
            let acumLleg2 = 0;

            function spawnVehiculos(dt) {{
                const l1 = (CONFIG.lambda_1 / 60.0) * dt;
                const l2 = (CONFIG.lambda_2 / 60.0) * dt;
                acumLleg1 += l1;
                acumLleg2 += l2;

                if (acumLleg1 >= 1.0) {{
                    acumLleg1 -= 1.0;
                    const dir = Math.random() < 0.5 ? 1 : -1;
                    const carril = Math.random() < 0.5 ? 0 : 1;
                    vehiculos.push(new VehiculoIsometrico(1, dir, carril));
                }}
                if (acumLleg2 >= 1.0) {{
                    acumLleg2 -= 1.0;
                    const dir = Math.random() < 0.5 ? 1 : -1;
                    const carril = Math.random() < 0.5 ? 0 : 1;
                    vehiculos.push(new VehiculoIsometrico(2, dir, carril));
                }}
            }}

            // RENDERIZADO DEL RADAR MINIMAPA
            function dibujarMinimapa(luzV1, luzV2) {{
                miniCtx.clearRect(0, 0, 100, 100);
                miniCtx.fillStyle = '#1E293B';
                miniCtx.fillRect(42, 10, 16, 80);
                miniCtx.fillRect(10, 42, 80, 16);

                const col1 = (luzV1 === 'VERDE') ? '#00E676' : ((luzV1 === 'AMARILLO') ? '#FFD600' : '#FF1744');
                const col2 = (luzV2 === 'VERDE') ? '#00E676' : ((luzV2 === 'AMARILLO') ? '#FFD600' : '#FF1744');

                // Vía 1 (N-S)
                miniCtx.fillStyle = col1;
                miniCtx.beginPath();
                miniCtx.arc(50, 30, 4, 0, Math.PI * 2);
                miniCtx.arc(50, 70, 4, 0, Math.PI * 2);
                miniCtx.fill();

                // Vía 2 (E-O)
                miniCtx.fillStyle = col2;
                miniCtx.beginPath();
                miniCtx.arc(30, 50, 4, 0, Math.PI * 2);
                miniCtx.arc(70, 50, 4, 0, Math.PI * 2);
                miniCtx.fill();
            }}

            // =================================================================
            // BUCLE PRINCIPAL DE ANIMACIÓN ISOMÉTRICA (60 FPS)
            // =================================================================
            let tiempoAnterior = performance.now();

            function bucleAnimacion(ahora) {{
                const dtReal = Math.min((ahora - tiempoAnterior) / 1000, 0.1);
                tiempoAnterior = ahora;

                const est = getEstadoSemaforos();

                if (simulando) {{
                    const dt = dtReal * velocidad;
                    tiempoTotalSimulado += dt;
                    tiempoEnFase += dt;

                    if (tiempoEnFase >= est.duracion) {{
                        faseActual = (faseActual + 1) % 6;
                        tiempoEnFase = 0.0;
                    }}

                    spawnVehiculos(dt);

                    // Actualizar cinemática de vehículos
                    for (let i = vehiculos.length - 1; i >= 0; i--) {{
                        const v = vehiculos[i];
                        v.actualizar(dt, est.luzV1, est.luzV2);

                        if (v.estaFuera()) {{
                            vehiculosAtendidos++;
                            sumaTiemposEspera += (tiempoTotalSimulado - v.tiempoLlegada);
                            vehiculos.splice(i, 1);
                        }}
                    }}
                }}

                // Renderizado
                const w = canvas.getBoundingClientRect().width;
                const h = canvas.getBoundingClientRect().height;
                ctx.clearRect(0, 0, w, h);

                // PASO 1: Dibujar Suelo, Veredas, Calzadas y Señalización (Z = 0)
                dibujarSueloYVias(ctx);

                // PASO 2: Construir Cola Unificada de Renderizado 3D
                const renderQueue = [];

                // Registrar Edificios
                for (let ed of edificiosEstaticos) {{
                    renderQueue.push({{
                        depth: ed.depth,
                        draw: (c) => ed.draw(c)
                    }});
                }}

                // Registrar Árboles
                for (let arb of arbolesEstaticos) {{
                    renderQueue.push({{
                        depth: arb.depth,
                        draw: (c) => arb.draw(c)
                    }});
                }}

                // Registrar Semáforos
                for (let sem of semaforosEstaticos) {{
                    renderQueue.push({{
                        depth: sem.depth,
                        draw: (c) => sem.draw(c, est)
                    }});
                }}

                // Registrar Vehículos
                for (let v of vehiculos) {{
                    renderQueue.push({{
                        depth: v.x + v.y,
                        draw: (c) => v.dibujar(c, esNoche)
                    }});
                }}

                // PASO 3: ORDENAMIENTO ESTRICTO DE PROFUNDIDAD (Z-SORTING D = x + y)
                // Los objetos con menor D están físicamente más al norte (más lejos de la cámara)
                // y se dibujan PRIMERO. Los objetos con mayor D están al sur y se dibujan DESPUÉS.
                renderQueue.sort((a, b) => a.depth - b.depth);

                for (let item of renderQueue) {{
                    item.draw(ctx);
                }}

                // PASO 4: Actualizar Telemetría y Minimapa
                actualizarTelemetria(est);
                dibujarMinimapa(est.luzV1, est.luzV2);

                requestAnimationFrame(bucleAnimacion);
            }}

            function actualizarTelemetria(est) {{
                // Reloj horario
                const sec = Math.floor(tiempoTotalSimulado);
                const hh = String(14 + Math.floor(sec / 3600)).padStart(2, '0');
                const mm = String(37 + Math.floor((sec % 3600) / 60)).padStart(2, '0');
                const ss = String(sec % 60).padStart(2, '0');
                document.getElementById('sim-clock').innerText = `${{hh}}:${{mm}}:${{ss}}`;

                // Conteo de colas por acceso
                let qNorte = 0, qSur = 0, qEste = 0, qOeste = 0;
                for (let v of vehiculos) {{
                    if (v.velocidad < 0.2) {{
                        if (v.via === 1 && v.dir === 1) qNorte++;
                        else if (v.via === 1 && v.dir === -1) qSur++;
                        else if (v.via === 2 && v.dir === 1) qOeste++;
                        else if (v.via === 2 && v.dir === -1) qEste++;
                    }}
                }}

                document.getElementById('q-norte').innerText = qNorte + ' veh';
                document.getElementById('q-sur').innerText = qSur + ' veh';
                document.getElementById('q-este').innerText = qEste + ' veh';
                document.getElementById('q-oeste').innerText = qOeste + ' veh';

                document.getElementById('bar-norte').style.width = Math.min(100, qNorte * 10) + '%';
                document.getElementById('bar-sur').style.width = Math.min(100, qSur * 10) + '%';
                document.getElementById('bar-este').style.width = Math.min(100, qEste * 10) + '%';
                document.getElementById('bar-oeste').style.width = Math.min(100, qOeste * 10) + '%';

                const totalCola = qNorte + qSur + qEste + qOeste;
                document.getElementById('hud-cola-total').innerText = totalCola;
                document.getElementById('hud-atendidos').innerText = vehiculosAtendidos;

                const esperaProm = vehiculosAtendidos > 0 ? (sumaTiemposEspera / vehiculosAtendidos).toFixed(1) : '0.0';
                document.getElementById('hud-espera').innerText = esperaProm + ' s';
                document.getElementById('hud-g-star').innerText = g1_duracion.toFixed(1) + ' s';
            }}

            // =================================================================
            // CONTROLES INTERACTIVOS DEL USUARIO
            // =================================================================
            function setModo(modo) {{
                modoControl = modo;
                document.getElementById('btn-fijo').classList.remove('active');
                document.getElementById('btn-calc').classList.remove('active');
                document.getElementById('btn-ia').classList.remove('active');

                if (modo === 'fijo') {{
                    document.getElementById('btn-fijo').classList.add('active');
                    g1_duracion = CONFIG.g1_fijo;
                    g2_duracion = CONFIG.g2_fijo;
                    document.getElementById('hud-mejora').innerText = 'Base (0.0%)';
                    document.getElementById('hud-mejora').style.color = '#94A3B8';
                }} else if (modo === 'calculo') {{
                    document.getElementById('btn-calc').classList.add('active');
                    g1_duracion = CONFIG.g1_calc;
                    g2_duracion = CONFIG.g2_calc;
                    document.getElementById('hud-mejora').innerText = '+31.2%';
                    document.getElementById('hud-mejora').style.color = '#00E676';
                }} else if (modo === 'ia') {{
                    document.getElementById('btn-ia').classList.add('active');
                    g1_duracion = CONFIG.g1_ia;
                    g2_duracion = CONFIG.g2_ia;
                    document.getElementById('hud-mejora').innerText = '+34.8%';
                    document.getElementById('hud-mejora').style.color = '#00E676';
                }}
            }}

            function toggleDiaNoche() {{
                esNoche = !esNoche;
                const btn = document.getElementById('btn-time-mode');
                btn.innerText = esNoche ? '☀️ Día' : '🌙 Noche';
            }}

            function togglePlayPause() {{
                simulando = !simulando;
                const btn = document.getElementById('btn-play-pause');
                btn.innerText = simulando ? '⏸️' : '▶️';
            }}

            function reiniciarSimulacion() {{
                vehiculos = [];
                tiempoTotalSimulado = 0;
                tiempoEnFase = 0;
                faseActual = 0;
                vehiculosAtendidos = 0;
                sumaTiemposEspera = 0;
                inicializarFlotaInicial();
            }}

            function toggleVelocidad() {{
                if (velocidad === 1.0) velocidad = 2.0;
                else if (velocidad === 2.0) velocidad = 4.0;
                else velocidad = 1.0;
                document.getElementById('btn-speed').innerText = `${{velocidad}}x`;
            }}

            function inyectarRafaga() {{
                for (let i = 0; i < 3; i++) {{
                    vehiculos.push(new VehiculoIsometrico(1, 1, Math.random() < 0.5 ? 0 : 1));
                    vehiculos.push(new VehiculoIsometrico(1, -1, Math.random() < 0.5 ? 0 : 1));
                    vehiculos.push(new VehiculoIsometrico(2, 1, Math.random() < 0.5 ? 0 : 1));
                    vehiculos.push(new VehiculoIsometrico(2, -1, Math.random() < 0.5 ? 0 : 1));
                }}
            }}

            function inicializarFlotaInicial() {{
                for (let i = 0; i < 3; i++) {{
                    vehiculos.push(new VehiculoIsometrico(1, 1, i % 2));
                    vehiculos.push(new VehiculoIsometrico(1, -1, i % 2));
                    vehiculos.push(new VehiculoIsometrico(2, 1, i % 2));
                    vehiculos.push(new VehiculoIsometrico(2, -1, i % 2));
                }}
            }}

            // Arranque
            setModo(modoControl);
            inicializarFlotaInicial();
            requestAnimationFrame(bucleAnimacion);
        </script>
    </body>
    </html>
    """
    return html_code
