"""
MOTOR DE SIMULACIÓN
===================
Sistema de eventos discretos para simular el flujo de pacientes
"""

from datetime import datetime, timedelta
from collections import deque
import config
from paciente import Paciente

class SimuladorResonador:
    """
    Motor de simulación de eventos discretos para el sistema de resonador.
    Maneja el flujo de pacientes a través de las diferentes etapas.
    """
    
    def __init__(self, fecha_inicio=None):
        """
        Inicializa el simulador
        
        Args:
            fecha_inicio: Fecha y hora de inicio de la simulación
        """
        # Tiempo de simulación
        if fecha_inicio is None:
            fecha_inicio = datetime.now().replace(
                hour=config.HORA_INICIO,
                minute=0,
                second=0,
                microsecond=0
            )
        
        self.fecha_inicio = fecha_inicio
        self.tiempo_actual = 0  # minutos desde el inicio
        self.datetime_actual = fecha_inicio
        
        # Recursos del sistema
        self.mesa_ocupada = False
        self.cambiador_ocupado = False
        self.resonador_ocupado = False
        
        # Pacientes en diferentes etapas
        self.pacientes_programados = []  # Lista de todos los pacientes
        self.cola_espera = deque()       # Pacientes en sala de espera
        self.cola_validacion = deque()   # Cola para mesa de atención
        self.cola_cambiador_in = deque() # Cola para cambiador (entrada)
        self.cola_resonador = deque()    # Cola para el resonador
        self.cola_cambiador_out = deque()# Cola para cambiador (salida)
        
        # Pacientes actualmente siendo atendidos
        self.paciente_en_mesa = None
        self.paciente_en_cambiador = None
        self.paciente_en_resonador = None
        
        # Pacientes completados
        self.pacientes_completados = []
        
        # Métricas globales
        self.total_pacientes = 0
        self.pacientes_atendidos = 0
        self.tiempo_ocupacion_resonador = 0
        self.tiempo_ocioso_resonador = 0
        
        # Estado de la simulación
        self.pausada = False
        self.finalizada = False
        
    def generar_turnos(self, cantidad_turnos=None):
        """
        Genera los turnos del día para los pacientes
        
        Args:
            cantidad_turnos: Cantidad de turnos a generar (None = día completo)
        """
        minutos_dia = (config.HORA_FIN - config.HORA_INICIO) * 60
        
        if cantidad_turnos is None:
            # Generar turnos cada INTERVALO_TURNOS minutos
            cantidad_turnos = minutos_dia // config.INTERVALO_TURNOS
        
        for i in range(cantidad_turnos):
            turno_minutos = i * config.INTERVALO_TURNOS
            paciente = Paciente(turno_minutos, self.fecha_inicio)
            self.pacientes_programados.append(paciente)
        
        self.total_pacientes = len(self.pacientes_programados)
        print(f"✅ Generados {self.total_pacientes} turnos para el día")
    
    def actualizar(self, delta_tiempo, delta_real=None):
        """
        Actualiza la simulación
        
        Args:
            delta_tiempo: Tiempo transcurrido en minutos simulados
            delta_real: Tiempo transcurrido en segundos reales (para animaciones)
        """
        if self.pausada or self.finalizada:
            return
        
        self.tiempo_actual += delta_tiempo
        self.datetime_actual = self.fecha_inicio + timedelta(minutes=self.tiempo_actual)
        
        # 1. Procesar llegadas de pacientes
        self._procesar_llegadas()
        
        # 2. Actualizar pacientes en proceso
        self._actualizar_pacientes_en_proceso(delta_tiempo)
        
        # 3. Actualizar movimientos de pacientes (si hay delta_real)
        if delta_real is not None:
            self._actualizar_movimientos(delta_real)
        
        # 4. Asignar recursos disponibles
        self._asignar_recursos()
        
        # 5. Actualizar métricas
        self._actualizar_metricas(delta_tiempo)
        
        # 6. Verificar si terminó la simulación
        self._verificar_finalizacion()
    
    def _actualizar_movimientos(self, delta_real):
        """Actualiza el movimiento suave de todos los pacientes"""
        for paciente in self.todos_los_pacientes():
            if paciente.esta_moviendo:
                paciente.actualizar_movimiento(delta_real)
    
    def _procesar_llegadas(self):
        """Procesa la llegada de pacientes según su hora de turno"""
        for paciente in self.pacientes_programados[:]:
            if paciente.tiempo_llegada_real <= self.tiempo_actual and paciente.estado == 'LLEGADA':
                # El paciente llega y se mueve a sala de espera
                paciente.timestamp_llegada = self.datetime_actual
                paciente.estado = 'ESPERA'
                
                # Definir ruta: entrada → sala de espera
                paciente.definir_ruta(['entrada', 'sala_espera_centro'])
                
                self.cola_espera.append(paciente)
                self.pacientes_programados.remove(paciente)
    
    def _actualizar_pacientes_en_proceso(self, delta_tiempo):
        """Actualiza el estado de los pacientes que están siendo atendidos"""
        
        # Mesa de atención
        if self.paciente_en_mesa:
            self.paciente_en_mesa.tiempo_actual_en_etapa += delta_tiempo
            
            if self.paciente_en_mesa.tiempo_actual_en_etapa >= self.paciente_en_mesa.tiempo_validacion:
                # Terminó la validación
                self.paciente_en_mesa.timestamp_fin_validacion = self.datetime_actual
                self.paciente_en_mesa.estado = 'CAMBIADOR_IN'
                self.paciente_en_mesa.tiempo_actual_en_etapa = 0
                self.cola_cambiador_in.append(self.paciente_en_mesa)
                self.paciente_en_mesa = None
                self.mesa_ocupada = False
        
        # Cambiador (entrada)
        if self.paciente_en_cambiador and self.paciente_en_cambiador.estado == 'CAMBIADOR_IN':
            self.paciente_en_cambiador.tiempo_actual_en_etapa += delta_tiempo
            
            if self.paciente_en_cambiador.tiempo_actual_en_etapa >= self.paciente_en_cambiador.tiempo_cambiador_entrada:
                # Terminó de cambiarse
                self.paciente_en_cambiador.timestamp_fin_cambiador_in = self.datetime_actual
                self.paciente_en_cambiador.estado = 'ESPERANDO_RESONADOR'
                self.paciente_en_cambiador.tiempo_actual_en_etapa = 0
                self.cola_resonador.append(self.paciente_en_cambiador)
                self.paciente_en_cambiador = None
                self.cambiador_ocupado = False
        
        # Resonador
        if self.paciente_en_resonador:
            self.paciente_en_resonador.tiempo_actual_en_etapa += delta_tiempo
            
            if self.paciente_en_resonador.tiempo_actual_en_etapa >= self.paciente_en_resonador.tiempo_total_resonador:
                # Terminó el estudio
                self.paciente_en_resonador.timestamp_fin_resonador = self.datetime_actual
                self.paciente_en_resonador.estado = 'CAMBIADOR_OUT'
                self.paciente_en_resonador.tiempo_actual_en_etapa = 0
                self.cola_cambiador_out.append(self.paciente_en_resonador)
                self.paciente_en_resonador = None
                self.resonador_ocupado = False
        
        # Cambiador (salida)
        if self.paciente_en_cambiador and self.paciente_en_cambiador.estado == 'CAMBIADOR_OUT':
            self.paciente_en_cambiador.tiempo_actual_en_etapa += delta_tiempo
            
            if self.paciente_en_cambiador.tiempo_actual_en_etapa >= self.paciente_en_cambiador.tiempo_cambiador_salida:
                # Terminó de vestirse
                self.paciente_en_cambiador.timestamp_fin_cambiador_out = self.datetime_actual
                self.paciente_en_cambiador.estado = 'SALIDA'
                self.paciente_en_cambiador.timestamp_salida = self.datetime_actual
                self.paciente_en_cambiador.tiempo_actual_en_etapa = 0
                
                # Calcular tiempo total de servicio
                self.paciente_en_cambiador.calcular_tiempo_total_servicio()
                self.paciente_en_cambiador.completado = True
                self.paciente_en_cambiador.estado = 'COMPLETADO'
                
                self.pacientes_completados.append(self.paciente_en_cambiador)
                self.pacientes_atendidos += 1
                self.paciente_en_cambiador = None
                self.cambiador_ocupado = False
    
    def _asignar_recursos(self):
        """Asigna pacientes a recursos disponibles"""
        
        # Mesa de atención
        if not self.mesa_ocupada and self.cola_espera:
            paciente = self.cola_espera.popleft()
            paciente.estado = 'VALIDACION'
            paciente.timestamp_inicio_validacion = self.datetime_actual
            paciente.tiempo_actual_en_etapa = 0
            
            # Ruta: sala espera → mesa
            paciente.definir_ruta(['sala_espera_centro', 'mesa'])
            
            self.paciente_en_mesa = paciente
            self.mesa_ocupada = True
        
        # Cambiador (entrada)
        if not self.cambiador_ocupado and self.cola_cambiador_in:
            paciente = self.cola_cambiador_in.popleft()
            paciente.timestamp_inicio_cambiador_in = self.datetime_actual
            paciente.tiempo_actual_en_etapa = 0
            
            # Ruta: mesa → pasillo → vestuario
            paciente.definir_ruta(['salida_sala_espera', 'pasillo_bajo', 'pasillo_medio', 
                                  'pasillo_alto', 'bajada_vestuario', 'vestuario_entrada', 'vestuario'])
            
            self.paciente_en_cambiador = paciente
            self.cambiador_ocupado = True
        
        # Resonador
        if not self.resonador_ocupado and self.cola_resonador:
            paciente = self.cola_resonador.popleft()
            paciente.estado = 'RESONADOR'
            paciente.timestamp_inicio_resonador = self.datetime_actual
            paciente.tiempo_actual_en_etapa = 0
            
            # Ruta: vestuario → sala resonancia → resonador
            paciente.definir_ruta(['bajada_resonancia', 'sala_resonancia_entrada', 'resonador'])
            
            self.paciente_en_resonador = paciente
            self.resonador_ocupado = True
        
        # Cambiador (salida)
        if not self.cambiador_ocupado and self.cola_cambiador_out:
            paciente = self.cola_cambiador_out.popleft()
            paciente.timestamp_inicio_cambiador_out = self.datetime_actual
            paciente.tiempo_actual_en_etapa = 0
            
            # Ruta: resonador → vestuario
            paciente.definir_ruta(['sala_resonancia_entrada', 'bajada_resonancia', 'vestuario'])
            
            self.paciente_en_cambiador = paciente
            self.cambiador_ocupado = True
    
    def _actualizar_metricas(self, delta_tiempo):
        """Actualiza las métricas globales de la simulación"""
        if self.resonador_ocupado:
            self.tiempo_ocupacion_resonador += delta_tiempo
        else:
            self.tiempo_ocioso_resonador += delta_tiempo
    
    def _verificar_finalizacion(self):
        """Verifica si la simulación ha terminado"""
        if (len(self.pacientes_programados) == 0 and
            len(self.cola_espera) == 0 and
            len(self.cola_validacion) == 0 and
            len(self.cola_cambiador_in) == 0 and
            len(self.cola_resonador) == 0 and
            len(self.cola_cambiador_out) == 0 and
            self.paciente_en_mesa is None and
            self.paciente_en_cambiador is None and
            self.paciente_en_resonador is None):
            self.finalizada = True
            print(f"🎉 Simulación finalizada - {self.pacientes_atendidos} pacientes atendidos")
    
    def obtener_metricas_globales(self):
        """Retorna métricas globales de la simulación"""
        tiempo_total = max(self.tiempo_actual, 1)  # Evitar división por cero
        
        utilizacion_resonador = 0
        if tiempo_total > 0:
            utilizacion_resonador = (self.tiempo_ocupacion_resonador / tiempo_total) * 100
        
        return {
            'tiempo_simulacion': round(self.tiempo_actual, 2),
            'total_pacientes': self.total_pacientes,
            'pacientes_atendidos': self.pacientes_atendidos,
            'pacientes_en_espera': len(self.cola_espera),
            'utilizacion_resonador': round(utilizacion_resonador, 2),
            'tiempo_ocupacion_resonador': round(self.tiempo_ocupacion_resonador, 2),
            'tiempo_ocioso_resonador': round(self.tiempo_ocioso_resonador, 2),
            'paciente_en_mesa': self.paciente_en_mesa,
            'paciente_en_cambiador': self.paciente_en_cambiador,
            'paciente_en_resonador': self.paciente_en_resonador
        }
    
    def obtener_paciente_activo(self):
        """Retorna el paciente que está actualmente en el resonador"""
        return self.paciente_en_resonador
    
    def todos_los_pacientes(self):
        """Retorna todos los pacientes en cualquier estado"""
        pacientes = list(self.pacientes_programados)
        pacientes.extend(self.cola_espera)
        pacientes.extend(self.cola_validacion)
        pacientes.extend(self.cola_cambiador_in)
        pacientes.extend(self.cola_resonador)
        pacientes.extend(self.cola_cambiador_out)
        
        if self.paciente_en_mesa:
            pacientes.append(self.paciente_en_mesa)
        if self.paciente_en_cambiador:
            pacientes.append(self.paciente_en_cambiador)
        if self.paciente_en_resonador:
            pacientes.append(self.paciente_en_resonador)
        
        pacientes.extend(self.pacientes_completados)
        
        return pacientes
    
    def obtener_estadisticas_dia(self):
        """Retorna estadísticas completas del día"""
        if not self.pacientes_completados:
            return {
                'estudios_por_tipo': {},
                'tiempo_promedio_total': 0,
                'tiempo_promedio_espera': 0,
                'tiempo_promedio_resonador': 0
            }
        
        # Contar estudios por tipo
        estudios_por_tipo = {}
        tiempos_totales = []
        tiempos_espera = []
        tiempos_resonador = []
        
        for paciente in self.pacientes_completados:
            # Conteo por tipo
            tipo = paciente.tipo_estudio
            estudios_por_tipo[tipo] = estudios_por_tipo.get(tipo, 0) + 1
            
            # Tiempos
            tiempos_totales.append(paciente.tiempo_total_servicio)
            tiempos_espera.append(paciente.tiempo_espera_acumulado)
            tiempos_resonador.append(paciente.tiempo_total_resonador)
        
        # Promedios
        tiempo_promedio_total = sum(tiempos_totales) / len(tiempos_totales) if tiempos_totales else 0
        tiempo_promedio_espera = sum(tiempos_espera) / len(tiempos_espera) if tiempos_espera else 0
        tiempo_promedio_resonador = sum(tiempos_resonador) / len(tiempos_resonador) if tiempos_resonador else 0
        
        return {
            'estudios_por_tipo': estudios_por_tipo,
            'tiempo_promedio_total': tiempo_promedio_total,
            'tiempo_promedio_espera': tiempo_promedio_espera,
            'tiempo_promedio_resonador': tiempo_promedio_resonador
        }
    
    def pausar(self):
        """Pausa la simulación"""
        self.pausada = True
    
    def reanudar(self):
        """Reanuda la simulación"""
        self.pausada = False
    
    def reiniciar(self):
        """Reinicia la simulación"""
        self.__init__(self.fecha_inicio)
