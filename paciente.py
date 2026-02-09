"""Clase Paciente V2.1"""
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
        
        # Estado y posición
        self.estado = 'ESPERANDO'
        self.posicion = list(config.WAYPOINTS['esperando'])
        self.ruta = []
        self.idx_ruta = 0
        self.moviendo = False
        
        # Métricas (generadas al crear paciente)
        self.desvio_llegada = self._calcular_desvio()
        self.tiempo_validacion = max(2, np.random.normal(
            config.VALIDACION_MESA['media'], config.VALIDACION_MESA['desviacion']))
        self.tiempo_box = max(3, np.random.normal(
            config.BOX_CAMBIO['media'], config.BOX_CAMBIO['desviacion']))
        self.tipo_estudio = self._seleccionar_estudio()
        self.tiempo_scan = config.TIPOS_ESTUDIOS[self.tipo_estudio]['duracion']
        self.tiempo_posicionamiento = max(1, np.random.normal(
            config.POSICIONAMIENTO['media'], config.POSICIONAMIENTO['desviacion']))
        self.tiempo_total_resonador = self.tiempo_scan + self.tiempo_posicionamiento
        
        # Timestamps
        self.ts_inicio = None
        self.ts_fin = None
        self.tiempo_en_etapa = 0
        self.tiempo_total = 0
        
    def _calcular_desvio(self):
        r = random.random()
        if r < 0.20: return -5
        elif r < 0.50: return 0
        else: return random.uniform(5, 10)
    
    def _seleccionar_estudio(self):
        r, acum = random.random(), 0
        for tipo, datos in config.TIPOS_ESTUDIOS.items():
            acum += datos['probabilidad']
            if r <= acum: return tipo
        return 'Otros'
    
    def definir_ruta(self, waypoints):
        self.ruta = [config.WAYPOINTS[wp] for wp in waypoints]
        self.idx_ruta = 0
        if self.ruta:
            self.moviendo = True
    
    def actualizar_movimiento(self, dt):
        if not self.moviendo or not self.ruta: return False
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
        
        vel = config.VELOCIDAD_PACIENTE * dt
        factor = vel / dist
        self.posicion[0] += dx * factor
        self.posicion[1] += dy * factor
        return False
