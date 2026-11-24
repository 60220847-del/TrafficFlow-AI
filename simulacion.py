"""
MÓDULO DE SIMULACIÓN DE TRÁFICO VEHICULAR Y DINÁMICA DE COLAS
============================================================
Proyecto: TrafficFlow AI
Carrera: Ingeniería Industrial
Asignatura: Cálculo Diferencial

Este módulo modela una intersección semaforizada de dos vías (Vía 1: Norte-Sur,
Vía 2: Este-Oeste) basada en la ecuación diferencial de conservación de flujo
y teoría de colas para sistemas discretos y continuos:
    Q'(t) = λ(t) - μ(t), con Q(t) >= 0

Donde:
    - Q(t): Cantidad instantánea de vehículos en cola (vehículos).
    - λ(t): Tasa de llegada vehicular (veh/s o veh/min).
    - μ(t): Tasa de salida o capacidad de descarga del semáforo (veh/s).
            Durante verde: μ = S (flujo de saturación).
            Durante amarillo: μ = β * S (factor de despeje).
            Durante rojo: μ = 0.
"""

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any, List, Optional, Tuple


class FaseSemaforo(Enum):
    VERDE_VIA_1 = "Verde Vía 1 (Norte-Sur)"
    AMARILLO_VIA_1 = "Amarillo Vía 1 (Norte-Sur)"
    TODO_ROJO_1 = "Todo Rojo (Seguridad 1)"
    VERDE_VIA_2 = "Verde Vía 2 (Este-Oeste)"
    AMARILLO_VIA_2 = "Amarillo Vía 2 (Este-Oeste)"
    TODO_ROJO_2 = "Todo Rojo (Seguridad 2)"


class EstadoVehiculo(Enum):
    APROXIMANDO = "Aproximando"
    EN_COLA = "En Cola"
    CRUZANDO = "Cruzando Intersección"
    COMPLETADO = "Completado"


@dataclass
class Vehiculo:
    id_vehiculo: int
    via_origen: int              # 1 para Vía 1 (N-S), 2 para Vía 2 (E-O)
    tiempo_llegada: float        # segundo de simulación en que llega a la cola
    tiempo_inicio_atencion: Optional[float] = None
    tiempo_salida: Optional[float] = None
    estado: EstadoVehiculo = EstadoVehiculo.APROXIMANDO
    posicion: float = 0.0        # Distancia en metros respecto al semáforo (negativo = aproximando, positivo = saliendo)
    velocidad: float = 11.11     # m/s (~40 km/h)
    tipo: str = "Sedán"
    color: str = "#3B82F6"       # Color visual del vehículo
    direccion: int = 1           # 1: sentido primario (ej. N->S u O->E), -1: sentido opuesto (S->N o E->O)
    carril: int = 0              # Carril asignado (0 o 1)
    largo_m: float = 4.5         # Largo físico del vehículo en metros
    ancho_m: float = 1.9         # Ancho físico en metros


@dataclass
class ConfiguracionSemaforo:
    tiempo_verde_1: float = 30.0    # g1 (segundos)
    tiempo_amarillo_1: float = 3.0   # y1 (segundos)
    tiempo_verde_2: float = 30.0    # g2 (segundos)
    tiempo_amarillo_2: float = 3.0   # y2 (segundos)
    tiempo_todo_rojo: float = 1.0   # r_all (segundos de despeje de seguridad)

    @property
    def ciclo_total(self) -> float:
        """Duración total del ciclo semafórico en segundos."""
        return (
            self.tiempo_verde_1
            + self.tiempo_amarillo_1
            + self.tiempo_todo_rojo
            + self.tiempo_verde_2
            + self.tiempo_amarillo_2
            + self.tiempo_todo_rojo
        )

    @property
    def verde_combinado(self) -> float:
        """Tiempo efectivo de verde disponible para optimización C = g1 + g2."""
        return self.tiempo_verde_1 + self.tiempo_verde_2


COLORES_VEHICULOS = [
    "#3B82F6",  # Azul Eléctrico Metálico
    "#EF4444",  # Rojo Carmesí Deportivo
    "#10B981",  # Verde Esmeralda
    "#F59E0B",  # Amarillo Taxi / Urbano
    "#F8FAFC",  # Blanco Perla
    "#1E293B",  # Negro Grafito
    "#94A3B8",  # Gris Plata Titanio
    "#EC4899",  # Magenta Sport
    "#8B5CF6",  # Púrpura Royal
    "#FB923C",  # Naranja Cobrizo
]

