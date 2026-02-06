"""
VISUALIZACIÓN PROFESIONAL CON PYGAME
=====================================
Interfaz gráfica 2D mejorada de la simulación del resonador
"""

import pygame
import sys
import config
import math
from datetime import timedelta

class Visualizador:
    """
    Maneja la visualización gráfica profesional de la simulación usando Pygame
    """
    
    def __init__(self, simulador):
        """
        Inicializa el visualizador
        
        Args:
            simulador: Instancia de SimuladorResonador
        """
        pygame.init()
        
        self.simulador = simulador
        self.pantalla = pygame.display.set_mode((config.VENTANA_ANCHO, config.VENTANA_ALTO))
        pygame.display.set_caption("Simulación Resonador - Clínica [VERSIÓN PROFESIONAL]")
        
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_pequena = pygame.font.Font(None, 18)
        self.fuente_titulo = pygame.font.Font(None, 36)
        self.fuente_grande = pygame.font.Font(None, 48)
        
        self.ejecutando = True
        self.velocidad = config.VELOCIDAD_SIMULACION_DEFAULT
        
        # Estado de resumen final
        self.mostrar_resumen = False
        
    def ejecutar(self):
        """Bucle principal de la visualización"""
        while self.ejecutando:
            delta_real = self.reloj.tick(config.FPS) / 1000.0  # Delta en segundos reales
            
            # Procesar eventos
            self._procesar_eventos()
            
            # Actualizar simulación
            if not self.simulador.pausada and not self.simulador.finalizada:
                delta_sim = self.velocidad / config.FPS  # Minutos simulados
                self.simulador.actualizar(delta_sim, delta_real)
            
            # Si terminó la simulación, mostrar resumen
            if self.simulador.finalizada and config.MOSTRAR_RESUMEN_FINAL:
                self.mostrar_resumen = True
            
            # Dibujar
            if self.mostrar_resumen:
                self._dibujar_resumen_final()
            else:
                self._dibujar()
            
        pygame.quit()
        sys.exit()
    
    def _procesar_eventos(self):
        """Procesa los eventos de Pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ejecutando = False
            
            elif evento.type == pygame.KEYDOWN:
                # Espacio: pausar/reanudar
                if evento.key == pygame.K_SPACE:
                    if self.simulador.pausada:
                        self.simulador.reanudar()
                    else:
                        self.simulador.pausar()
                
                # Flechas: ajustar velocidad
                elif evento.key == pygame.K_UP:
                    self.velocidad = min(self.velocidad * 1.5, config.VELOCIDAD_SIMULACION_MAX)
                elif evento.key == pygame.K_DOWN:
                    self.velocidad = max(self.velocidad / 1.5, config.VELOCIDAD_SIMULACION_MIN)
                
                # R: reiniciar
                elif evento.key == pygame.K_r:
                    self.simulador.reiniciar()
                    self.simulador.generar_turnos()
                    self.mostrar_resumen = False
                
                # ESC: salir
                elif evento.key == pygame.K_ESCAPE:
                    self.ejecutando = False
                
                # Enter: cerrar resumen
                elif evento.key == pygame.K_RETURN and self.mostrar_resumen:
                    self.mostrar_resumen = False
                    self.simulador.pausar()
    
    def _dibujar(self):
        """Dibuja toda la interfaz"""
        # Fondo con gradiente sutil
        self.pantalla.fill(config.COLOR_FONDO)
        
        # Título superior
        self._dibujar_header()
        
        # Dibujar layout de la clínica
        self._dibujar_clinica_profesional()
        
        # Dibujar pacientes con animación
        self._dibujar_pacientes_animados()
        
        # Dibujar panel de métricas
        self._dibujar_panel_metricas_mejorado()
        
        # Dibujar panel de paciente activo
        self._dibujar_panel_paciente_activo_mejorado()
        
        # Dibujar controles
        self._dibujar_controles_mejorados()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def _dibujar_header(self):
        """Dibuja el header superior con título"""
        # Barra superior
        pygame.draw.rect(self.pantalla, (60, 90, 140), (0, 0, config.VENTANA_ANCHO, 60))
        
        # Título
        texto = self.fuente_titulo.render("SIMULACIÓN DE RESONADOR - CLÍNICA", True, (255, 255, 255))
        self.pantalla.blit(texto, (20, 15))
        
        # Hora de simulación
        metricas = self.simulador.obtener_metricas_globales()
        hora_sim = self.simulador.datetime_actual.strftime('%H:%M')
        texto_hora = self.fuente.render(f"Hora: {hora_sim}", True, (200, 220, 255))
        self.pantalla.blit(texto_hora, (config.VENTANA_ANCHO - 150, 18))
    
    def _dibujar_clinica_profesional(self):
        """Dibuja el layout de la clínica con estilo profesional"""
        layout = config.LAYOUT
        
        # Función auxiliar para dibujar rectángulos con sombra
        def dibujar_area_con_sombra(x, y, ancho, alto, color, nombre, color_texto=config.COLOR_TEXTO):
            # Sombra
            pygame.draw.rect(self.pantalla, config.COLOR_SOMBRA, 
                           (x + 5, y + 5, ancho, alto), 0, border_radius=8)
            # Área principal
            pygame.draw.rect(self.pantalla, color, 
                           (x, y, ancho, alto), 0, border_radius=8)
            # Borde
            pygame.draw.rect(self.pantalla, config.COLOR_BORDE, 
                           (x, y, ancho, alto), 2, border_radius=8)
            # Texto
            texto = self.fuente.render(nombre, True, color_texto)
            rect_texto = texto.get_rect()
            rect_texto.center = (x + ancho // 2, y + 25)
            self.pantalla.blit(texto, rect_texto)
        
        # Sala de espera
        dibujar_area_con_sombra(
            layout['sala_espera']['x'], layout['sala_espera']['y'],
            layout['sala_espera']['ancho'], layout['sala_espera']['alto'],
            config.COLOR_SALA_ESPERA, "SALA DE ESPERA"
        )
        
        # Mesa de atención
        dibujar_area_con_sombra(
            layout['mesa_atencion']['x'], layout['mesa_atencion']['y'],
            layout['mesa_atencion']['ancho'], layout['mesa_atencion']['alto'],
            config.COLOR_MESA, "Mesa de Atención"
        )
        
        # Pasillos (sin sombra, más sutiles)
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO,
                        (layout['pasillo_vertical']['x'], layout['pasillo_vertical']['y'],
                         layout['pasillo_vertical']['ancho'], layout['pasillo_vertical']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO,
                        (layout['pasillo_horizontal']['x'], layout['pasillo_horizontal']['y'],
                         layout['pasillo_horizontal']['ancho'], layout['pasillo_horizontal']['alto']), 0)
        
        # Box
        dibujar_area_con_sombra(
            layout['box']['x'], layout['box']['y'],
            layout['box']['ancho'], layout['box']['alto'],
            config.COLOR_BOX, "Box"
        )
        
        # Vestuario
        dibujar_area_con_sombra(
            layout['vestuario']['x'], layout['vestuario']['y'],
            layout['vestuario']['ancho'], layout['vestuario']['alto'],
            config.COLOR_VESTUARIO, "VESTUARIO"
        )
        
        # Sala de resonancia
        dibujar_area_con_sombra(
            layout['sala_resonancia']['x'], layout['sala_resonancia']['y'],
            layout['sala_resonancia']['ancho'], layout['sala_resonancia']['alto'],
            config.COLOR_SALA_RESONANCIA, "SALA DE RESONANCIA"
        )
        
        # Resonador (destacado)
        # Sombra
        pygame.draw.rect(self.pantalla, (80, 80, 80),
                        (layout['resonador']['x'] + 6, layout['resonador']['y'] + 6,
                         layout['resonador']['ancho'], layout['resonador']['alto']), 0, border_radius=12)
        # Resonador
        pygame.draw.rect(self.pantalla, config.COLOR_RESONADOR,
                        (layout['resonador']['x'], layout['resonador']['y'],
                         layout['resonador']['ancho'], layout['resonador']['alto']), 0, border_radius=12)
        # Borde brillante
        pygame.draw.rect(self.pantalla, (70, 120, 200),
                        (layout['resonador']['x'], layout['resonador']['y'],
                         layout['resonador']['ancho'], layout['resonador']['alto']), 4, border_radius=12)
        # Texto
        texto = self.fuente_titulo.render("RESONADOR", True, (255, 255, 255))
        rect_texto = texto.get_rect()
        rect_texto.center = (layout['resonador']['x'] + layout['resonador']['ancho'] // 2,
                            layout['resonador']['y'] + layout['resonador']['alto'] // 2)
        self.pantalla.blit(texto, rect_texto)
    
    def _dibujar_pacientes_animados(self):
        """Dibuja los pacientes con animación suave"""
        # Pacientes en sala de espera (en grid)
        for i, paciente in enumerate(self.simulador.cola_espera):
            x = config.LAYOUT['sala_espera']['x'] + 60 + (i % 3) * 120
            y = config.LAYOUT['sala_espera']['y'] + 120 + (i // 3) * 100
            self._dibujar_paciente_mejorado(x, y, paciente, config.COLOR_PACIENTE)
        
        # Pacientes en movimiento o en proceso
        for paciente in self.simulador.todos_los_pacientes():
            if paciente.esta_moviendo or paciente.estado in ['VALIDACION', 'CAMBIADOR_IN', 'RESONADOR', 'CAMBIADOR_OUT']:
                color = config.COLOR_PACIENTE_ACTIVO if paciente.estado == 'RESONADOR' else config.COLOR_PACIENTE
                self._dibujar_paciente_mejorado(
                    int(paciente.posicion[0]), 
                    int(paciente.posicion[1]), 
                    paciente, 
                    color,
                    animado=True
                )
    
    def _dibujar_paciente_mejorado(self, x, y, paciente, color, animado=False):
        """Dibuja un paciente individual con mejor diseño"""
        # Sombra del paciente
        pygame.draw.circle(self.pantalla, (180, 180, 180), (int(x) + 2, int(y) + 2), 18)
        
        # Círculo principal
        pygame.draw.circle(self.pantalla, color, (int(x), int(y)), 18)
        
        # Borde
        pygame.draw.circle(self.pantalla, config.COLOR_TEXTO, (int(x), int(y)), 18, 2)
        
        # Número del paciente
        texto = self.fuente_pequena.render(f"#{paciente.id}", True, (255, 255, 255))
        rect_texto = texto.get_rect(center=(int(x), int(y)))
        self.pantalla.blit(texto, rect_texto)
        
        # Indicador de movimiento (pequeña flecha si está en movimiento)
        if animado and paciente.esta_moviendo:
            pygame.draw.circle(self.pantalla, (0, 255, 0), (int(x) + 15, int(y) - 15), 4)
    
    def _dibujar_panel_metricas_mejorado(self):
        """Dibuja el panel de métricas globales con mejor diseño"""
        panel_x = 1200
        panel_y = 80
        panel_ancho = 370
        panel_alto = 420
        
        # Sombra del panel
        pygame.draw.rect(self.pantalla, config.COLOR_SOMBRA,
                        (panel_x + 5, panel_y + 5, panel_ancho, panel_alto), 0, border_radius=12)
        # Panel
        pygame.draw.rect(self.pantalla, config.COLOR_PANEL,
                        (panel_x, panel_y, panel_ancho, panel_alto), 0, border_radius=12)
        # Borde
        pygame.draw.rect(self.pantalla, config.COLOR_BORDE,
                        (panel_x, panel_y, panel_ancho, panel_alto), 2, border_radius=12)
        
        # Título
        pygame.draw.rect(self.pantalla, (60, 90, 140),
                        (panel_x, panel_y, panel_ancho, 50), 0, border_radius=12)
        texto = self.fuente_titulo.render("MÉTRICAS", True, (255, 255, 255))
        self.pantalla.blit(texto, (panel_x + 110, panel_y + 10))
        
        # Obtener métricas
        metricas = self.simulador.obtener_metricas_globales()
        
        y_offset = panel_y + 70
        
        # Tiempo de simulación
        horas = int(metricas['tiempo_simulacion'] // 60)
        minutos = int(metricas['tiempo_simulacion'] % 60)
        texto = self.fuente.render(f"Tiempo: {horas:02d}:{minutos:02d}", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 20, y_offset))
        y_offset += 40
        
        # Pacientes
        texto = self.fuente_pequena.render(f"Pacientes totales: {metricas['total_pacientes']}", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 20, y_offset))
        y_offset += 28
        
        texto = self.fuente_pequena.render(f"Atendidos: {metricas['pacientes_atendidos']}", True, (0, 150, 0))
        self.pantalla.blit(texto, (panel_x + 20, y_offset))
        y_offset += 28
        
        texto = self.fuente_pequena.render(f"En espera: {metricas['pacientes_en_espera']}", True, (200, 100, 0))
        self.pantalla.blit(texto, (panel_x + 20, y_offset))
        y_offset += 45
        
        # Utilización del resonador con barra de progreso
        utilizacion = metricas['utilizacion_resonador']
        texto = self.fuente.render("Utilización Resonador:", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 20, y_offset))
        y_offset += 30
        
        # Barra de progreso
        barra_ancho = 320
        barra_alto = 30
        barra_x = panel_x + 25
        barra_y = y_offset
        
        # Fondo de la barra
        pygame.draw.rect(self.pantalla, (220, 220, 220),
                        (barra_x, barra_y, barra_ancho, barra_alto), 0, border_radius=8)
        
        # Relleno según utilización
        if utilizacion > 0:
            ancho_relleno = int((utilizacion / 100) * barra_ancho)
            color_barra = (0, 200, 0) if utilizacion > 70 else (255, 165, 0) if utilizacion > 50 else (255, 100, 100)
            pygame.draw.rect(self.pantalla, color_barra,
                            (barra_x, barra_y, ancho_relleno, barra_alto), 0, border_radius=8)
        
        # Borde de la barra
        pygame.draw.rect(self.pantalla, config.COLOR_BORDE,
                        (barra_x, barra_y, barra_ancho, barra_alto), 2, border_radius=8)
        
        # Porcentaje
        texto_porc = self.fuente_grande.render(f"{utilizacion:.1f}%", True, config.COLOR_TEXTO)
        rect_porc = texto_porc.get_rect(center=(barra_x + barra_ancho // 2, barra_y + barra_alto // 2))
        self.pantalla.blit(texto_porc, rect_porc)
        
        y_offset += 50
        
        # Estado del resonador
        if metricas['paciente_en_resonador']:
            estado_texto = "● OCUPADO"
            color_estado = (255, 50, 50)
        else:
            estado_texto = "● LIBRE"
            color_estado = (50, 255, 50)
        
        texto = self.fuente.render("Estado:", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 20, y_offset))
        y_offset += 28
        texto = self.fuente_titulo.render(estado_texto, True, color_estado)
        self.pantalla.blit(texto, (panel_x + 90, y_offset - 5))
    
    def _dibujar_panel_paciente_activo_mejorado(self):
        """Dibuja el panel con info del paciente en el resonador"""
        panel_x = 1200
        panel_y = 520
        panel_ancho = 370
        panel_alto = 360
        
        # Sombra del panel
        pygame.draw.rect(self.pantalla, config.COLOR_SOMBRA,
                        (panel_x + 5, panel_y + 5, panel_ancho, panel_alto), 0, border_radius=12)
        # Panel
        pygame.draw.rect(self.pantalla, config.COLOR_PANEL,
                        (panel_x, panel_y, panel_ancho, panel_alto), 0, border_radius=12)
        # Borde
        pygame.draw.rect(self.pantalla, config.COLOR_BORDE,
                        (panel_x, panel_y, panel_ancho, panel_alto), 2, border_radius=12)
        
        # Título
        pygame.draw.rect(self.pantalla, (60, 90, 140),
                        (panel_x, panel_y, panel_ancho, 50), 0, border_radius=12)
        texto = self.fuente_titulo.render("PACIENTE", True, (255, 255, 255))
        self.pantalla.blit(texto, (panel_x + 100, panel_y + 10))
        
        paciente = self.simulador.obtener_paciente_activo()
        
        y_offset = panel_y + 70
        
        if paciente:
            # ID del paciente
            texto = self.fuente_titulo.render(f"Paciente #{paciente.id}", True, (60, 90, 140))
            self.pantalla.blit(texto, (panel_x + 80, y_offset))
            y_offset += 50
            
            # Tipo de estudio (destacado)
            texto = self.fuente_pequena.render("Tipo de estudio:", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 20, y_offset))
            y_offset += 24
            texto = self.fuente.render(f"{paciente.tipo_estudio}", True, (0, 100, 200))
            self.pantalla.blit(texto, (panel_x + 20, y_offset))
            y_offset += 40
            
            # Estado
            texto = self.fuente_pequena.render("Estado:", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 20, y_offset))
            y_offset += 24
            estado_texto = config.ESTADOS_PACIENTE.get(paciente.estado, paciente.estado)
            texto = self.fuente.render(estado_texto, True, (200, 50, 50))
            self.pantalla.blit(texto, (panel_x + 20, y_offset))
            y_offset += 40
            
            # Tiempo en circuito
            if paciente.timestamp_llegada:
                tiempo_en_circuito = (self.simulador.datetime_actual - paciente.timestamp_llegada).total_seconds() / 60
                texto = self.fuente_pequena.render("Tiempo en circuito:", True, config.COLOR_TEXTO)
                self.pantalla.blit(texto, (panel_x + 20, y_offset))
                y_offset += 24
                texto = self.fuente.render(f"{tiempo_en_circuito:.1f} min", True, (0, 150, 0))
                self.pantalla.blit(texto, (panel_x + 20, y_offset))
                y_offset += 35
            
            # Métricas adicionales
            metricas = paciente.obtener_metricas()
            
            y_offset += 10
            texto = self.fuente_pequena.render(f"● Llegada: {metricas['desvio_llegada']:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 20, y_offset))
            y_offset += 24
            
            if paciente.timestamp_fin_validacion:
                texto = self.fuente_pequena.render(f"● Validación: {metricas['tiempo_validacion']:.1f} min", True, config.COLOR_TEXTO)
                self.pantalla.blit(texto, (panel_x + 20, y_offset))
                y_offset += 24
            
            texto = self.fuente_pequena.render(f"● Scan: {metricas['tiempo_scan']:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 20, y_offset))
            
        else:
            texto = self.fuente_titulo.render("Sin paciente", True, (150, 150, 150))
            self.pantalla.blit(texto, (panel_x + 70, panel_y + 160))
    
    def _dibujar_controles_mejorados(self):
        """Dibuja los controles de la simulación con mejor diseño"""
        y = config.VENTANA_ALTO - 60
        
        # Fondo para controles
        pygame.draw.rect(self.pantalla, (250, 250, 250), (0, y - 10, config.VENTANA_ANCHO, 70))
        
        # Estado de pausa
        if self.simulador.pausada:
            texto = self.fuente.render("⏸ PAUSADO", True, (255, 0, 0))
        else:
            texto = self.fuente.render("▶ EJECUTANDO", True, (0, 200, 0))
        self.pantalla.blit(texto, (20, y))
        
        # Velocidad con barra visual
        velocidad_texto = f"Velocidad: {self.velocidad:.0f}x"
        texto = self.fuente_pequena.render(velocidad_texto, True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (200, y + 5))
        
        # Controles
        controles = "ESPACIO: Pausar | ↑↓: Velocidad | R: Reiniciar | ESC: Salir"
        texto = self.fuente_pequena.render(controles, True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (200, y + 30))
    
    def _dibujar_resumen_final(self):
        """Dibuja la pantalla de resumen final del día"""
        # Fondo semi-transparente
        overlay = pygame.Surface((config.VENTANA_ANCHO, config.VENTANA_ALTO))
        overlay.set_alpha(250)
        overlay.fill((245, 245, 250))
        self.pantalla.blit(overlay, (0, 0))
        
        # Panel central del resumen
        panel_x = 200
        panel_y = 100
        panel_ancho = 1200
        panel_alto = 750
        
        # Sombra
        pygame.draw.rect(self.pantalla, (100, 100, 100),
                        (panel_x + 10, panel_y + 10, panel_ancho, panel_alto), 0, border_radius=20)
        # Panel
        pygame.draw.rect(self.pantalla, (255, 255, 255),
                        (panel_x, panel_y, panel_ancho, panel_alto), 0, border_radius=20)
        
        # Título
        pygame.draw.rect(self.pantalla, (60, 90, 140),
                        (panel_x, panel_y, panel_ancho, 80), 0, border_radius=20)
        titulo = self.fuente_grande.render("RESUMEN DEL DÍA", True, (255, 255, 255))
        rect_titulo = titulo.get_rect(center=(panel_x + panel_ancho // 2, panel_y + 40))
        self.pantalla.blit(titulo, rect_titulo)
        
        y_offset = panel_y + 110
        
        # Métricas del día
        metricas = self.simulador.obtener_metricas_globales()
        estadisticas_dia = self.simulador.obtener_estadisticas_dia()
        
        # Información general
        col1_x = panel_x + 80
        col2_x = panel_x + 650
        
        texto = self.fuente_titulo.render("📊 ESTADÍSTICAS GENERALES", True, (60, 90, 140))
        self.pantalla.blit(texto, (col1_x, y_offset))
        y_offset += 60
        
        # Columna 1
        info_general = [
            f"Total de pacientes atendidos: {metricas['pacientes_atendidos']}",
            f"Tiempo total de simulación: {int(metricas['tiempo_simulacion']//60)}h {int(metricas['tiempo_simulacion']%60)}min",
            f"Utilización del resonador: {metricas['utilizacion_resonador']:.1f}%",
            f"Tiempo ocupado: {metricas['tiempo_ocupacion_resonador']:.0f} min",
            f"Tiempo ocioso: {metricas['tiempo_ocioso_resonador']:.0f} min",
        ]
        
        for info in info_general:
            texto = self.fuente.render(info, True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (col1_x, y_offset))
            y_offset += 35
        
        # Tipos de estudios realizados
        y_offset = panel_y + 110 + 60
        texto = self.fuente_titulo.render("🔬 ESTUDIOS REALIZADOS", True, (60, 90, 140))
        self.pantalla.blit(texto, (col2_x, y_offset))
        y_offset += 60
        
        for tipo, cantidad in estadisticas_dia['estudios_por_tipo'].items():
            texto = self.fuente.render(f"{tipo}: {cantidad}", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (col2_x, y_offset))
            y_offset += 35
        
        # Promedios
        y_offset = panel_y + 500
        texto = self.fuente_titulo.render("⏱️ TIEMPOS PROMEDIO", True, (60, 90, 140))
        self.pantalla.blit(texto, (col1_x, y_offset))
        y_offset += 60
        
        promedios = [
            f"Tiempo total por paciente: {estadisticas_dia['tiempo_promedio_total']:.1f} min",
            f"Tiempo de espera: {estadisticas_dia['tiempo_promedio_espera']:.1f} min",
            f"Tiempo en resonador: {estadisticas_dia['tiempo_promedio_resonador']:.1f} min",
        ]
        
        for prom in promedios:
            texto = self.fuente.render(prom, True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (col1_x, y_offset))
            y_offset += 35
        
        # Instrucciones
        y_final = panel_y + panel_alto - 60
        texto = self.fuente.render("Presiona ENTER para continuar o R para reiniciar", True, (100, 100, 100))
        rect_texto = texto.get_rect(center=(panel_x + panel_ancho // 2, y_final))
        self.pantalla.blit(texto, rect_texto)
        
        pygame.display.flip()
