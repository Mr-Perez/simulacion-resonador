"""Motor de Simulación V3.0 - Grilla Flexible con Llegadas Realistas"""
from datetime import datetime, timedelta
import config
from paciente import Paciente

class SimuladorResonador:
    def __init__(self):
        self.fecha_inicio = datetime.now().replace(hour=config.HORA_INICIO, minute=0, second=0, microsecond=0)
        self.tiempo_actual = 0.0
        self.datetime_actual = self.fecha_inicio
        
        self.pacientes_programados = []
        self.pacientes_en_espera = []
        self.paciente_en_validacion = None
        self.paciente_en_box = None
        self.paciente_en_resonador = None
        self.pacientes_completados = []
        
        self.pausada = False
        self.finalizada = False
        
        self._generar_agenda_flexible()
        
    def _generar_agenda_flexible(self):
        """Genera turnos con grilla flexible"""
        turno_actual = 0.0
        numero_paciente = 1
        
        while turno_actual < 690:
            p = Paciente(turno_actual, self.fecha_inicio)
            p.id = numero_paciente
            p.turno_asignado = turno_actual
            
            # Tiempo estimado para siguiente turno
            tiempo_estimado = (
                p.tiempo_validacion +
                2.0 +
                p.tiempo_box +
                p.tiempo_total_resonador +
                2.0 +
                p.tiempo_salida
            )
            
            # Hora de llegada REAL = turno + desvío
            p.hora_llegada_real = turno_actual + p.desvio_llegada
            p.estado = 'PROGRAMADO'
            
            self.pacientes_programados.append(p)
            
            # GRILLA FLEXIBLE
            turno_actual += tiempo_estimado
            numero_paciente += 1
        
        print(f"✓ Agenda: {len(self.pacientes_programados)} pacientes")
        print(f"  Turnos: {self.pacientes_programados[0].turno_asignado:.0f} - {self.pacientes_programados[-1].turno_asignado:.0f} min")
        
    def actualizar(self, delta_sim, delta_real, multiplicador_velocidad=1.0):
        if self.pausada or self.finalizada:
            return
        
        self.tiempo_actual += delta_sim
        self.datetime_actual = self.fecha_inicio + timedelta(minutes=self.tiempo_actual)
        
        # 1. Procesar llegadas
        self._procesar_llegadas()
        
        # 2. Actualizar movimientos
        todos = self.pacientes_en_espera.copy()
        if self.paciente_en_validacion:
            todos.append(self.paciente_en_validacion)
        if self.paciente_en_box:
            todos.append(self.paciente_en_box)
        if self.paciente_en_resonador:
            todos.append(self.paciente_en_resonador)
        
        for p in todos:
            if p.moviendo:
                p.actualizar_movimiento(delta_real, multiplicador_velocidad)
        
        # 3. Actualizar tiempos
        if self.paciente_en_validacion:
            self.paciente_en_validacion.tiempo_en_etapa += delta_sim
        if self.paciente_en_box:
            self.paciente_en_box.tiempo_en_etapa += delta_sim
        if self.paciente_en_resonador:
            self.paciente_en_resonador.tiempo_en_etapa += delta_sim
        
        # 4. Gestionar flujo
        self._gestionar_flujo()
        
        # 5. Verificar fin
        if (not self.pacientes_programados and 
            not self.pacientes_en_espera and
            not self.paciente_en_validacion and
            not self.paciente_en_box and
            not self.paciente_en_resonador):
            self.finalizada = True
    
    def _procesar_llegadas(self):
        """Procesar llegadas - SOLO 1 paciente por actualización"""
        if not self.pacientes_programados:
            return
        
        # Ordenar por hora de llegada
        self.pacientes_programados.sort(key=lambda p: p.hora_llegada_real)
        
        # Procesar SOLO 1 paciente si ya llegó su hora
        if self.pacientes_programados and self.tiempo_actual >= self.pacientes_programados[0].hora_llegada_real:
            p = self.pacientes_programados.pop(0)
            p.estado = 'LLEGADA'
            p.ts_inicio = self.datetime_actual
            p.definir_ruta(['esperando', 'entrada', 'sala_espera'])
            self.pacientes_en_espera.append(p)
    
    def _gestionar_flujo(self):
        """Gestiona el flujo de pacientes"""
        
        # Sala → Mesa
        if not self.paciente_en_validacion and self.pacientes_en_espera:
            for p in self.pacientes_en_espera:
                if not p.moviendo and p.estado == 'LLEGADA':
                    self.pacientes_en_espera.remove(p)
                    p.estado = 'VALIDACION'
                    p.tiempo_en_etapa = 0
                    p.definir_ruta(['sala_espera', 'mesa'])
                    self.paciente_en_validacion = p
                    break
        
        # Mesa → Box (ruta completa)
        if self.paciente_en_validacion and not self.paciente_en_validacion.moviendo:
            p = self.paciente_en_validacion
            if p.tiempo_en_etapa >= p.tiempo_validacion:
                if not self.paciente_en_box:
                    self.paciente_en_validacion = None
                    p.estado = 'BOX'
                    p.tiempo_en_etapa = 0
                    p.definir_ruta(['salida_sala', 'pasillo_v', 'pasillo_v_arriba', 
                                   'pasillo_h', 'pasillo_h_derecha', 'entrada_vestuario', 
                                   'vestuario', 'box'])
                    self.paciente_en_box = p
        
        # Box → Resonador
        if self.paciente_en_box and not self.paciente_en_box.moviendo:
            p = self.paciente_en_box
            if p.tiempo_en_etapa >= p.tiempo_box:
                if not self.paciente_en_resonador:
                    self.paciente_en_box = None
                    p.estado = 'RESONADOR'
                    p.tiempo_en_etapa = 0
                    p.definir_ruta(['vuelta_vestuario', 'entrada_resonancia', 
                                   'resonancia', 'resonador'])
                    self.paciente_en_resonador = p
        
        # Resonador → Completado
        if self.paciente_en_resonador and not self.paciente_en_resonador.moviendo:
            p = self.paciente_en_resonador
            if p.tiempo_en_etapa >= p.tiempo_total_resonador:
                self.paciente_en_resonador = None
                p.estado = 'COMPLETADO'
                p.ts_fin = self.datetime_actual
                if p.ts_inicio:
                    p.tiempo_total = (p.ts_fin - p.ts_inicio).total_seconds() / 60
                p.definir_ruta(['salida'])
                self.pacientes_completados.append(p)
    
    def obtener_paciente_activo(self):
        if self.paciente_en_resonador:
            return self.paciente_en_resonador
        if self.paciente_en_box:
            return self.paciente_en_box
        if self.paciente_en_validacion:
            return self.paciente_en_validacion
        if self.pacientes_en_espera:
            return self.pacientes_en_espera[0]
        return None
    
    def todos_los_pacientes(self):
        pacientes = self.pacientes_en_espera.copy()
        if self.paciente_en_validacion:
            pacientes.append(self.paciente_en_validacion)
        if self.paciente_en_box:
            pacientes.append(self.paciente_en_box)
        if self.paciente_en_resonador:
            pacientes.append(self.paciente_en_resonador)
        return pacientes
    
    def obtener_estadisticas_dia(self):
        if not self.pacientes_completados:
            return {
                'estudios_por_tipo': {},
                'tiempo_promedio_total': 0,
                'total_pacientes': 0,
                'ultimo_turno_min': 0,
                'ultimo_turno_hora': '00:00',
                'hora_finalizacion_min': 0,
                'hora_finalizacion_hora': '00:00'
            }
        
        estudios = {}
        tiempos = []
        for p in self.pacientes_completados:
            estudios[p.tipo_estudio] = estudios.get(p.tipo_estudio, 0) + 1
            tiempo = p.calcular_tiempo_circuito()
            tiempos.append(tiempo)
        
        ultimo = self.pacientes_completados[-1]
        ultimo_turno_min = ultimo.turno_asignado
        hora_fin_min = ultimo.hora_llegada_real + ultimo.calcular_tiempo_circuito()
        
        def min_a_hora(minutos):
            horas = 8 + int(minutos // 60)
            mins = int(minutos % 60)
            return f"{horas:02d}:{mins:02d}"
        
        return {
            'estudios_por_tipo': estudios,
            'tiempo_promedio_total': sum(tiempos) / len(tiempos) if tiempos else 0,
            'total_pacientes': len(self.pacientes_completados),
            'ultimo_turno_min': ultimo_turno_min,
            'ultimo_turno_hora': min_a_hora(ultimo_turno_min),
            'hora_finalizacion_min': hora_fin_min,
            'hora_finalizacion_hora': min_a_hora(hora_fin_min)
        }
    
    def pausar(self):
        self.pausada = True
    
    def reanudar(self):
        self.pausada = False
    
    def reiniciar(self):
        self.__init__()
