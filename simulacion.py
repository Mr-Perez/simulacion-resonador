"""Motor de Simulación V3.0 - GRILLA FLEXIBLE con llegadas realistas"""
from datetime import datetime, timedelta
import config
from paciente import Paciente

class SimuladorResonador:
    def __init__(self):
        self.fecha_inicio = datetime.now().replace(hour=config.HORA_INICIO, minute=0, second=0, microsecond=0)
        self.tiempo_actual = 0  # Minutos desde inicio
        self.datetime_actual = self.fecha_inicio
        
        # SISTEMA DE GRILLA FLEXIBLE
        self.pacientes_programados = []  # Pacientes con turno asignado
        self.pacientes_en_espera = []    # En sala de espera
        self.paciente_en_validacion = None
        self.paciente_en_vestuario = None
        self.paciente_en_box = None
        self.paciente_en_resonador = None
        self.pacientes_completados = []
        
        self.pausada = False
        self.finalizada = False
        
        # Generar agenda del día con GRILLA FLEXIBLE
        self._generar_agenda_flexible()
        
    def _generar_agenda_flexible(self):
        """Genera turnos con grilla flexible (cada turno cuando termina el anterior)
        
        LÓGICA:
        - Paciente 1: Turno = 0 min
        - Paciente 2: Turno = 0 + tiempo_estimado_paciente_1
        - Paciente 3: Turno = turno_2 + tiempo_estimado_paciente_2
        - ...
        - Hasta llenar la jornada (~720 min)
        """
        turno_actual = 0.0
        numero_paciente = 1
        
        # Generar pacientes hasta llenar la jornada
        while turno_actual < 690:  # Último turno antes de las 19:30
            # Crear paciente con turno asignado
            p = Paciente(turno_actual, self.fecha_inicio)
            p.id = numero_paciente
            p.turno_asignado = turno_actual
            
            # Calcular tiempo ESTIMADO de servicio para asignar siguiente turno
            # (Este es el "core" del sistema: anticipar cuánto demorará)
            tiempo_estimado = (
                p.tiempo_validacion +
                2.0 +  # Camino al vestuario
                p.tiempo_box +
                p.tiempo_total_resonador +
                2.0 +  # Camino salida
                p.tiempo_salida
            )
            
            # Calcular hora de llegada REAL (turno + desvío)
            # 20% temprano, 30% puntual, 50% tarde
            p.hora_llegada_real = turno_actual + p.desvio_llegada
            p.estado = 'PROGRAMADO'
            
            self.pacientes_programados.append(p)
            
            # GRILLA FLEXIBLE: Siguiente turno = este turno + tiempo estimado
            turno_actual += tiempo_estimado
            numero_paciente += 1
        
        print(f"Agenda generada: {len(self.pacientes_programados)} pacientes")
        print(f"Primer turno: {self.pacientes_programados[0].turno_asignado:.1f} min")
        print(f"Último turno: {self.pacientes_programados[-1].turno_asignado:.1f} min")
        
    def actualizar(self, delta_sim, delta_real, multiplicador_velocidad=1.0):
        """Actualiza la simulación automáticamente"""
        if self.pausada or self.finalizada:
            return
        
        self.tiempo_actual += delta_sim
        self.datetime_actual = self.fecha_inicio + timedelta(minutes=self.tiempo_actual)
        
        # 1. Procesar llegadas (pacientes que llegan según su hora)
        self._procesar_llegadas()
        
        # 2. Actualizar movimientos de todos los pacientes activos
        self._actualizar_movimientos(delta_real, multiplicador_velocidad)
        
        # 3. Actualizar tiempos en etapa
        self._actualizar_tiempos_en_etapa(delta_sim)
        
        # 4. Gestionar flujo de pacientes
        self._gestionar_flujo()
        
        # 5. Verificar si terminó el día
        if (not self.pacientes_programados and 
            not self.pacientes_en_espera and
            self.paciente_en_validacion is None and
            self.paciente_en_vestuario is None and
            self.paciente_en_box is None and
            self.paciente_en_resonador is None):
            self.finalizada = True
    
    def _procesar_llegadas(self):
        """Procesar pacientes que llegan según su hora REAL (turno + desvío)"""
        pacientes_a_llegar = []
        
        for p in self.pacientes_programados:
            # Llega cuando el tiempo actual >= hora_llegada_real
            if self.tiempo_actual >= p.hora_llegada_real:
                pacientes_a_llegar.append(p)
        
        # Procesar llegadas
        for p in pacientes_a_llegar:
            self.pacientes_programados.remove(p)
            p.estado = 'LLEGADA'
            p.ts_inicio = self.datetime_actual
            # Ruta: entrada → sala de espera
            p.definir_ruta(['esperando', 'entrada', 'sala_espera'])
            self.pacientes_en_espera.append(p)
    
    def _actualizar_movimientos(self, delta_real, mult_vel):
        """Actualiza movimientos de todos los pacientes visibles"""
        todos = (self.pacientes_en_espera + 
                [p for p in [self.paciente_en_validacion, self.paciente_en_vestuario,
                            self.paciente_en_box, self.paciente_en_resonador] if p])
        
        for p in todos:
            if p.moviendo:
                p.actualizar_movimiento(delta_real, mult_vel)
    
    def _actualizar_tiempos_en_etapa(self, delta_sim):
        """Actualiza tiempo en etapa de pacientes en proceso"""
        if self.paciente_en_validacion:
            self.paciente_en_validacion.tiempo_en_etapa += delta_sim
        if self.paciente_en_box:
            self.paciente_en_box.tiempo_en_etapa += delta_sim
        if self.paciente_en_resonador:
            self.paciente_en_resonador.tiempo_en_etapa += delta_sim
    
    def _gestionar_flujo(self):
        """Gestiona el flujo de pacientes por las diferentes estaciones"""
        
        # Sala de espera → Mesa de validación
        if self.paciente_en_validacion is None and self.pacientes_en_espera:
            # Tomar el primer paciente que terminó de moverse
            for p in self.pacientes_en_espera:
                if not p.moviendo and p.estado == 'LLEGADA':
                    self.pacientes_en_espera.remove(p)
                    self.paciente_en_validacion = p
                    p.estado = 'VALIDACION'
                    p.tiempo_en_etapa = 0
                    p.definir_ruta(['sala_espera', 'mesa'])
                    break
        
        # Mesa → Camino al vestuario
        if self.paciente_en_validacion and not self.paciente_en_validacion.moviendo:
            if self.paciente_en_validacion.estado == 'VALIDACION':
                if self.paciente_en_validacion.tiempo_en_etapa >= self.paciente_en_validacion.tiempo_validacion:
                    p = self.paciente_en_validacion
                    self.paciente_en_validacion = None
                    p.estado = 'CAMINANDO_VESTUARIO'
                    p.definir_ruta(['salida_sala', 'pasillo_v', 'pasillo_v_arriba', 
                                   'pasillo_h', 'pasillo_h_derecha', 'entrada_vestuario', 'vestuario'])
                    self.paciente_en_vestuario = p
        
        # Vestuario → Box
        if self.paciente_en_vestuario and not self.paciente_en_vestuario.moviendo:
            if self.paciente_en_box is None:
                p = self.paciente_en_vestuario
                self.paciente_en_vestuario = None
                p.estado = 'BOX'
                p.tiempo_en_etapa = 0
                p.definir_ruta(['vestuario', 'box'])
                self.paciente_en_box = p
        
        # Box → Resonador (espera si está ocupado)
        if self.paciente_en_box and not self.paciente_en_box.moviendo:
            if self.paciente_en_box.tiempo_en_etapa >= self.paciente_en_box.tiempo_box:
                if self.paciente_en_resonador is None:
                    p = self.paciente_en_box
                    self.paciente_en_box = None
                    p.estado = 'RESONADOR'
                    p.tiempo_en_etapa = 0
                    p.definir_ruta(['vuelta_vestuario', 'entrada_resonancia', 
                                   'resonancia', 'resonador'])
                    self.paciente_en_resonador = p
        
        # Resonador → Completado
        if self.paciente_en_resonador and not self.paciente_en_resonador.moviendo:
            if self.paciente_en_resonador.tiempo_en_etapa >= self.paciente_en_resonador.tiempo_total_resonador:
                p = self.paciente_en_resonador
                self.paciente_en_resonador = None
                p.estado = 'COMPLETADO'
                p.ts_fin = self.datetime_actual
                if p.ts_inicio:
                    p.tiempo_total = (p.ts_fin - p.ts_inicio).total_seconds() / 60
                p.definir_ruta(['salida'])
                self.pacientes_completados.append(p)
    
    def obtener_paciente_activo(self):
        """Retorna el paciente más relevante para mostrar en pantalla"""
        if self.paciente_en_resonador:
            return self.paciente_en_resonador
        if self.paciente_en_box:
            return self.paciente_en_box
        if self.paciente_en_vestuario:
            return self.paciente_en_vestuario
        if self.paciente_en_validacion:
            return self.paciente_en_validacion
        if self.pacientes_en_espera:
            return self.pacientes_en_espera[0]
        return None
    
    def todos_los_pacientes(self):
        """Retorna todos los pacientes visibles en la clínica"""
        pacientes = self.pacientes_en_espera.copy()
        if self.paciente_en_validacion:
            pacientes.append(self.paciente_en_validacion)
        if self.paciente_en_vestuario:
            pacientes.append(self.paciente_en_vestuario)
        if self.paciente_en_box:
            pacientes.append(self.paciente_en_box)
        if self.paciente_en_resonador:
            pacientes.append(self.paciente_en_resonador)
        return pacientes
    
    def obtener_estadisticas_dia(self):
        """Obtiene estadísticas del día con último turno y hora fin"""
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
        
        # Último paciente completado
        ultimo = self.pacientes_completados[-1]
        ultimo_turno_min = ultimo.turno_asignado
        
        # Calcular hora de finalización (llegada + tiempo de servicio)
        hora_fin_min = ultimo.hora_llegada_real + ultimo.calcular_tiempo_circuito()
        
        # Convertir minutos a formato HH:MM
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
