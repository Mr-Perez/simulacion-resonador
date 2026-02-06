"""
VISUALIZACIÓN CON PYGAME
=========================
Interfaz gráfica 2D de la simulación del resonador
"""

import pygame
import sys
import config
from datetime import timedelta

class Visualizador:
    """
    Maneja la visualización gráfica de la simulación usando Pygame
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
        pygame.display.set_caption("Simulación Resonador - Clínica")
        
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 24)
        self.fuente_pequena = pygame.font.Font(None, 18)
        self.fuente_titulo = pygame.font.Font(None, 32)
        
        self.ejecutando = True
        self.velocidad = config.VELOCIDAD_SIMULACION
        
    def ejecutar(self):
        """Bucle principal de la visualización"""
        while self.ejecutando:
            # Procesar eventos
            self._procesar_eventos()
            
            # Actualizar simulación
            delta = self.velocidad / config.FPS
            self.simulador.actualizar(delta)
            
            # Dibujar
            self._dibujar()
            
            # Control de FPS
            self.reloj.tick(config.FPS)
            
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
                    self.velocidad = min(self.velocidad * 2, 960)
                elif evento.key == pygame.K_DOWN:
                    self.velocidad = max(self.velocidad / 2, 15)
                
                # R: reiniciar
                elif evento.key == pygame.K_r:
                    self.simulador.reiniciar()
                    self.simulador.generar_turnos()
                
                # ESC: salir
                elif evento.key == pygame.K_ESCAPE:
                    self.ejecutando = False
    
    def _dibujar(self):
        """Dibuja toda la interfaz"""
        # Fondo
        self.pantalla.fill(config.COLOR_FONDO)
        
        # Dibujar layout de la clínica
        self._dibujar_clinica()
        
        # Dibujar pacientes
        self._dibujar_pacientes()
        
        # Dibujar panel de métricas
        self._dibujar_panel_metricas()
        
        # Dibujar panel de paciente activo
        self._dibujar_panel_paciente_activo()
        
        # Dibujar controles
        self._dibujar_controles()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    def _dibujar_clinica(self):
        """Dibuja el layout de la clínica"""
        layout = config.LAYOUT
        
        # Sala de espera
        pygame.draw.rect(self.pantalla, config.COLOR_SALA_ESPERA,
                        (layout['sala_espera']['x'], layout['sala_espera']['y'],
                         layout['sala_espera']['ancho'], layout['sala_espera']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (layout['sala_espera']['x'], layout['sala_espera']['y'],
                         layout['sala_espera']['ancho'], layout['sala_espera']['alto']), 2)
        texto = self.fuente.render("Sala de Espera", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (layout['sala_espera']['x'] + 10, layout['sala_espera']['y'] + 10))
        
        # Mesa de atención
        pygame.draw.rect(self.pantalla, config.COLOR_MESA,
                        (layout['mesa_atencion']['x'], layout['mesa_atencion']['y'],
                         layout['mesa_atencion']['ancho'], layout['mesa_atencion']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (layout['mesa_atencion']['x'], layout['mesa_atencion']['y'],
                         layout['mesa_atencion']['ancho'], layout['mesa_atencion']['alto']), 2)
        texto = self.fuente.render("Mesa de Atención", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (layout['mesa_atencion']['x'] + 10, layout['mesa_atencion']['y'] + 25))
        
        # Pasillos
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO,
                        (layout['pasillo_vertical']['x'], layout['pasillo_vertical']['y'],
                         layout['pasillo_vertical']['ancho'], layout['pasillo_vertical']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO,
                        (layout['pasillo_horizontal']['x'], layout['pasillo_horizontal']['y'],
                         layout['pasillo_horizontal']['ancho'], layout['pasillo_horizontal']['alto']), 0)
        
        # Cambiador/Vestuario
        pygame.draw.rect(self.pantalla, config.COLOR_CAMBIADOR,
                        (layout['cambiador']['x'], layout['cambiador']['y'],
                         layout['cambiador']['ancho'], layout['cambiador']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (layout['cambiador']['x'], layout['cambiador']['y'],
                         layout['cambiador']['ancho'], layout['cambiador']['alto']), 2)
        texto = self.fuente.render("Vestuario", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (layout['cambiador']['x'] + 50, layout['cambiador']['y'] + 90))
        
        # Box
        pygame.draw.rect(self.pantalla, config.COLOR_BOX,
                        (layout['box']['x'], layout['box']['y'],
                         layout['box']['ancho'], layout['box']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (layout['box']['x'], layout['box']['y'],
                         layout['box']['ancho'], layout['box']['alto']), 2)
        texto = self.fuente_pequena.render("Box", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (layout['box']['x'] + 30, layout['box']['y'] + 40))
        
        # Sala de resonancia
        pygame.draw.rect(self.pantalla, config.COLOR_SALA_ESPERA,
                        (layout['sala_resonancia']['x'], layout['sala_resonancia']['y'],
                         layout['sala_resonancia']['ancho'], layout['sala_resonancia']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (layout['sala_resonancia']['x'], layout['sala_resonancia']['y'],
                         layout['sala_resonancia']['ancho'], layout['sala_resonancia']['alto']), 2)
        texto = self.fuente.render("Sala de Resonancia", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (layout['sala_resonancia']['x'] + 100, layout['sala_resonancia']['y'] + 10))
        
        # Resonador
        pygame.draw.rect(self.pantalla, config.COLOR_RESONADOR,
                        (layout['resonador']['x'], layout['resonador']['y'],
                         layout['resonador']['ancho'], layout['resonador']['alto']), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (layout['resonador']['x'], layout['resonador']['y'],
                         layout['resonador']['ancho'], layout['resonador']['alto']), 3)
        texto = self.fuente.render("RESONADOR", True, (255, 255, 255))
        self.pantalla.blit(texto, (layout['resonador']['x'] + 35, layout['resonador']['y'] + 40))
    
    def _dibujar_pacientes(self):
        """Dibuja los pacientes en sus ubicaciones actuales"""
        # Pacientes en sala de espera
        for i, paciente in enumerate(self.simulador.cola_espera):
            x = config.LAYOUT['sala_espera']['x'] + 50 + (i % 4) * 90
            y = config.LAYOUT['sala_espera']['y'] + 80 + (i // 4) * 80
            self._dibujar_paciente(x, y, paciente, config.COLOR_PACIENTE)
        
        # Paciente en mesa
        if self.simulador.paciente_en_mesa:
            x = config.LAYOUT['mesa_atencion']['x'] + 100
            y = config.LAYOUT['mesa_atencion']['y'] + 40
            self._dibujar_paciente(x, y, self.simulador.paciente_en_mesa, config.COLOR_PACIENTE_ACTIVO)
        
        # Paciente en cambiador
        if self.simulador.paciente_en_cambiador:
            x = config.LAYOUT['cambiador']['x'] + 100
            y = config.LAYOUT['cambiador']['y'] + 100
            self._dibujar_paciente(x, y, self.simulador.paciente_en_cambiador, config.COLOR_PACIENTE_ACTIVO)
        
        # Paciente en resonador
        if self.simulador.paciente_en_resonador:
            x = config.LAYOUT['resonador']['x'] + 100
            y = config.LAYOUT['resonador']['y'] + 50
            self._dibujar_paciente(x, y, self.simulador.paciente_en_resonador, config.COLOR_PACIENTE_ACTIVO)
    
    def _dibujar_paciente(self, x, y, paciente, color):
        """Dibuja un paciente individual"""
        # Círculo del paciente
        pygame.draw.circle(self.pantalla, color, (int(x), int(y)), 15)
        pygame.draw.circle(self.pantalla, config.COLOR_TEXTO, (int(x), int(y)), 15, 2)
        
        # Número del paciente
        texto = self.fuente_pequena.render(f"#{paciente.id}", True, (255, 255, 255))
        rect_texto = texto.get_rect(center=(int(x), int(y)))
        self.pantalla.blit(texto, rect_texto)
    
    def _dibujar_panel_metricas(self):
        """Dibuja el panel de métricas globales"""
        panel_x = 1100
        panel_y = 20
        panel_ancho = 280
        panel_alto = 400
        
        # Fondo del panel
        pygame.draw.rect(self.pantalla, config.COLOR_PANEL,
                        (panel_x, panel_y, panel_ancho, panel_alto), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (panel_x, panel_y, panel_ancho, panel_alto), 2)
        
        # Título
        texto = self.fuente_titulo.render("MÉTRICAS", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 70, panel_y + 10))
        
        # Obtener métricas
        metricas = self.simulador.obtener_metricas_globales()
        
        y_offset = panel_y + 60
        
        # Tiempo de simulación
        horas = int(metricas['tiempo_simulacion'] // 60)
        minutos = int(metricas['tiempo_simulacion'] % 60)
        texto = self.fuente_pequena.render(f"Tiempo: {horas:02d}:{minutos:02d}", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 15, y_offset))
        y_offset += 35
        
        # Pacientes
        texto = self.fuente_pequena.render(f"Pacientes totales: {metricas['total_pacientes']}", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 15, y_offset))
        y_offset += 25
        
        texto = self.fuente_pequena.render(f"Atendidos: {metricas['pacientes_atendidos']}", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 15, y_offset))
        y_offset += 25
        
        texto = self.fuente_pequena.render(f"En espera: {metricas['pacientes_en_espera']}", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 15, y_offset))
        y_offset += 40
        
        # Utilización del resonador
        utilizacion = metricas['utilizacion_resonador']
        color_util = (0, 200, 0) if utilizacion > 70 else (255, 165, 0) if utilizacion > 50 else (255, 0, 0)
        texto = self.fuente_pequena.render(f"Utilización Resonador:", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 15, y_offset))
        y_offset += 25
        texto = self.fuente.render(f"{utilizacion:.1f}%", True, color_util)
        self.pantalla.blit(texto, (panel_x + 90, y_offset))
        y_offset += 40
        
        # Estado del resonador
        if metricas['paciente_en_resonador']:
            estado_texto = "OCUPADO"
            color_estado = (255, 0, 0)
        else:
            estado_texto = "LIBRE"
            color_estado = (0, 200, 0)
        
        texto = self.fuente_pequena.render("Estado Resonador:", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 15, y_offset))
        y_offset += 25
        texto = self.fuente.render(estado_texto, True, color_estado)
        self.pantalla.blit(texto, (panel_x + 80, y_offset))
    
    def _dibujar_panel_paciente_activo(self):
        """Dibuja el panel con info del paciente en el resonador"""
        panel_x = 1100
        panel_y = 440
        panel_ancho = 280
        panel_alto = 380
        
        # Fondo del panel
        pygame.draw.rect(self.pantalla, config.COLOR_PANEL,
                        (panel_x, panel_y, panel_ancho, panel_alto), 0)
        pygame.draw.rect(self.pantalla, config.COLOR_TEXTO,
                        (panel_x, panel_y, panel_ancho, panel_alto), 2)
        
        # Título
        texto = self.fuente_titulo.render("PACIENTE", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (panel_x + 60, panel_y + 10))
        
        paciente = self.simulador.obtener_paciente_activo()
        
        if paciente:
            y_offset = panel_y + 60
            
            # ID del paciente
            texto = self.fuente.render(f"Paciente #{paciente.id}", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 70, y_offset))
            y_offset += 40
            
            # Tipo de estudio
            texto = self.fuente_pequena.render(f"Estudio:", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            y_offset += 20
            texto = self.fuente_pequena.render(f"{paciente.tipo_estudio}", True, (0, 100, 200))
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            y_offset += 35
            
            # Estado
            texto = self.fuente_pequena.render(f"Estado:", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            y_offset += 20
            estado_texto = config.ESTADOS_PACIENTE.get(paciente.estado, paciente.estado)
            texto = self.fuente_pequena.render(estado_texto, True, (200, 0, 0))
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            y_offset += 35
            
            # Tiempo en circuito
            if paciente.timestamp_llegada:
                tiempo_en_circuito = (self.simulador.datetime_actual - paciente.timestamp_llegada).total_seconds() / 60
                texto = self.fuente_pequena.render(f"Tiempo en circuito:", True, config.COLOR_TEXTO)
                self.pantalla.blit(texto, (panel_x + 15, y_offset))
                y_offset += 20
                texto = self.fuente_pequena.render(f"{tiempo_en_circuito:.1f} min", True, (0, 150, 0))
                self.pantalla.blit(texto, (panel_x + 15, y_offset))
                y_offset += 35
            
            # Métricas del paciente
            metricas = paciente.obtener_metricas()
            
            texto = self.fuente_pequena.render(f"Llegada: {metricas['desvio_llegada']:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            y_offset += 22
            
            texto = self.fuente_pequena.render(f"Validación: {metricas['tiempo_validacion']:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            y_offset += 22
            
            texto = self.fuente_pequena.render(f"Scan: {metricas['tiempo_scan']:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(texto, (panel_x + 15, y_offset))
            
        else:
            texto = self.fuente.render("Sin paciente", True, (150, 150, 150))
            self.pantalla.blit(texto, (panel_x + 60, panel_y + 180))
    
    def _dibujar_controles(self):
        """Dibuja los controles de la simulación"""
        y = config.VENTANA_ALTO - 80
        
        # Estado de pausa
        if self.simulador.pausada:
            texto = self.fuente.render("⏸ PAUSADO", True, (255, 0, 0))
        else:
            texto = self.fuente.render("▶ EJECUTANDO", True, (0, 200, 0))
        self.pantalla.blit(texto, (20, y))
        
        # Velocidad
        texto = self.fuente_pequena.render(f"Velocidad: {self.velocidad:.0f}x", True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (20, y + 30))
        
        # Controles
        controles = "ESPACIO: Pausar | ↑↓: Velocidad | R: Reiniciar | ESC: Salir"
        texto = self.fuente_pequena.render(controles, True, config.COLOR_TEXTO)
        self.pantalla.blit(texto, (220, y + 30))
