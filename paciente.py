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
        
        # Tiempo de salida (vestuario)
        self.tiempo_salida = max(2, np.random.normal(4.0, 1.0))
        
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
    
    def calcular_tiempo_circuito(self):
        """Calcula el tiempo total en el circuito sumando todas las etapas"""
        # SUMA SIMPLE de todos los tiempos (no depende del estado)
        tiempo_total = (
            abs(self.desvio_llegada) +  # Llegada (en valor absoluto)
            self.tiempo_validacion +     # Mesa de atención
            2.0 +                         # Tiempo caminando al vestuario
            self.tiempo_box +             # Box (cambiarse)
            self.tiempo_total_resonador + # Resonador (posicionamiento + scan)
            2.0 +                         # Tiempo saliendo
            self.tiempo_salida            # Vestuario salida
        )
        return tiempo_total
    
    def actualizar_movimiento(self, dt, multiplicador_velocidad=1.0):
        """Actualiza el movimiento del paciente
        
        Args:
            dt: Delta tiempo en segundos
            multiplicador_velocidad: Multiplicador de velocidad (1.0 normal, 2.0 rápido)
        """
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
        
        # Aplicar multiplicador de velocidad
        vel = config.VELOCIDAD_PACIENTE * multiplicador_velocidad * dt
        factor = vel / dist
        self.posicion[0] += dx * factor
        self.posicion[1] += dy * factor
        return False
