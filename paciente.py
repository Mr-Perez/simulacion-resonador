import config
import math

class Paciente:
    def __init__(self, turno_minutos, fecha_inicio):
        self.turno_minutos = turno_minutos
        self.fecha_inicio = fecha_inicio

        self.ruta = config.RUTA_PACIENTE
        self.waypoints = config.WAYPOINTS

        self.indice_ruta = 0
        self.posicion = list(self.waypoints[self.ruta[0]])
        self.destino = self.waypoints[self.ruta[1]]

        self.completado = False

    def actualizar(self, dt):
        if self.completado:
            return

        dx = self.destino[0] - self.posicion[0]
        dy = self.destino[1] - self.posicion[1]
        distancia = math.hypot(dx, dy)

        if distancia < 1:
            self.indice_ruta += 1
            if self.indice_ruta >= len(self.ruta) - 1:
                self.completado = True
                return
            self.destino = self.waypoints[self.ruta[self.indice_ruta + 1]]
            return

        vx = dx / distancia
        vy = dy / distancia

        self.posicion[0] += vx * config.PACIENTE_SPEED * dt
        self.posicion[1] += vy * config.PACIENTE_SPEED * dt
