"""
CONFIGURACIÓN DE LA SIMULACIÓN - RESONADOR MRI
==============================================
Todos los parámetros estadísticos y configuraciones del sistema
"""

# ============================================================================
# TIPOS DE ESTUDIOS Y PROBABILIDADES
# ============================================================================
TIPOS_ESTUDIOS = {
    'Cerebro': {
        'duracion': 4.45,  # minutos
        'probabilidad': 0.25
    },
    'Columna': {
        'duracion': 5.20,
        'probabilidad': 0.25
    },
    'Articulaciones': {
        'duracion': 4.53,
        'probabilidad': 0.33
    },
    'Cuerpo completo': {
        'duracion': 20.0,
        'probabilidad': 0.02
    },
    'Otros': {
        'duracion': 5.0,
        'probabilidad': 0.15
    }
}

# ============================================================================
# TIEMPOS DE LLEGADA DEL PACIENTE
# ============================================================================
LLEGADA_PROBABILIDADES = {
    'temprano': {'minutos': -5, 'probabilidad': 0.20},  # 5 min antes
    'puntual': {'minutos': 0, 'probabilidad': 0.30},     # A horario
    'tarde': {'minutos_min': 5, 'minutos_max': 10, 'probabilidad': 0.50}  # 5-10 min tarde
}

# ============================================================================
# DISTRIBUCIONES NORMALES (μ, σ)
# ============================================================================
# Validación administrativa (mesa de atención)
VALIDACION_MESA = {
    'media': 5.0,      # μ = 5 minutos
    'desviacion': 1.0  # σ = 1 minuto
}

# Tiempo en cambiador (entrada)
CAMBIADOR_ENTRADA = {
    'media': 6.0,      # μ = 6 minutos
    'desviacion': 1.5  # σ = 1.5 minutos
}

# Tiempo en cambiador (salida)
CAMBIADOR_SALIDA = {
    'media': 4.0,      # μ = 4 minutos
    'desviacion': 1.0  # σ = 1 minuto
}

# Tiempo de posicionamiento del paciente en el resonador
POSICIONAMIENTO = {
    'media': 3.0,      # μ = 3 minutos
    'desviacion': 0.5  # σ = 0.5 minutos
}

# Margen de error/limpieza entre pacientes
MARGEN_ERROR = 2.0  # minutos fijos

# ============================================================================
# CONFIGURACIÓN DE TURNOS
# ============================================================================
HORA_INICIO = 8  # 8:00 AM
HORA_FIN = 18    # 6:00 PM
INTERVALO_TURNOS = 30  # minutos entre turnos (se puede modificar)

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================
VENTANA_ANCHO = 1400
VENTANA_ALTO = 900

# Colores (RGB)
COLOR_FONDO = (240, 240, 245)
COLOR_SALA_ESPERA = (200, 220, 240)
COLOR_MESA = (180, 200, 220)
COLOR_PASILLO = (220, 220, 220)
COLOR_CAMBIADOR = (255, 230, 200)
COLOR_BOX = (255, 200, 200)
COLOR_RESONADOR = (150, 180, 220)
COLOR_PACIENTE = (50, 150, 250)
COLOR_PACIENTE_ACTIVO = (255, 100, 100)
COLOR_TEXTO = (50, 50, 50)
COLOR_PANEL = (255, 255, 255)

# Estados de paciente (para visualización)
ESTADOS_PACIENTE = {
    'LLEGADA': 'Llegando',
    'ESPERA': 'En sala de espera',
    'VALIDACION': 'En mesa de atención',
    'CAMBIADOR_IN': 'Cambiándose',
    'ESPERANDO_RESONADOR': 'Esperando turno',
    'RESONADOR': 'En resonador',
    'CAMBIADOR_OUT': 'Vistiéndose',
    'SALIDA': 'Saliendo',
    'COMPLETADO': 'Completado'
}

# ============================================================================
# LAYOUT DE LA CLÍNICA (coordenadas en píxeles)
# ============================================================================
LAYOUT = {
    'sala_espera': {'x': 50, 'y': 300, 'ancho': 400, 'alto': 450},
    'mesa_atencion': {'x': 150, 'y': 200, 'ancho': 200, 'alto': 80},
    'pasillo_vertical': {'x': 470, 'y': 50, 'ancho': 120, 'alto': 700},
    'pasillo_horizontal': {'x': 590, 'y': 50, 'ancho': 350, 'alto': 120},
    'cambiador': {'x': 650, 'y': 400, 'ancho': 200, 'alto': 200},
    'box': {'x': 750, 'y': 230, 'ancho': 100, 'alto': 100},
    'sala_resonancia': {'x': 650, 'y': 620, 'ancho': 400, 'alto': 250},
    'resonador': {'x': 750, 'y': 700, 'ancho': 200, 'alto': 100}
}

# Posiciones de movimiento (waypoints)
WAYPOINTS = {
    'entrada': (250, 100),
    'sala_espera': (250, 500),
    'mesa': (250, 240),
    'pasillo_inicio': (530, 240),
    'pasillo_medio': (530, 400),
    'cambiador': (750, 500),
    'box': (800, 280),
    'sala_resonador': (850, 650),
    'resonador': (850, 750),
    'salida': (250, 100)
}

# ============================================================================
# CONFIGURACIÓN DE SIMULACIÓN
# ============================================================================
VELOCIDAD_SIMULACION = 60  # Cuántos minutos simulados por segundo real (ajustable)
FPS = 60  # Frames por segundo de la visualización
