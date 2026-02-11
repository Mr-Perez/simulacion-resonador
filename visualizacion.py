"""Visualización V2.1 - Control Manual + Métricas Siempre Visibles"""
import pygame
import sys
import config

class Visualizador:
    def __init__(self, simulador):
        pygame.init()
        self.sim = simulador
        self.pantalla = pygame.display.set_mode((config.VENTANA_ANCHO, config.VENTANA_ALTO))
        pygame.display.set_caption("Simulación Resonador V2.1 - CONTROL MANUAL")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.Font(None, 22)
        self.fuente_pequena = pygame.font.Font(None, 18)
        self.fuente_titulo = pygame.font.Font(None, 28)
        self.ejecutando = True
        self.velocidad_normal = config.VELOCIDAD_SIMULACION_DEFAULT
        self.velocidad_rapida = self.velocidad_normal * 2
        self.velocidad = self.velocidad_normal
        self.modo_rapido = False
        self.mostrar_resumen = False
        self.pacientes_dia_completo = []  # Para almacenar simulación completa del día
    
    def ejecutar(self):
        while self.ejecutando:
            dt_real = self.reloj.tick(config.FPS) / 1000.0
            self._procesar_eventos()
            
            if not self.sim.pausada and not self.sim.finalizada:
                dt_sim = self.velocidad / config.FPS
                # Pasar multiplicador de velocidad (2.0 si modo rápido, 1.0 normal)
                mult_vel = 2.0 if self.modo_rapido else 1.0
                self.sim.actualizar(dt_sim, dt_real, mult_vel)
            
            if self.mostrar_resumen:
                self._dibujar_resumen()
            else:
                self._dibujar()
            
        pygame.quit()
        sys.exit()
    
    def _procesar_eventos(self):
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                self.ejecutando = False
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN:  # ENTER
                    if self.sim.esperando_input:
                        self.sim.crear_siguiente_paciente()
                    elif self.mostrar_resumen:
                        self.mostrar_resumen = False
                elif ev.key == pygame.K_SPACE:
                    self.sim.pausar() if not self.sim.pausada else self.sim.reanudar()
                elif ev.key == pygame.K_v:  # V: Cambiar velocidad
                    self.modo_rapido = not self.modo_rapido
                    self.velocidad = self.velocidad_rapida if self.modo_rapido else self.velocidad_normal
                elif ev.key == pygame.K_s:  # S: Simular y mostrar resumen del día
                    # Simular día completo
                    self.pacientes_dia_completo = self.sim.simular_dia_completo()
                    self.mostrar_resumen = True
                elif ev.key == pygame.K_r:
                    self.sim.reiniciar()
                    self.mostrar_resumen = False
                    self.pacientes_dia_completo = []  # Limpiar simulación del día
                elif ev.key == pygame.K_ESCAPE:
                    self.ejecutando = False
    
    def _dibujar(self):
        self.pantalla.fill(config.COLOR_FONDO)
        self._dibujar_header()
        self._dibujar_layout()
        self._dibujar_paciente()
        self._dibujar_metricas()
        self._dibujar_controles()
        pygame.display.flip()
    
    def _dibujar_header(self):
        pygame.draw.rect(self.pantalla, (60, 90, 140), (0, 0, config.VENTANA_ANCHO, 50))
        t = self.fuente_titulo.render("SIMULACIÓN RESONADOR V2.1 - CONTROL MANUAL", True, (255, 255, 255))
        self.pantalla.blit(t, (10, 12))
    
    def _dibujar_layout(self):
        def dibujar_area(key, nombre, color):
            l = config.LAYOUT[key]
            pygame.draw.rect(self.pantalla, (200, 200, 200), (l['x']+3, l['y']+3, l['ancho'], l['alto']), 0, 8)
            pygame.draw.rect(self.pantalla, color, (l['x'], l['y'], l['ancho'], l['alto']), 0, 8)
            pygame.draw.rect(self.pantalla, config.COLOR_BORDE, (l['x'], l['y'], l['ancho'], l['alto']), 2, 8)
            t = self.fuente_pequena.render(nombre, True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (l['x']+10, l['y']+10))
        
        dibujar_area('sala_espera', 'SALA DE ESPERA', config.COLOR_SALA_ESPERA)
        dibujar_area('mesa_atencion', 'Mesa', config.COLOR_MESA)
        
        # Pasillos
        l = config.LAYOUT['pasillo_vertical']
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO, (l['x'], l['y'], l['ancho'], l['alto']))
        l = config.LAYOUT['pasillo_horizontal']
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO, (l['x'], l['y'], l['ancho'], l['alto']))
        
        dibujar_area('vestuario', 'VESTUARIO', config.COLOR_VESTUARIO)
        dibujar_area('box', 'Box', config.COLOR_BOX)
        dibujar_area('sala_resonancia', 'SALA DE RESONANCIA', config.COLOR_SALA_RESONANCIA)
        
        # Resonador destacado
        l = config.LAYOUT['resonador']
        pygame.draw.rect(self.pantalla, (80, 80, 80), (l['x']+4, l['y']+4, l['ancho'], l['alto']), 0, 10)
        pygame.draw.rect(self.pantalla, config.COLOR_RESONADOR, (l['x'], l['y'], l['ancho'], l['alto']), 0, 10)
        pygame.draw.rect(self.pantalla, (70, 120, 200), (l['x'], l['y'], l['ancho'], l['alto']), 3, 10)
        t = self.fuente_titulo.render("RESONADOR", True, (255, 255, 255))
        r = t.get_rect(center=(l['x']+l['ancho']//2, l['y']+l['alto']//2))
        self.pantalla.blit(t, r)
    
    def _dibujar_paciente(self):
        if self.sim.paciente_actual:
            p = self.sim.paciente_actual
            x, y = int(p.posicion[0]), int(p.posicion[1])
            pygame.draw.circle(self.pantalla, (180, 180, 180), (x+2, y+2), 16)
            pygame.draw.circle(self.pantalla, config.COLOR_PACIENTE_ACTIVO, (x, y), 16)
            pygame.draw.circle(self.pantalla, config.COLOR_TEXTO, (x, y), 16, 2)
            t = self.fuente_pequena.render(f"#{p.id}", True, (255, 255, 255))
            r = t.get_rect(center=(x, y))
            self.pantalla.blit(t, r)
    
    def _dibujar_metricas(self):
        px, py = 980, 70
        pw, ph = 280, 550
        
        # Panel
        pygame.draw.rect(self.pantalla, (200, 200, 200), (px+4, py+4, pw, ph), 0, 10)
        pygame.draw.rect(self.pantalla, config.COLOR_PANEL, (px, py, pw, ph), 0, 10)
        pygame.draw.rect(self.pantalla, config.COLOR_BORDE, (px, py, pw, ph), 2, 10)
        
        # Título
        pygame.draw.rect(self.pantalla, (60, 90, 140), (px, py, pw, 40), 0, 10)
        t = self.fuente_titulo.render("MÉTRICAS", True, (255, 255, 255))
        self.pantalla.blit(t, (px+85, py+8))
        
        y = py + 55
        
        if self.sim.paciente_actual:
            p = self.sim.paciente_actual
            
            # Paciente #
            t = self.fuente.render(f"Paciente #{p.id}", True, (60, 90, 140))
            self.pantalla.blit(t, (px+15, y))
            y += 35
            
            # Llegada
            t = self.fuente_pequena.render(f"Llegada: {p.desvio_llegada:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            # Validación
            t = self.fuente_pequena.render(f"Validación: {p.tiempo_validacion:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            # Tiempo en box (cambiador)
            t = self.fuente_pequena.render(f"Tiempo en box: {p.tiempo_box:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            # Tipo de estudio
            t = self.fuente_pequena.render("Tipo de estudio:", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            t = self.fuente.render(p.tipo_estudio, True, (0, 100, 200))
            self.pantalla.blit(t, (px+15, y))
            y += 35
            
            # Tiempo de estudio
            t = self.fuente_pequena.render(f"Tiempo estudio: {p.tiempo_scan:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            # Tiempo de salida (vestuario)
            t = self.fuente_pequena.render(f"Tiempo salida: {p.tiempo_salida:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            # Tiempo en circuito (SUMA de todas las etapas)
            tiempo_circuito = p.calcular_tiempo_circuito()
            t = self.fuente_pequena.render("Tiempo en circuito:", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            t = self.fuente.render(f"{tiempo_circuito:.1f} min", True, (0, 150, 0))
            self.pantalla.blit(t, (px+15, y))
            y += 35
            
            # Estado actual
            t = self.fuente_pequena.render("Estado actual:", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            estado_txt = config.ESTADOS_PACIENTE.get(p.estado, p.estado)
            t = self.fuente_pequena.render(estado_txt, True, (200, 50, 50))
            self.pantalla.blit(t, (px+15, y))
            
        elif self.sim.esperando_input:
            t = self.fuente.render("Esperando paciente...", True, (150, 150, 150))
            self.pantalla.blit(t, (px+40, py+250))
            t = self.fuente_pequena.render("Presiona ENTER", True, (100, 100, 100))
            self.pantalla.blit(t, (px+70, py+280))
        
        # Completados
        y = py + ph - 60
        t = self.fuente_pequena.render(f"Pacientes completados: {len(self.sim.pacientes_completados)}", True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (px+15, y))
    
    def _dibujar_controles(self):
        y = config.VENTANA_ALTO - 50
        pygame.draw.rect(self.pantalla, (250, 250, 250), (0, y-5, config.VENTANA_ANCHO, 60))
        
        if self.sim.pausada:
            t = self.fuente.render("⏸ PAUSADO", True, (255, 0, 0))
        else:
            t = self.fuente.render("▶ EJECUTANDO", True, (0, 200, 0))
        self.pantalla.blit(t, (15, y))
        
        # Mostrar velocidad actual
        vel_texto = "Velocidad: 2x 🚀" if self.modo_rapido else "Velocidad: Normal"
        t = self.fuente_pequena.render(vel_texto, True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (15, y+25))
        
        # Controles actualizados
        controles = "ENTER: Siguiente | ESPACIO: Pausa | V: Velocidad | S: Resumen | R: Reiniciar | ESC: Salir"
        t = self.fuente_pequena.render(controles, True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (200, y+25))
    
    def _dibujar_resumen(self):
        overlay = pygame.Surface((config.VENTANA_ANCHO, config.VENTANA_ALTO))
        overlay.set_alpha(250)
        overlay.fill((245, 245, 250))
        self.pantalla.blit(overlay, (0, 0))
        
        px, py = 150, 150
        pw, ph = 980, 660
        
        pygame.draw.rect(self.pantalla, (100, 100, 100), (px+8, py+8, pw, ph), 0, 15)
        pygame.draw.rect(self.pantalla, (255, 255, 255), (px, py, pw, ph), 0, 15)
        pygame.draw.rect(self.pantalla, (60, 90, 140), (px, py, pw, 60), 0, 15)
        
        t = self.fuente_titulo.render("RESUMEN DEL DÍA COMPLETO", True, (255, 255, 255))
        r = t.get_rect(center=(px+pw//2, py+30))
        self.pantalla.blit(t, r)
        
        y = py + 100
        
        # Obtener estadísticas de la simulación completa del día
        stats = self.sim.obtener_estadisticas_dia(self.pacientes_dia_completo)
        
        # Total de pacientes
        t = self.fuente.render(f"Total de pacientes: {stats['total_pacientes']}", True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (px+50, y))
        y += 40
        
        # Jornada laboral
        t = self.fuente_pequena.render("Jornada: 08:00 - 20:00 (720 minutos)", True, (100, 100, 100))
        self.pantalla.blit(t, (px+50, y))
        y += 35
        
        # Estudios realizados
        t = self.fuente.render("Estudios realizados:", True, (60, 90, 140))
        self.pantalla.blit(t, (px+50, y))
        y += 35
        
        for tipo, cant in stats['estudios_por_tipo'].items():
            t = self.fuente_pequena.render(f"  • {tipo}: {cant}", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+70, y))
            y += 28
        
        y += 30
        
        # Tiempo promedio
        t = self.fuente.render(f"Tiempo promedio por paciente: {stats['tiempo_promedio_total']:.1f} min", True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (px+50, y))
        y += 40
        
        # Pacientes procesados manualmente (si hay)
        if self.sim.pacientes_completados:
            t = self.fuente_pequena.render(f"(Procesados manualmente: {len(self.sim.pacientes_completados)})", True, (100, 100, 100))
            self.pantalla.blit(t, (px+50, y))
        
        y = py + ph - 50
        t = self.fuente_pequena.render("Presiona ENTER para continuar o R para reiniciar", True, (100, 100, 100))
        r = t.get_rect(center=(px+pw//2, y))
        self.pantalla.blit(t, r)
        
        pygame.display.flip()
