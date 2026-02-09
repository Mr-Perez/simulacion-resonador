"""Motor de Simulación V2.1 - Control MANUAL"""
from datetime import datetime, timedelta
import config
from paciente import Paciente

class SimuladorResonador:
    def __init__(self):
        self.fecha_inicio = datetime.now().replace(hour=config.HORA_INICIO, minute=0, second=0, microsecond=0)
        self.tiempo_actual = 0
        self.datetime_actual = self.fecha_inicio
        
        # MODO MANUAL
        self.paciente_actual = None
        self.pacientes_completados = []
        self.numero_paciente = 0
        self.esperando_input = True  # Espera ENTER para comenzar
        
        self.pausada = False
        self.finalizada = False
        
    def crear_siguiente_paciente(self):
        """Crea el siguiente paciente (llamado al presionar ENTER)"""
        if not self.finalizada:
            self.numero_paciente += 1
            turno = (self.numero_paciente - 1) * config.INTERVALO_TURNOS
            self.paciente_actual = Paciente(turno, self.fecha_inicio)
            self.paciente_actual.ts_inicio = self.datetime_actual
            self.esperando_input = False
            # Iniciar flujo correcto
            self._iniciar_flujo()
    
    def _iniciar_flujo(self):
        """Inicia el flujo correcto del paciente"""
        p = self.paciente_actual
        p.estado = 'LLEGADA'
        p.definir_ruta(['esperando', 'entrada', 'sala_espera'])
    
    def actualizar(self, delta_sim, delta_real):
        if self.pausada or self.finalizada or self.esperando_input:
            return
        
        self.tiempo_actual += delta_sim
        self.datetime_actual = self.fecha_inicio + timedelta(minutes=self.tiempo_actual)
        
        if self.paciente_actual:
            # Actualizar movimiento
            self.paciente_actual.actualizar_movimiento(delta_real)
            
            # Actualizar tiempo en etapa
            self.paciente_actual.tiempo_en_etapa += delta_sim
            
            # Gestionar estados
            self._gestionar_estados()
    
    def _gestionar_estados(self):
        p = self.paciente_actual
        
        if p.estado == 'LLEGADA' and not p.moviendo:
            p.estado = 'ESPERA'
            p.definir_ruta(['sala_espera', 'mesa'])
        
        elif p.estado == 'ESPERA' and not p.moviendo:
            p.estado = 'VALIDACION'
            p.tiempo_en_etapa = 0
        
        elif p.estado == 'VALIDACION':
            if p.tiempo_en_etapa >= p.tiempo_validacion:
                p.estado = 'CAMINANDO_PASILLO'
                p.definir_ruta(['salida_sala', 'pasillo_v', 'pasillo_v_arriba', 'pasillo_h', 'pasillo_h_derecha', 'entrada_vestuario', 'vestuario'])
                p.tiempo_en_etapa = 0
        
        elif p.estado == 'CAMINANDO_PASILLO' and not p.moviendo:
            p.estado = 'VESTUARIO'
            p.definir_ruta(['vestuario', 'box'])
        
        elif p.estado == 'VESTUARIO' and not p.moviendo:
            p.estado = 'BOX'
            p.tiempo_en_etapa = 0
        
        elif p.estado == 'BOX':
            if p.tiempo_en_etapa >= p.tiempo_box:
                p.estado = 'RESONADOR'
                p.definir_ruta(['vuelta_vestuario', 'entrada_resonancia', 'resonancia', 'resonador'])
                p.tiempo_en_etapa = 0
        
        elif p.estado == 'RESONADOR':
            if not p.moviendo:
                # Comenzó el scan
                if p.tiempo_en_etapa >= p.tiempo_total_resonador:
                    p.estado = 'SALIDA'
                    p.definir_ruta(['salida'])
                    p.tiempo_en_etapa = 0
        
        elif p.estado == 'SALIDA' and not p.moviendo:
            p.estado = 'COMPLETADO'
            p.ts_fin = self.datetime_actual
            if p.ts_inicio:
                p.tiempo_total = (p.ts_fin - p.ts_inicio).total_seconds() / 60
            self.pacientes_completados.append(p)
            self.paciente_actual = None
            self.esperando_input = True  # Espera siguiente ENTER
    
    def obtener_estadisticas_dia(self):
        if not self.pacientes_completados:
            return {'estudios_por_tipo': {}, 'tiempo_promedio_total': 0}
        
        estudios = {}
        tiempos = []
        for p in self.pacientes_completados:
            estudios[p.tipo_estudio] = estudios.get(p.tipo_estudio, 0) + 1
            tiempos.append(p.tiempo_total)
        
        return {
            'estudios_por_tipo': estudios,
            'tiempo_promedio_total': sum(tiempos) / len(tiempos) if tiempos else 0
        }
    
    def pausar(self):
        self.pausada = True
    
    def reanudar(self):
        self.pausada = False
    
    def reiniciar(self):
        self.__init__()
