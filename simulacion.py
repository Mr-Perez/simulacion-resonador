"""Motor de Simulación V3.1 - Llegadas espaciadas y salida completa"""
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
        self.pacientes_saliendo = []  # NUEVO: pacientes en ruta de salida
        self.pacientes_completados = []
        
        self.pausada = False
        self.finalizada = False
        
        # Control de llegadas espaciadas
        self.ultimo_tiempo_llegada = -999  # Tiempo de última llegada
        
        self._generar_agenda_flexible()
        
    def _generar_agenda_flexible(self):
        """Genera turnos con grilla flexible"""
        turno_actual = 0.0
        numero_paciente = 1
        
        while turno_actual < 690:
            p = Paciente(turno_actual, self.fecha_inicio)
            p.id = numero_paciente
            p.turno_asignado = turno_actual
            
            tiempo_estimado = (
                p.tiempo_validacion +
                2.0 +
                p.tiempo_box +
                p.tiempo_total_resonador +
                2.0 +
                p.tiempo_salida
            )
            
            p.hora_llegada_real = turno_actual + p.desvio_llegada
            p.estado = 'PROGRAMADO'
            
            self.pacientes_programados.append(p)
            
            turno_actual += tiempo_estimado
            numero_paciente += 1
        
        print(f"✓ Agenda: {len(self.pacientes_programados)} pacientes")
        print(f"  Turnos: 0 - {self.pacientes_programados[-1].turno_asignado:.0f} min")
        print(f"\n📊 Ejemplos de llegadas (turno + desvío):")
        for i in range(min(5, len(self.pacientes_programados))):
            p = self.pacientes_programados[i]
            desvio_texto = "temprano" if p.desvio_llegada < 0 else ("puntual" if p.desvio_llegada == 0 else "tarde")
            print(f"  P#{p.id}: Turno {p.turno_asignado:.0f}min + {p.desvio_llegada:+.0f}min = Llega {p.hora_llegada_real:.0f}min ({desvio_texto})")
        
    def actualizar(self, delta_sim, delta_real, multiplicador_velocidad=1.0):
        if self.pausada or self.finalizada:
            return
        
        self.tiempo_actual += delta_sim
        self.datetime_actual = self.fecha_inicio + timedelta(minutes=self.tiempo_actual)
        
        # 1. Procesar llegadas (con espaciado)
        self._procesar_llegadas()
        
        # 2. Actualizar movimientos
        todos = self.pacientes_en_espera.copy()
        if self.paciente_en_validacion:
            todos.append(self.paciente_en_validacion)
        if self.paciente_en_box:
            todos.append(self.paciente_en_box)
        if self.paciente_en_resonador:
            todos.append(self.paciente_en_resonador)
        todos.extend(self.pacientes_saliendo)
        
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
            not self.paciente_en_resonador and
            not self.pacientes_saliendo):
            self.finalizada = True
    
    def _procesar_llegadas(self):
        """Procesar llegadas - Solo cuando hay alguien SALIENDO (verde)"""
        if not self.pacientes_programados:
            return
        
        # RESTRICCIÓN 1: Máximo 1 en espera
        if len(self.pacientes_en_espera) >= 1:
            return
        
        # RESTRICCIÓN 2: Solo permitir llegada cuando hay alguien SALIENDO (VERDE)
        # O cuando el sistema está vacío (primer paciente)
        sistema_vacio = (not self.paciente_en_validacion and 
                        not self.paciente_en_box and 
                        not self.paciente_en_resonador and
                        len(self.pacientes_saliendo) == 0 and
                        len(self.pacientes_completados) == 0)
        
        tiene_alguien_saliendo = len(self.pacientes_saliendo) > 0
        
        if not sistema_vacio and not tiene_alguien_saliendo:
            return  # Nadie está saliendo (verde), esperar
        
        # Ordenar por hora de llegada real (turno + desvío)
        self.pacientes_programados.sort(key=lambda p: p.hora_llegada_real)
        
        if not self.pacientes_programados:
            return
        
        proximo = self.pacientes_programados[0]
        
        # El siguiente paciente llega en su hora_llegada_real (turno + desvío)
        # SI el tiempo actual ya pasó esa hora
        if self.tiempo_actual >= proximo.hora_llegada_real:
            p = self.pacientes_programados.pop(0)
            p.estado = 'LLEGADA'
            p.ts_inicio = self.datetime_actual
            p.definir_ruta(['esperando', 'entrada', 'sala_espera'])
            self.pacientes_en_espera.append(p)
            self.ultimo_tiempo_llegada = self.tiempo_actual
    
    def _gestionar_flujo(self):
        """Gestiona el flujo incluyendo SALIDA completa"""
        
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
        
        # Mesa → Box
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
        
        # Resonador → SALIDA (NUEVO)
        if self.paciente_en_resonador and not self.paciente_en_resonador.moviendo:
            p = self.paciente_en_resonador
            if p.tiempo_en_etapa >= p.tiempo_total_resonador:
                self.paciente_en_resonador = None
                p.estado = 'SALIENDO'
                p.ts_fin = self.datetime_actual
                if p.ts_inicio:
                    p.tiempo_total = (p.ts_fin - p.ts_inicio).total_seconds() / 60
                # Ruta de salida completa
                p.definir_ruta(['salida_resonancia', 'salida_vestuario', 
                               'salida_pasillo_h', 'salida_pasillo_v', 
                               'retorno_sala', 'salida_final'])
                self.pacientes_saliendo.append(p)
        
        # Saliendo → Completado (NUEVO)
        for p in self.pacientes_saliendo[:]:
            if not p.moviendo:
                self.pacientes_saliendo.remove(p)
                p.estado = 'COMPLETADO'
                self.pacientes_completados.append(p)
    
    def simular_dia_completo_rapido(self):
        """Simula el resto del día rápidamente (para tecla S)"""
        pacientes_simulados = []
        turno_actual = 0.0
        numero = 1
        
        while turno_actual < 690:
            p = Paciente(turno_actual, self.fecha_inicio)
            p.id = numero
            p.turno_asignado = turno_actual
            
            tiempo_servicio = (
                p.tiempo_validacion +
                2.0 +
                p.tiempo_box +
                p.tiempo_total_resonador +
                2.0 +
                p.tiempo_salida
            )
            
            p.hora_llegada_real = turno_actual + p.desvio_llegada
            p.estado = 'COMPLETADO'
            pacientes_simulados.append(p)
            
            turno_actual += tiempo_servicio
            numero += 1
        
        return pacientes_simulados
    
    def obtener_paciente_activo(self):
        if self.paciente_en_resonador:
            return self.paciente_en_resonador
        if self.paciente_en_box:
            return self.paciente_en_box
        if self.paciente_en_validacion:
            return self.paciente_en_validacion
        if self.pacientes_en_espera:
            return self.pacientes_en_espera[0]
        if self.pacientes_saliendo:
            return self.pacientes_saliendo[0]
        return None
    
    def todos_los_pacientes(self):
        pacientes = self.pacientes_en_espera.copy()
        if self.paciente_en_validacion:
            pacientes.append(self.paciente_en_validacion)
        if self.paciente_en_box:
            pacientes.append(self.paciente_en_box)
        if self.paciente_en_resonador:
            pacientes.append(self.paciente_en_resonador)
        pacientes.extend(self.pacientes_saliendo)
        return pacientes
    
    def obtener_estadisticas_dia(self, pacientes=None):
        if pacientes is None:
            pacientes = self.pacientes_completados
        
        if not pacientes:
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
        for p in pacientes:
            estudios[p.tipo_estudio] = estudios.get(p.tipo_estudio, 0) + 1
            tiempo = p.calcular_tiempo_circuito()
            tiempos.append(tiempo)
        
        ultimo = pacientes[-1]
        ultimo_turno_min = ultimo.turno_asignado
        hora_fin_min = ultimo.hora_llegada_real + ultimo.calcular_tiempo_circuito()
        
        def min_a_hora(minutos):
            horas = 8 + int(minutos // 60)
            mins = int(minutos % 60)
            return f"{horas:02d}:{mins:02d}"
        
        return {
            'estudios_por_tipo': estudios,
            'tiempo_promedio_total': sum(tiempos) / len(tiempos) if tiempos else 0,
            'total_pacientes': len(pacientes),
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
