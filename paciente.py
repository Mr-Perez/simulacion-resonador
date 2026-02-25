"""Clase Paciente V3.0"""
import random
import numpy as np
from datetime import datetime
import config

class Paciente:
    contador_id = 0
    
    def __init__(self, turno_minutos, datetime_inicio):
        Paciente.contador_id += 1
        self.id = Paciente.contador_id
        self.turno = turno_minutos
        self.turno_asignado = turno_minutos
        
        # Estado y posición
        self.estado = 'ESPERANDO'
        self.posicion = list(config.WAYPOINTS['esperando'])
        self.ruta = []
        self.idx_ruta = 0
        self.moviendo = False
        
        # Métricas - usando los nombres correctos de config.py
        self.desvio_llegada = self._calcular_desvio()
        
        # TIEMPO_VALIDACION es una tupla (min, max)
        min_val, max_val = config.TIEMPO_VALIDACION
        self.tiempo_validacion = random.uniform(min_val, max_val)
        
        # TIEMPO_BOX es una tupla (min, max)
        min_box, max_box = config.TIEMPO_BOX
        self.tiempo_box = random.uniform(min_box, max_box)
        
        # Seleccionar tipo de estudio
        self.tipo_estudio = self._seleccionar_estudio()
        
        # Obtener tiempos del estudio
        estudio_config = config.TIPOS_ESTUDIO[self.tipo_estudio]
        min_scan, max_scan = estudio_config['tiempo_scan']
        self.tiempo_scan = random.uniform(min_scan, max_scan)
        
        min_pos, max_pos = estudio_config['tiempo_posicionamiento']
        self.tiempo_posicionamiento = random.uniform(min_pos, max_pos)
        
        self.tiempo_total_resonador = self.tiempo_scan + self.tiempo_posicionamiento
        
        # Tiempo de salida
        min_salida, max_salida = config.TIEMPO_SALIDA
        self.tiempo_salida = random.uniform(min_salida, max_salida)
        
        # Hora de llegada real (para sistema de grilla flexible)
        self.hora_llegada_real = 0
        
        # Timestamps
        self.ts_inicio = None
        self.ts_fin = None
        self.tiempo_en_etapa = 0
        self.tiempo_total = 0
        
        # Tiempo visual (en segundos reales para visualización)
        self.tiempo_visual_en_etapa = 0.0
        
    def _calcular_desvio(self):
        """Calcula el desvío de llegada según probabilidades"""
        r = random.random()
        if r < config.PROB_LLEGADA_TEMPRANO:
            return -5  # 20% llega 5 min temprano
        elif r < config.PROB_LLEGADA_TEMPRANO + config.PROB_LLEGADA_PUNTUAL:
            return 0   # 30% llega puntual
        else:
            return random.uniform(5, 10)  # 50% llega 5-10 min tarde
    
    def _seleccionar_estudio(self):
        """Selecciona tipo de estudio según probabilidades"""
        r = random.random()
        acum = 0
        for tipo, datos in config.TIPOS_ESTUDIO.items():
            acum += datos['probabilidad']
            if r <= acum:
                return tipo
        return 'Otros'
    
    def definir_ruta(self, waypoints):
        """Define la ruta del paciente"""
        self.ruta = [config.WAYPOINTS[wp] for wp in waypoints]
        self.idx_ruta = 0
        if self.ruta:
            self.moviendo = True
    
    def calcular_tiempo_circuito(self):
        """Calcula el tiempo total en el circuito"""
        tiempo_total = (
            abs(self.desvio_llegada) +
            self.tiempo_validacion +
            2.0 +  # Camino al vestuario
            self.tiempo_box +
            self.tiempo_total_resonador +
            2.0 +  # Camino salida
            self.tiempo_salida
        )
        return tiempo_total
    
    def actualizar_movimiento(self, dt, multiplicador_velocidad=1.0):
        """Actualiza el movimiento del paciente"""
        if not self.moviendo or not self.ruta:
            return False
        
        objetivo = self.ruta[self.idx_ruta]
        dx = objetivo[0] - self.posicion[0]
        dy = objetivo[1] - self.posicion[1]
        dist = (dx**2 + dy**2)**0.5
        
        if dist < 5:
            self.posicion = list(objetivo)
            self.idx_ruta += 1
            if self.idx_ruta >= len(self.ruta):
                self.moviendo = False
                return True
            return False
        
        vel = config.VELOCIDAD_PACIENTE * multiplicador_velocidad * dt
        factor = vel / dist
        self.posicion[0] += dx * factor
        self.posicion[1] += dy * factor
        return False
