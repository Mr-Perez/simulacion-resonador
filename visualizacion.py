"""Visualización V3.1 - Con salida completa y resumen automático"""
import pygame
import sys
import config

class Visualizador:
    def __init__(self, simulador):
        pygame.init()
        self.sim = simulador
        self.pantalla = pygame.display.set_mode((config.VENTANA_ANCHO, config.VENTANA_ALTO))
        pygame.display.set_caption("Simulación Resonador V3.1 - GRILLA FLEXIBLE")
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
        self.pacientes_dia_completo = []
    
    def ejecutar(self):
        while self.ejecutando:
            dt_real = self.reloj.tick(config.FPS) / 1000.0
            self._procesar_eventos()
            
            if not self.sim.pausada and not self.sim.finalizada and not self.mostrar_resumen:
                dt_sim = self.velocidad / config.FPS
                mult_vel = 2.0 if self.modo_rapido else 1.0
                self.sim.actualizar(dt_sim, dt_real, mult_vel)
            
            if self.sim.finalizada and not self.mostrar_resumen:
                # Simular día completo antes de mostrar resumen
                self.pacientes_dia_completo = self.sim.simular_dia_completo_rapido()
                self.mostrar_resumen = True
            
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
                if ev.key == pygame.K_RETURN:
                    if self.mostrar_resumen:
                        self.mostrar_resumen = False
                        self.pacientes_dia_completo = []
                elif ev.key == pygame.K_SPACE:
                    if self.sim.pausada:
                        self.sim.reanudar()
                    else:
                        self.sim.pausar()
                elif ev.key == pygame.K_v:
                    self.modo_rapido = not self.modo_rapido
                    self.velocidad = self.velocidad_rapida if self.modo_rapido else self.velocidad_normal
                elif ev.key == pygame.K_s:
                    # Simular día completo y mostrar resumen
                    self.pacientes_dia_completo = self.sim.simular_dia_completo_rapido()
                    self.mostrar_resumen = True
                elif ev.key == pygame.K_r:
                    self.sim.reiniciar()
                    self.mostrar_resumen = False
                    self.pacientes_dia_completo = []
                elif ev.key == pygame.K_ESCAPE:
                    self.ejecutando = False
    
    def _dibujar(self):
        self.pantalla.fill(config.COLOR_FONDO)
        self._dibujar_header()
        self._dibujar_layout()
        self._dibujar_pacientes()
        self._dibujar_metricas()
        self._dibujar_controles()
        pygame.display.flip()
    
    def _dibujar_header(self):
        pygame.draw.rect(self.pantalla, (60, 90, 140), (0, 0, config.VENTANA_ANCHO, 50))
        t = self.fuente_titulo.render("SIMULACIÓN RESONADOR V3.1 - GRILLA FLEXIBLE", True, (255, 255, 255))
        self.pantalla.blit(t, (10, 12))
        
        horas = 8 + int(self.sim.tiempo_actual // 60)
        minutos = int(self.sim.tiempo_actual % 60)
        t_tiempo = self.fuente.render(f"{horas:02d}:{minutos:02d}", True, (255, 255, 255))
        self.pantalla.blit(t_tiempo, (config.VENTANA_ANCHO - 100, 14))
    
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
        
        l = config.LAYOUT['pasillo_vertical']
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO, (l['x'], l['y'], l['ancho'], l['alto']))
        l = config.LAYOUT['pasillo_horizontal']
        pygame.draw.rect(self.pantalla, config.COLOR_PASILLO, (l['x'], l['y'], l['ancho'], l['alto']))
        
        dibujar_area('vestuario', 'VESTUARIO', config.COLOR_VESTUARIO)
        dibujar_area('box', 'Box', config.COLOR_BOX)
        dibujar_area('sala_resonancia', 'SALA DE RESONANCIA', config.COLOR_SALA_RESONANCIA)
        
        l = config.LAYOUT['resonador']
        pygame.draw.rect(self.pantalla, (80, 80, 80), (l['x']+4, l['y']+4, l['ancho'], l['alto']), 0, 10)
        pygame.draw.rect(self.pantalla, config.COLOR_RESONADOR, (l['x'], l['y'], l['ancho'], l['alto']), 0, 10)
        pygame.draw.rect(self.pantalla, (70, 120, 200), (l['x'], l['y'], l['ancho'], l['alto']), 3, 10)
        t = self.fuente_titulo.render("RESONADOR", True, (255, 255, 255))
        r = t.get_rect(center=(l['x']+l['ancho']//2, l['y']+l['alto']//2))
        self.pantalla.blit(t, r)
    
    def _dibujar_pacientes(self):
        for p in self.sim.todos_los_pacientes():
            x, y = int(p.posicion[0]), int(p.posicion[1])
            pygame.draw.circle(self.pantalla, (180, 180, 180), (x+2, y+2), 16)
            
            # Color diferente para pacientes saliendo
            if p.estado == 'SALIENDO':
                color = (100, 255, 100)  # Verde para saliendo
            elif p == self.sim.obtener_paciente_activo():
                color = config.COLOR_PACIENTE_ACTIVO
            else:
                color = config.COLOR_PACIENTE
            
            pygame.draw.circle(self.pantalla, color, (x, y), 16)
            pygame.draw.circle(self.pantalla, config.COLOR_TEXTO, (x, y), 16, 2)
            t = self.fuente_pequena.render(f"#{p.id}", True, (255, 255, 255))
            r = t.get_rect(center=(x, y))
            self.pantalla.blit(t, r)
    
    def _dibujar_metricas(self):
        px, py = 980, 70
        pw, ph = 280, 600
        
        pygame.draw.rect(self.pantalla, (200, 200, 200), (px+4, py+4, pw, ph), 0, 10)
        pygame.draw.rect(self.pantalla, config.COLOR_PANEL, (px, py, pw, ph), 0, 10)
        pygame.draw.rect(self.pantalla, config.COLOR_BORDE, (px, py, pw, ph), 2, 10)
        
        pygame.draw.rect(self.pantalla, (60, 90, 140), (px, py, pw, 40), 0, 10)
        t = self.fuente_titulo.render("MÉTRICAS", True, (255, 255, 255))
        self.pantalla.blit(t, (px+85, py+8))
        
        y = py + 55
        
        p_act = self.sim.obtener_paciente_activo()
        if p_act:
            t = self.fuente.render(f"Paciente #{p_act.id}", True, (60, 90, 140))
            self.pantalla.blit(t, (px+15, y))
            y += 35
            
            t = self.fuente_pequena.render(f"Turno: {p_act.turno_asignado:.0f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            
            t = self.fuente_pequena.render(f"Llegada: {p_act.desvio_llegada:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            
            t = self.fuente_pequena.render(f"Validación: {p_act.tiempo_validacion:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            
            t = self.fuente_pequena.render(f"Tiempo en box: {p_act.tiempo_box:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            t = self.fuente_pequena.render("Tipo de estudio:", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 20
            t = self.fuente.render(p_act.tipo_estudio, True, (0, 100, 200))
            self.pantalla.blit(t, (px+15, y))
            y += 30
            
            t = self.fuente_pequena.render(f"Tiempo estudio: {p_act.tiempo_scan:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 22
            
            t = self.fuente_pequena.render(f"Tiempo salida: {p_act.tiempo_salida:.1f} min", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 25
            
            t = self.fuente_pequena.render(f"Tiempo en circuito:", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 20
            t = self.fuente.render(f"{p_act.calcular_tiempo_circuito():.1f} min", True, (0, 150, 0))
            self.pantalla.blit(t, (px+15, y))
            y += 30
            
            t = self.fuente_pequena.render("Estado actual:", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+15, y))
            y += 20
            estado_txt = config.ESTADOS_PACIENTE.get(p_act.estado, p_act.estado)
            t = self.fuente_pequena.render(estado_txt, True, (200, 50, 50))
            self.pantalla.blit(t, (px+15, y))
            y += 35
        
        pygame.draw.line(self.pantalla, (150, 150, 150), (px+10, y), (px+pw-10, y), 1)
        y += 15
        
        t = self.fuente_pequena.render(f"Programados: {len(self.sim.pacientes_programados)}", True, (100, 100, 100))
        self.pantalla.blit(t, (px+15, y))
        y += 25
        
        t = self.fuente_pequena.render(f"En espera: {len(self.sim.pacientes_en_espera)}", True, (0, 100, 200))
        self.pantalla.blit(t, (px+15, y))
        y += 25
        
        t = self.fuente_pequena.render(f"Completados: {len(self.sim.pacientes_completados)}", True, (0, 150, 0))
        self.pantalla.blit(t, (px+15, y))
    
    def _dibujar_controles(self):
        y = config.VENTANA_ALTO - 50
        pygame.draw.rect(self.pantalla, (250, 250, 250), (0, y-5, config.VENTANA_ANCHO, 60))
        
        if self.sim.pausada:
            t = self.fuente.render("⏸ PAUSADO", True, (255, 0, 0))
        elif self.sim.finalizada:
            t = self.fuente.render("✓ FINALIZADO", True, (0, 150, 0))
        else:
            t = self.fuente.render("▶ EJECUTANDO", True, (0, 200, 0))
        self.pantalla.blit(t, (15, y))
        
        vel_texto = "Velocidad: Normal" if not self.modo_rapido else "Velocidad: 2x 🚀"
        t = self.fuente_pequena.render(vel_texto, True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (15, y+25))
        
        controles = "ESPACIO: Pausa | V: Velocidad | S: Resumen día completo | R: Reiniciar | ESC: Salir"
        t = self.fuente_pequena.render(controles, True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (200, y+25))
    
    def _dibujar_resumen(self):
        overlay = pygame.Surface((config.VENTANA_ANCHO, config.VENTANA_ALTO))
        overlay.set_alpha(250)
        overlay.fill((245, 245, 250))
        self.pantalla.blit(overlay, (0, 0))
        
        px, py = 150, 100
        pw, ph = 980, 760
        
        pygame.draw.rect(self.pantalla, (100, 100, 100), (px+8, py+8, pw, ph), 0, 15)
        pygame.draw.rect(self.pantalla, (255, 255, 255), (px, py, pw, ph), 0, 15)
        pygame.draw.rect(self.pantalla, (60, 90, 140), (px, py, pw, 60), 0, 15)
        
        t = self.fuente_titulo.render("RESUMEN DEL DÍA COMPLETO - GRILLA FLEXIBLE", True, (255, 255, 255))
        r = t.get_rect(center=(px+pw//2, py+30))
        self.pantalla.blit(t, r)
        
        y = py + 90
        
        # Usar pacientes simulados del día completo
        stats = self.sim.obtener_estadisticas_dia(self.pacientes_dia_completo)
        
        t = self.fuente.render(f"Total de pacientes: {stats['total_pacientes']}", True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (px+50, y))
        y += 40
        
        t = self.fuente_pequena.render("Jornada laboral: 08:00 - 20:00 (720 min)", True, (100, 100, 100))
        self.pantalla.blit(t, (px+50, y))
        y += 35
        
        t = self.fuente.render(f"Último turno dado: {stats['ultimo_turno_hora']} ({stats['ultimo_turno_min']:.0f} min)", 
                              True, (200, 100, 0))
        self.pantalla.blit(t, (px+50, y))
        y += 30
        
        t = self.fuente.render(f"Finalización: {stats['hora_finalizacion_hora']} ({stats['hora_finalizacion_min']:.0f} min)", 
                              True, (200, 0, 0))
        self.pantalla.blit(t, (px+50, y))
        y += 40
        
        if stats['hora_finalizacion_min'] > 720:
            minutos_extra = stats['hora_finalizacion_min'] - 720
            t = self.fuente.render(f"⚠️ HORAS EXTRAS: {minutos_extra:.0f} minutos", True, (255, 0, 0))
            self.pantalla.blit(t, (px+70, y))
            y += 40
        else:
            t = self.fuente_pequena.render("✓ Sin horas extras", True, (0, 150, 0))
            self.pantalla.blit(t, (px+70, y))
            y += 35
        
        t = self.fuente.render("Estudios realizados:", True, (60, 90, 140))
        self.pantalla.blit(t, (px+50, y))
        y += 35
        
        for tipo, cant in stats['estudios_por_tipo'].items():
            t = self.fuente_pequena.render(f"  • {tipo}: {cant}", True, config.COLOR_TEXTO)
            self.pantalla.blit(t, (px+70, y))
            y += 28
        
        y += 20
        
        t = self.fuente.render(f"Tiempo promedio por paciente: {stats['tiempo_promedio_total']:.1f} min", 
                              True, config.COLOR_TEXTO)
        self.pantalla.blit(t, (px+50, y))
        
        y = py + ph - 50
        t = self.fuente_pequena.render("Presiona ENTER para continuar o R para reiniciar", True, (100, 100, 100))
        r = t.get_rect(center=(px+pw//2, y))
        self.pantalla.blit(t, r)
        
        pygame.display.flip()