MODELOS_VEHICULOS = [
    ("Sedán", 4.5, 1.9, 0.40),
    ("SUV", 4.8, 2.1, 0.25),
    ("Camioneta", 5.2, 2.1, 0.15),
    ("Compacto", 3.8, 1.7, 0.12),
    ("Taxi", 4.5, 1.9, 0.08),
]


class SimuladorInterseccion:
    """
    Simulador híbrido (continuo-discreto) del comportamiento vehicular
    en una intersección ortogonal semaforizada.
    """

    def __init__(
        self,
        config_semaforo: Optional[ConfiguracionSemaforo] = None,
        tasa_llegada_1: float = 18.0,  # veh/minuto (0.3 veh/s)
        tasa_llegada_2: float = 12.0,  # veh/minuto (0.2 veh/s)
        flujo_saturacion_1: float = 36.0,  # veh/minuto (0.6 veh/s)
        flujo_saturacion_2: float = 36.0,  # veh/minuto (0.6 veh/s)
        cola_inicial_1: int = 5,
        cola_inicial_2: int = 4,
        es_estocastico: bool = True,
        semilla: Optional[int] = 42
    ):
        self.config = config_semaforo or ConfiguracionSemaforo()
        self.lambda_1 = tasa_llegada_1 / 60.0  # convertir a veh/segundo
        self.lambda_2 = tasa_llegada_2 / 60.0
        self.mu_sat_1 = flujo_saturacion_1 / 60.0
        self.mu_sat_2 = flujo_saturacion_2 / 60.0
        self.cola_inicial_1 = cola_inicial_1
        self.cola_inicial_2 = cola_inicial_2
        self.es_estocastico = es_estocastico
        self.semilla = semilla

        if semilla is not None:
            random.seed(semilla)

        self.reiniciar()

    def _crear_vehiculo(
        self,
        via_origen: int,
        tiempo_llegada: float,
        posicion: float,
        direccion: Optional[int] = None,
        carril: Optional[int] = None
    ) -> Vehiculo:
        """Crea un vehículo con apariencia reconocible, clase realista y color."""
        self.contador_vehiculos += 1
        
        # Selección ponderada del tipo de vehículo
        r_tipo = random.random()
        acumulado = 0.0
        tipo_sel = "Sedán"
        largo_sel = 4.5
        ancho_sel = 1.9
        for nombre, largo, ancho, prob in MODELOS_VEHICULOS:
            acumulado += prob
            if r_tipo <= acumulado:
                tipo_sel = nombre
                largo_sel = largo
                ancho_sel = ancho
                break

        # Color: Si es taxi, amarillo asegurado; sino de la paleta automotriz
        if tipo_sel == "Taxi":
            color_sel = "#F59E0B"
        else:
            color_sel = random.choice([c for c in COLORES_VEHICULOS if c != "#F59E0B"])

        # Dirección bidireccional (1: sentido Norte->Sur u Oeste->Este; -1: Sur->Norte o Este->Oeste)
        dir_sel = direccion if direccion is not None else (1 if random.random() < 0.55 else -1)
        carril_sel = carril if carril is not None else (0 if dir_sel == 1 else 1)

        return Vehiculo(
            id_vehiculo=self.contador_vehiculos,
            via_origen=via_origen,
            tiempo_llegada=tiempo_llegada,
            estado=EstadoVehiculo.EN_COLA if posicion <= -10.0 else EstadoVehiculo.APROXIMANDO,
            posicion=posicion,
            velocidad=0.0 if posicion <= -10.0 else 11.11,
            tipo=tipo_sel,
            color=color_sel,
            direccion=dir_sel,
            carril=carril_sel,
            largo_m=largo_sel,
            ancho_m=ancho_sel
        )

    def reiniciar(self) -> None:
        """Reinicia el estado del simulador al tiempo t=0."""
        if self.semilla is not None:
            random.seed(self.semilla)

        self.tiempo_actual: float = 0.0
        self.tiempo_en_fase: float = 0.0
        self.fase_actual: FaseSemaforo = FaseSemaforo.VERDE_VIA_1

        # Colas continuas Q(t)
        self.cola_1: float = float(self.cola_inicial_1)
        self.cola_2: float = float(self.cola_inicial_2)

        # Registro de vehículos
        self.vehiculos_1: List[Vehiculo] = []
        self.vehiculos_2: List[Vehiculo] = []
        self.contador_vehiculos: int = 0

        # Crear vehículos iniciales en cola (distribuidos en ambas direcciones)
        for i in range(self.cola_inicial_1):
            dir_i = 1 if i % 2 == 0 else -1
            pos_i = -15.0 - ((i // 2) * 8.0)
            v = self._crear_vehiculo(via_origen=1, tiempo_llegada=0.0, posicion=pos_i, direccion=dir_i)
            self.vehiculos_1.append(v)

        for i in range(self.cola_inicial_2):
            dir_i = 1 if i % 2 == 0 else -1
            pos_i = -15.0 - ((i // 2) * 8.0)
            v = self._crear_vehiculo(via_origen=2, tiempo_llegada=0.0, posicion=pos_i, direccion=dir_i)
            self.vehiculos_2.append(v)

        # Contadores de desempeño
        self.vehiculos_atendidos_1: int = 0
        self.vehiculos_atendidos_2: int = 0
        self.tiempos_espera_1: List[float] = []
        self.tiempos_espera_2: List[float] = []

        # Histórico temporal para análisis y gráficos
        self.historial: Dict[str, List[float]] = {
            "tiempo": [0.0],
            "cola_1": [self.cola_1],
            "cola_2": [self.cola_2],
            "tasa_llegada_1": [self.lambda_1],
            "tasa_llegada_2": [self.lambda_2],
            "tasa_salida_1": [self.mu_sat_1],
            "tasa_salida_2": [0.0],
            "derivada_q1": [self.lambda_1 - self.mu_sat_1],
            "derivada_q2": [self.lambda_2],
            "fase": [self.fase_actual.value],
            "luz_1": ["VERDE"],
            "luz_2": ["ROJO"]
        }

    def _obtener_tasa_descarga(self) -> Tuple[float, float, str, str]:
        """
        Determina las tasas instantáneas de descarga mu_1 y mu_2
        y el estado visual de cada luz según la fase actual.
        """
        if self.fase_actual == FaseSemaforo.VERDE_VIA_1:
            return self.mu_sat_1, 0.0, "VERDE", "ROJO"
        elif self.fase_actual == FaseSemaforo.AMARILLO_VIA_1:
            return 0.35 * self.mu_sat_1, 0.0, "AMARILLO", "ROJO"
        elif self.fase_actual == FaseSemaforo.TODO_ROJO_1:
            return 0.0, 0.0, "ROJO", "ROJO"
        elif self.fase_actual == FaseSemaforo.VERDE_VIA_2:
            return 0.0, self.mu_sat_2, "ROJO", "VERDE"
        elif self.fase_actual == FaseSemaforo.AMARILLO_VIA_2:
            return 0.0, 0.35 * self.mu_sat_2, "ROJO", "AMARILLO"
        elif self.fase_actual == FaseSemaforo.TODO_ROJO_2:
            return 0.0, 0.0, "ROJO", "ROJO"
        return 0.0, 0.0, "ROJO", "ROJO"

    def _duracion_fase_actual(self) -> float:
        """Devuelve la duración planificada de la fase semafórica actual."""
        if self.fase_actual == FaseSemaforo.VERDE_VIA_1:
            return self.config.tiempo_verde_1
        elif self.fase_actual == FaseSemaforo.AMARILLO_VIA_1:
            return self.config.tiempo_amarillo_1
        elif self.fase_actual == FaseSemaforo.TODO_ROJO_1:
            return self.config.tiempo_todo_rojo
        elif self.fase_actual == FaseSemaforo.VERDE_VIA_2:
            return self.config.tiempo_verde_2
        elif self.fase_actual == FaseSemaforo.AMARILLO_VIA_2:
            return self.config.tiempo_amarillo_2
        elif self.fase_actual == FaseSemaforo.TODO_ROJO_2:
            return self.config.tiempo_todo_rojo
        return 30.0

    def _siguiente_fase(self) -> FaseSemaforo:
        """Transición de autómata de estados finitos del ciclo semafórico."""
        transiciones = {
            FaseSemaforo.VERDE_VIA_1: FaseSemaforo.AMARILLO_VIA_1,
            FaseSemaforo.AMARILLO_VIA_1: FaseSemaforo.TODO_ROJO_1,
            FaseSemaforo.TODO_ROJO_1: FaseSemaforo.VERDE_VIA_2,
            FaseSemaforo.VERDE_VIA_2: FaseSemaforo.AMARILLO_VIA_2,
            FaseSemaforo.AMARILLO_VIA_2: FaseSemaforo.TODO_ROJO_2,
            FaseSemaforo.TODO_ROJO_2: FaseSemaforo.VERDE_VIA_1,
        }
        return transiciones[self.fase_actual]

    def avanzar_paso(self, dt: float = 1.0) -> None:
        """
        Avanza la simulación en un delta de tiempo dt (segundos),
        integrando numéricamente la ecuación diferencial Q'(t) = λ - μ
        y actualizando los estados de los vehículos.
        """
        self.tiempo_actual += dt
        self.tiempo_en_fase += dt

        # Control de fase del semáforo
        duracion_fase = self._duracion_fase_actual()
        if self.tiempo_en_fase >= duracion_fase:
            self.fase_actual = self._siguiente_fase()
            self.tiempo_en_fase = 0.0

        mu_1, mu_2, luz_1, luz_2 = self._obtener_tasa_descarga()

        # Generación de llegadas vehiculares
        # Modelo estocástico de Poisson o tasa continua
        if self.es_estocastico:
            llegadas_1 = 1 if random.random() < (self.lambda_1 * dt) else 0
            llegadas_2 = 1 if random.random() < (self.lambda_2 * dt) else 0
            tasa_llegada_instantanea_1 = llegadas_1 / dt
            tasa_llegada_instantanea_2 = llegadas_2 / dt
        else:
            llegadas_1 = self.lambda_1 * dt
            llegadas_2 = self.lambda_2 * dt
            tasa_llegada_instantanea_1 = self.lambda_1
            tasa_llegada_instantanea_2 = self.lambda_2

        # Registro de nuevos vehículos discretos
        if self.es_estocastico:
            if llegadas_1 > 0:
                dir_1 = 1 if random.random() < 0.55 else -1
                pos_1 = -20.0 - (len([v for v in self.vehiculos_1 if v.estado == EstadoVehiculo.EN_COLA and v.direccion == dir_1]) * 8.0)
                v1 = self._crear_vehiculo(via_origen=1, tiempo_llegada=self.tiempo_actual, posicion=pos_1, direccion=dir_1)
                self.vehiculos_1.append(v1)
            if llegadas_2 > 0:
                dir_2 = 1 if random.random() < 0.55 else -1
                pos_2 = -20.0 - (len([v for v in self.vehiculos_2 if v.estado == EstadoVehiculo.EN_COLA and v.direccion == dir_2]) * 8.0)
                v2 = self._crear_vehiculo(via_origen=2, tiempo_llegada=self.tiempo_actual, posicion=pos_2, direccion=dir_2)
                self.vehiculos_2.append(v2)

        # Integración numérica de la ecuación diferencial: Q(t + dt) = Q(t) + Q'(t)*dt
        # con restricción de frontera de no negatividad Q >= 0
        dQ1_dt = tasa_llegada_instantanea_1 - (mu_1 if self.cola_1 > 0 else min(tasa_llegada_instantanea_1, mu_1))
        nueva_cola_1 = max(0.0, self.cola_1 + (tasa_llegada_instantanea_1 - mu_1) * dt)

        dQ2_dt = tasa_llegada_instantanea_2 - (mu_2 if self.cola_2 > 0 else min(tasa_llegada_instantanea_2, mu_2))
        nueva_cola_2 = max(0.0, self.cola_2 + (tasa_llegada_instantanea_2 - mu_2) * dt)

        # Salida de vehículos discretos durante fases permitidas
        if mu_1 > 0 and len(self.vehiculos_1) > 0:
            salidas_potenciales_1 = mu_1 * dt
            prob_salida = salidas_potenciales_1 if self.es_estocastico else 1.0
            if (not self.es_estocastico) or (random.random() < prob_salida):
                en_espera_1 = [v for v in self.vehiculos_1 if v.estado == EstadoVehiculo.EN_COLA]
                if en_espera_1:
                    atendido = en_espera_1[0]
                    atendido.estado = EstadoVehiculo.COMPLETADO
                    atendido.tiempo_salida = self.tiempo_actual
                    tiempo_espera = max(0.0, self.tiempo_actual - atendido.tiempo_llegada)
                    self.tiempos_espera_1.append(tiempo_espera)
                    self.vehiculos_atendidos_1 += 1

        if mu_2 > 0 and len(self.vehiculos_2) > 0:
            salidas_potenciales_2 = mu_2 * dt
            prob_salida = salidas_potenciales_2 if self.es_estocastico else 1.0
            if (not self.es_estocastico) or (random.random() < prob_salida):
                en_espera_2 = [v for v in self.vehiculos_2 if v.estado == EstadoVehiculo.EN_COLA]
                if en_espera_2:
                    atendido = en_espera_2[0]
                    atendido.estado = EstadoVehiculo.COMPLETADO
                    atendido.tiempo_salida = self.tiempo_actual
                    tiempo_espera = max(0.0, self.tiempo_actual - atendido.tiempo_llegada)
                    self.tiempos_espera_2.append(tiempo_espera)
                    self.vehiculos_atendidos_2 += 1

        self.cola_1 = nueva_cola_1
        self.cola_2 = nueva_cola_2

        # Actualizar posiciones visuales para vehículos en cola y cruzando
        self._actualizar_cinematica_vehiculos(dt)

        # Almacenar en histórico
        self.historial["tiempo"].append(self.tiempo_actual)
        self.historial["cola_1"].append(self.cola_1)
        self.historial["cola_2"].append(self.cola_2)
        self.historial["tasa_llegada_1"].append(tasa_llegada_instantanea_1)
        self.historial["tasa_llegada_2"].append(tasa_llegada_instantanea_2)
        self.historial["tasa_salida_1"].append(mu_1)
        self.historial["tasa_salida_2"].append(mu_2)
        self.historial["derivada_q1"].append(dQ1_dt)
        self.historial["derivada_q2"].append(dQ2_dt)
        self.historial["fase"].append(self.fase_actual.value)
        self.historial["luz_1"].append(luz_1)
        self.historial["luz_2"].append(luz_2)

    def _actualizar_cinematica_vehiculos(self, dt: float) -> None:
        """Actualiza distancias y velocidades de vehículos para animación visual."""
        # Vía 1
        cola_idx = 0
        for v in self.vehiculos_1:
            if v.estado == EstadoVehiculo.EN_COLA:
                pos_meta = -12.0 - (cola_idx * 7.0)
                if v.posicion < pos_meta:
                    v.posicion = min(pos_meta, v.posicion + 8.0 * dt)
                cola_idx += 1
            elif v.estado == EstadoVehiculo.COMPLETADO:
                v.posicion += 12.0 * dt

        # Vía 2
        cola_idx = 0
        for v in self.vehiculos_2:
            if v.estado == EstadoVehiculo.EN_COLA:
                pos_meta = -12.0 - (cola_idx * 7.0)
                if v.posicion < pos_meta:
                    v.posicion = min(pos_meta, v.posicion + 8.0 * dt)
                cola_idx += 1
            elif v.estado == EstadoVehiculo.COMPLETADO:
                v.posicion += 12.0 * dt

    def simular_horizonte(self, duracion_total_segundos: float, dt: float = 1.0) -> Dict[str, Any]:
        """
        Ejecuta la simulación completa de forma continua hasta alcanzar
        el horizonte especificado de tiempo.
        """
        pasos = int(duracion_total_segundos / dt)
        for _ in range(pasos):
            self.avanzar_paso(dt)
        return self.obtener_resumen_metricas()

    def obtener_resumen_metricas(self) -> Dict[str, Any]:
        """
        Calcula indicadores clave de rendimiento (KPIs) del sistema
        bajo normas de ingeniería de tránsito e ingeniería industrial.
        """
        cola_promedio_1 = (
            sum(self.historial["cola_1"]) / len(self.historial["cola_1"])
            if self.historial["cola_1"] else 0.0
        )
        cola_promedio_2 = (
            sum(self.historial["cola_2"]) / len(self.historial["cola_2"])
            if self.historial["cola_2"] else 0.0
        )
        cola_maxima_1 = max(self.historial["cola_1"]) if self.historial["cola_1"] else 0.0
        cola_maxima_2 = max(self.historial["cola_2"]) if self.historial["cola_2"] else 0.0

        espera_promedio_1 = (
            sum(self.tiempos_espera_1) / len(self.tiempos_espera_1)
            if self.tiempos_espera_1 else (cola_promedio_1 / max(0.01, self.lambda_1))
        )
        espera_promedio_2 = (
            sum(self.tiempos_espera_2) / len(self.tiempos_espera_2)
            if self.tiempos_espera_2 else (cola_promedio_2 / max(0.01, self.lambda_2))
        )

        espera_promedio_global = (
            (espera_promedio_1 * self.lambda_1 + espera_promedio_2 * self.lambda_2)
            / max(0.001, (self.lambda_1 + self.lambda_2))
        )

        total_vehiculos_atendidos = self.vehiculos_atendidos_1 + self.vehiculos_atendidos_2

        # Retraso total acumulado (Área bajo la curva de cola: integral de Q(t) dt)
        retraso_total_1 = sum(self.historial["cola_1"]) * 1.0
        retraso_total_2 = sum(self.historial["cola_2"]) * 1.0
        retraso_total_global = retraso_total_1 + retraso_total_2

        return {
            "tiempo_simulado": self.tiempo_actual,
            "cola_promedio_1": cola_promedio_1,
            "cola_promedio_2": cola_promedio_2,
            "cola_promedio_total": (cola_promedio_1 + cola_promedio_2) / 2.0,
            "cola_maxima_1": cola_maxima_1,
            "cola_maxima_2": cola_maxima_2,
            "espera_promedio_1": espera_promedio_1,
            "espera_promedio_2": espera_promedio_2,
            "espera_promedio_global": espera_promedio_global,
            "vehiculos_atendidos_1": self.vehiculos_atendidos_1,
            "vehiculos_atendidos_2": self.vehiculos_atendidos_2,
            "total_atendidos": total_vehiculos_atendidos,
            "retraso_total_acumulado": retraso_total_global,
            "rendimiento_por_hora": (total_vehiculos_atendidos / max(1.0, self.tiempo_actual)) * 3600.0,
        }

    def obtener_estado_visual(self) -> Dict[str, Any]:
        """Devuelve el estado instantáneo para renderizado de la UI."""
        mu_1, mu_2, luz_1, luz_2 = self._obtener_tasa_descarga()
        duracion_fase = self._duracion_fase_actual()
        tiempo_restante_fase = max(0.0, duracion_fase - self.tiempo_en_fase)

        return {
            "tiempo_actual": self.tiempo_actual,
            "fase_actual": self.fase_actual.value,
            "tiempo_en_fase": self.tiempo_en_fase,
            "duracion_fase": duracion_fase,
            "tiempo_restante_fase": tiempo_restante_fase,
            "luz_1": luz_1,
            "luz_2": luz_2,
            "cola_1": self.cola_1,
            "cola_2": self.cola_2,
            "cola_discreta_1": len([v for v in self.vehiculos_1 if v.estado == EstadoVehiculo.EN_COLA]),
            "cola_discreta_2": len([v for v in self.vehiculos_2 if v.estado == EstadoVehiculo.EN_COLA]),
            "vehiculos_1": [
                {
                    "id": v.id_vehiculo,
                    "pos": v.posicion,
                    "estado": v.estado.value,
                    "tipo": v.tipo,
                    "color": v.color,
                    "direccion": v.direccion,
                    "carril": v.carril,
                    "largo_m": v.largo_m,
                    "ancho_m": v.ancho_m,
                    "velocidad": v.velocidad
                }
                for v in self.vehiculos_1 if v.estado != EstadoVehiculo.COMPLETADO or v.posicion < 70.0
            ],
            "vehiculos_2": [
                {
                    "id": v.id_vehiculo,
                    "pos": v.posicion,
                    "estado": v.estado.value,
                    "tipo": v.tipo,
                    "color": v.color,
                    "direccion": v.direccion,
                    "carril": v.carril,
                    "largo_m": v.largo_m,
                    "ancho_m": v.ancho_m,
                    "velocidad": v.velocidad
                }
                for v in self.vehiculos_2 if v.estado != EstadoVehiculo.COMPLETADO or v.posicion < 70.0
            ],
            "atendidos_1": self.vehiculos_atendidos_1,
            "atendidos_2": self.vehiculos_atendidos_2,
        }
