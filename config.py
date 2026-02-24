"""Configuración del simulador V3.1"""

# ============================================================================
# CONFIGURACIÓN DE JORNADA
# ============================================================================
HORA_INICIO = 8
HORA_FIN = 20
INTERVALO_TURNOS = 30

# ============================================================================
# TIPOS DE ESTUDIOS Y PROBABILIDADES
# ============================================================================
TIPOS_ESTUDIO = {
    'Cerebro': {
        'probabilidad': 0.25,
        'tiempo_scan': (4, 6),
        'tiempo_posicionamiento': (1, 2)
    },
    'Columna': {
        'probabilidad': 0.25,
        'tiempo_scan': (5, 7),
        'tiempo_posicionamiento': (1, 2)
    },
    'Articulaciones': {
        'probabilidad': 0.33,
        'tiempo_scan': (4, 6),
        'tiempo_posicionamiento': (1, 2)
    },
    'Cuerpo completo': {
        'probabilidad': 0.02,
        'tiempo_scan': (20, 30),
        'tiempo_posicionamiento': (2, 4)
    },
    'Otros': {
        'probabilidad': 0.15,
        'tiempo_scan': (4, 8),
        'tiempo_posicionamiento': (1, 3)
    }
}

# ============================================================================
# TIEMPOS DE PROCESO (tuplas min, max en minutos)
# ============================================================================
TIEMPO_VALIDACION = (3, 7)
TIEMPO_BOX = (3, 6)  # REDUCIDO de (3,9) a (3,6)
TIEMPO_SALIDA = (3, 5)

# Probabilidades de llegada
PROB_LLEGADA_TEMPRANO = 0.20
PROB_LLEGADA_PUNTUAL = 0.30
PROB_LLEGADA_TARDE = 0.50

# ============================================================================
# INTERFAZ GRÁFICA
# ============================================================================
VENTANA_ANCHO = 1280
VENTANA_ALTO = 960

COLOR_FONDO = (240, 240, 245)
COLOR_SALA_ESPERA = (200, 220, 255)
COLOR_MESA = (180, 200, 240)
COLOR_PASILLO = (220, 220, 220)
COLOR_VESTUARIO = (255, 240, 200)
COLOR_BOX = (255, 200, 200)
COLOR_SALA_RESONANCIA = (200, 230, 255)
COLOR_RESONADOR = (70, 120, 200)
COLOR_PACIENTE = (100, 150, 255)
COLOR_PACIENTE_ACTIVO = (255, 100, 100)
COLOR_TEXTO = (50, 50, 50)
COLOR_BORDE = (100, 100, 100)
COLOR_PANEL = (250, 250, 250)

# ============================================================================
# LAYOUT
# ============================================================================
LAYOUT = {
    'sala_espera': {'x': 30, 'y': 480, 'ancho': 240, 'alto': 420},
    'mesa_atencion': {'x': 50, 'y': 540, 'ancho': 200, 'alto': 80},
    'pasillo_vertical': {'x': 350, 'y': 100, 'ancho': 50, 'alto': 800},
    'pasillo_horizontal': {'x': 350, 'y': 280, 'ancho': 500, 'alto': 70},
    'vestuario': {'x': 475, 'y': 380, 'ancho': 450, 'alto': 250},
    'box': {'x': 760, 'y': 420, 'ancho': 140, 'alto': 90},
    'sala_resonancia': {'x': 475, 'y': 640, 'ancho': 450, 'alto': 260},
    'resonador': {'x': 575, 'y': 720, 'ancho': 250, 'alto': 140}
}

# ============================================================================
# WAYPOINTS - Incluye ruta de SALIDA completa
# ============================================================================
WAYPOINTS = {
    'esperando': (150, 950),
    'entrada': (150, 920),
    'sala_espera': (150, 700),
    'mesa': (150, 595),
    'salida_sala': (270, 595),
    'pasillo_v': (375, 595),
    'pasillo_v_arriba': (375, 315),
    'pasillo_h': (600, 315),
    'pasillo_h_derecha': (800, 315),
    'entrada_vestuario': (705, 380),
    'vestuario': (705, 515),
    'box': (845, 465),
    'vuelta_vestuario': (705, 515),
    'entrada_resonancia': (705, 630),
    'resonancia': (705, 790),
    'resonador': (705, 790),
    # RUTA DE SALIDA (nueva)
    'salida_resonancia': (705, 630),
    'salida_vestuario': (705, 515),
    'salida_pasillo_h': (600, 315),
    'salida_pasillo_v': (375, 595),
    'retorno_sala': (270, 595),
    'salida_final': (150, 950)
}

ESTADOS_PACIENTE = {
    'PROGRAMADO': 'Programado',
    'LLEGADA': 'Llegando',
    'VALIDACION': 'En mesa de atención',
    'BOX': 'En box',
    'RESONADOR': 'En resonador',
    'SALIENDO': 'Saliendo',
    'COMPLETADO': 'Completado',
    'CAMINANDO_VESTUARIO': 'Caminando al vestuario'
}

# Velocidad
VELOCIDAD_PACIENTE = 120
VELOCIDAD_SIMULACION_DEFAULT = 5  # REDUCIDA de 10 a 5 para ver mejor las llegadas
FPS = 60
MOSTRAR_RESUMEN_FINAL = True
