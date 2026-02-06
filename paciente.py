"""
CLASE PACIENTE
==============
Representa a cada paciente individual en la simulación
"""

import random
import numpy as np
from datetime import datetime, timedelta
import config

class Paciente:
    """
    Representa un paciente individual en el sistema de resonador.
    Contiene todas las métricas y tiempos del flujo del paciente.
    """
    
    # Contador global de pacientes
    contador_id = 0
    
    def __init__(self, turno_asignado, tiempo_simulacion_inicio):
        """
        Inicializa un nuevo paciente
        
        Args:
            turno_asignado: Hora del turno en minutos desde inicio de simulación
            tiempo_simulacion_inicio: Tiempo de inicio de la simulación (datetime)
        """
        Paciente.contador_id += 1
        self.id = Paciente.contador_id
        
        # Turno asignado
        self.turno_asignado = turno_asignado
        self.hora_turno = tiempo_simulacion_inicio + timedelta(minutes=turno_asignado)
        
        # Estado actual
        self.estado = 'LLEGADA'
        self.posicion = list(config.WAYPOINTS['entrada'])  # Lista para poder modificar
        self.posicion_objetivo = None  # Hacia dónde se mueve
        self.esta_moviendo = False  # Si está en movimiento
        
        # Ruta de waypoints a seguir
        self.ruta_actual = []
        self.waypoint_actual_index = 0
        
        # ====================================================================
        # MÉTRICAS DEL PACIENTE (lo que queremos medir)
        # ====================================================================
        
        # 1. Tiempo de llegada (desviación del turno)
        self.desvio_llegada = self._calcular_desvio_llegada()
        self.tiempo_llegada_real = turno_asignado + self.desvio_llegada
        self.llego_temprano = self.desvio_llegada < 0
        self.llego_tarde = self.desvio_llegada > 0
        
        # 2. Tiempo de validación en mesa
        self.tiempo_validacion = max(3.0, np.random.normal(
            config.VALIDACION_MESA['media'],
            config.VALIDACION_MESA['desviacion']
        ))
        
        # 3. Tiempo en cambiador (entrada)
        self.tiempo_cambiador_entrada = max(3.0, np.random.normal(
            config.CAMBIADOR_ENTRADA['media'],
            config.CAMBIADOR_ENTRADA['desviacion']
        ))
        
        # 4. Tipo de estudio y tiempo de scan
        self.tipo_estudio = self._seleccionar_tipo_estudio()
        self.tiempo_scan = config.TIPOS_ESTUDIOS[self.tipo_estudio]['duracion']
        self.tiempo_posicionamiento = max(2.0, np.random.normal(
            config.POSICIONAMIENTO['media'],
            config.POSICIONAMIENTO['desviacion']
        ))
        self.tiempo_total_resonador = self.tiempo_scan + self.tiempo_posicionamiento
        
        # 5. Tiempo en cambiador (salida)
        self.tiempo_cambiador_salida = max(3.0, np.random.normal(
            config.CAMBIADOR_SALIDA['media'],
            config.CAMBIADOR_SALIDA['desviacion']
        ))
        
        # 6. Margen de error (limpieza/preparación)
        self.margen_error = config.MARGEN_ERROR
        
        # ====================================================================
        # TIEMPOS ACUMULADOS (para tracking en tiempo real)
        # ====================================================================
        self.tiempo_inicio_atencion = None  # Cuando empieza a ser atendido
        self.tiempo_fin_atencion = None     # Cuando termina todo el proceso
        self.tiempo_espera_acumulado = 0    # Tiempo perdido esperando
        
        # Timestamps de cada etapa
        self.timestamp_llegada = None
        self.timestamp_inicio_validacion = None
        self.timestamp_fin_validacion = None
        self.timestamp_inicio_cambiador_in = None
        self.timestamp_fin_cambiador_in = None
        self.timestamp_inicio_resonador = None
        self.timestamp_fin_resonador = None
        self.timestamp_inicio_cambiador_out = None
        self.timestamp_fin_cambiador_out = None
        self.timestamp_salida = None
        
        # Tiempo total de servicio (se calcula al final)
        self.tiempo_total_servicio = 0
        
        # ====================================================================
        # VARIABLES DE CONTROL
        # ====================================================================
        self.completado = False
        self.tiempo_actual_en_etapa = 0  # Cuánto lleva en la etapa actual
        self.objetivo_movimiento = None   # Hacia dónde se está moviendo
        
    def _calcular_desvio_llegada(self):
        """
        Calcula el desvío de llegada según las probabilidades:
        - 20% llega 5 min antes
        - 30% llega a horario
        - 50% llega entre 5-10 min tarde
        """
        rand = random.random()
        
        if rand < 0.20:
            # 20% llega 5 min antes
            return -5
        elif rand < 0.50:  # 20% + 30% = 50%
            # 30% llega puntual
            return 0
        else:
            # 50% llega entre 5-10 min tarde
            return random.uniform(5, 10)
    
    def _seleccionar_tipo_estudio(self):
        """
        Selecciona el tipo de estudio según las probabilidades definidas
        """
        rand = random.random()
        acumulado = 0
        
        for tipo, datos in config.TIPOS_ESTUDIOS.items():
            acumulado += datos['probabilidad']
            if rand <= acumulado:
                return tipo
        
        # Fallback (no debería llegar aquí)
        return 'Otros'
    
    def calcular_tiempo_total_servicio(self):
        """
        Calcula el tiempo total de servicio del paciente
        (desde llegada hasta salida)
        """
        if self.timestamp_llegada and self.timestamp_salida:
            delta = self.timestamp_salida - self.timestamp_llegada
            self.tiempo_total_servicio = delta.total_seconds() / 60  # en minutos
        return self.tiempo_total_servicio
    
    def obtener_metricas(self):
        """
        Retorna un diccionario con todas las métricas del paciente
        """
        return {
            'id': self.id,
            'turno_asignado': self.turno_asignado,
            'desvio_llegada': round(self.desvio_llegada, 2),
            'llego_temprano': self.llego_temprano,
            'llego_tarde': self.llego_tarde,
            'tiempo_validacion': round(self.tiempo_validacion, 2),
            'tiempo_cambiador_entrada': round(self.tiempo_cambiador_entrada, 2),
            'tipo_estudio': self.tipo_estudio,
            'tiempo_scan': round(self.tiempo_scan, 2),
            'tiempo_posicionamiento': round(self.tiempo_posicionamiento, 2),
            'tiempo_total_resonador': round(self.tiempo_total_resonador, 2),
            'tiempo_cambiador_salida': round(self.tiempo_cambiador_salida, 2),
            'tiempo_espera_acumulado': round(self.tiempo_espera_acumulado, 2),
            'tiempo_total_servicio': round(self.tiempo_total_servicio, 2),
            'estado': self.estado,
            'completado': self.completado
        }
    
    def definir_ruta(self, waypoints):
        """
        Define una ruta de waypoints para que el paciente siga
        
        Args:
            waypoints: Lista de nombres de waypoints en config.WAYPOINTS
        """
        self.ruta_actual = [config.WAYPOINTS[wp] for wp in waypoints]
        self.waypoint_actual_index = 0
        if self.ruta_actual:
            self.posicion_objetivo = self.ruta_actual[0]
            self.esta_moviendo = True
    
    def actualizar_movimiento(self, delta_tiempo):
        """
        Actualiza la posición del paciente moviéndolo suavemente hacia su objetivo
        
        Args:
            delta_tiempo: Tiempo transcurrido en segundos (tiempo real, no simulado)
        
        Returns:
            True si llegó al waypoint objetivo, False si aún se está moviendo
        """
        if not self.esta_moviendo or self.posicion_objetivo is None:
            return False
        
        # Calcular dirección y distancia
        dx = self.posicion_objetivo[0] - self.posicion[0]
        dy = self.posicion_objetivo[1] - self.posicion[1]
        distancia = (dx**2 + dy**2)**0.5
        
        # Si ya llegó al waypoint
        if distancia < 5:  # Threshold de 5 píxeles
            self.posicion = list(self.posicion_objetivo)
            
            # Avanzar al siguiente waypoint
            self.waypoint_actual_index += 1
            if self.waypoint_actual_index < len(self.ruta_actual):
                self.posicion_objetivo = self.ruta_actual[self.waypoint_actual_index]
            else:
                # Terminó la ruta
                self.esta_moviendo = False
                self.posicion_objetivo = None
                return True
            
            return False
        
        # Moverse hacia el objetivo
        velocidad = config.VELOCIDAD_PACIENTE  # píxeles por segundo
        paso = velocidad * delta_tiempo
        
        # Normalizar y aplicar velocidad
        factor = paso / distancia
        self.posicion[0] += dx * factor
        self.posicion[1] += dy * factor
        
        return False
    
    def __repr__(self):
        return f"Paciente #{self.id} - {self.tipo_estudio} - Estado: {self.estado}"
