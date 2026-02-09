"""
CONFIGURACIÓN DE LA SIMULACIÓN - RESONADOR MRI V2.1
====================================================
VERSIÓN CORREGIDA - Control manual y flujo correcto
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

# Tiempo en box (cambiador)
BOX_CAMBIO = {
    'media': 6.0,      # μ = 6 minutos
    'desviacion': 1.5  # σ = 1.5 minutos
}

# Tiempo de posicionamiento del paciente en el resonador
POSICIONAMIENTO = {
    'media': 3.0,      # μ = 3 minutos
    'desviacion': 0.5  # σ = 0.5 minutos
}

# ============================================================================
# CONFIGURACIÓN DE TURNOS
# ============================================================================
HORA_INICIO = 8  # 8:00 AM
HORA_FIN = 18    # 6:00 PM
INTERVALO_TURNOS = 30  # minutos entre turnos

# MODO DE CONTROL
MODO_MANUAL = True  # Control manual con ENTER

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN - 1280x960
# ============================================================================
VENTANA_ANCHO = 1280
VENTANA_ALTO = 960

# Colores profesionales
COLOR_FONDO = (245, 247, 250)
COLOR_SALA_ESPERA = (220, 235, 255)
COLOR_MESA = (200, 220, 240)
COLOR_PASILLO = (235, 235, 235)
COLOR_VESTUARIO = (255, 240, 220)
COLOR_BOX = (255, 200, 200)
COLOR_SALA_RESONANCIA = (230, 245, 255)
COLOR_RESONADOR = (100, 150, 220)
COLOR_PACIENTE = (50, 150, 250)
COLOR_PACIENTE_ACTIVO = (255, 100, 100)
COLOR_TEXTO = (40, 40, 40)
COLOR_PANEL = (255, 255, 255)
COLOR_BORDE = (180, 180, 180)
COLOR_SOMBRA = (200, 200, 200)

# Estados de paciente
ESTADOS_PACIENTE = {
    'ESPERANDO': 'Esperando inicio',
    'LLEGADA': 'Llegando',
    'ESPERA': 'En sala de espera',
    'VALIDACION': 'En mesa de atención',
    'CAMINANDO_PASILLO': 'Caminando',
    'VESTUARIO': 'En vestuario',
    'BOX': 'En box',
    'RESONADOR': 'En resonador',
    'SALIDA': 'Saliendo',
    'COMPLETADO': 'Completado'
}

# ============================================================================
# LAYOUT - EXACTO SEGÚN TU IMAGEN 3
# ============================================================================
LAYOUT = {
    # Sala de espera (abajo izquierda)
    'sala_espera': {'x': 30, 'y': 500, 'ancho': 240, 'alto': 390},
    
    # Mesa (dentro de sala de espera)
    'mesa_atencion': {'x': 50, 'y': 520, 'ancho': 200, 'alto': 70},
    
    # Pasillo vertical
    'pasillo_vertical': {'x': 290, 'y': 250, 'ancho': 170, 'alto': 640},
    
    # Pasillo horizontal
    'pasillo_horizontal': {'x': 30, 'y': 250, 'ancho': 900, 'alto': 130},
    
    # Vestuario (GRANDE, contiene el box)
    'vestuario': {'x': 480, 'y': 400, 'ancho': 450, 'alto': 230},
    
    # Box (DENTRO del vestuario)
    'box': {'x': 780, 'y': 420, 'ancho': 130, 'alto': 90},
    
    # Sala de resonancia
    'sala_resonancia': {'x': 480, 'y': 650, 'ancho': 450, 'alto': 240},
    
    # Resonador
    'resonador': {'x': 580, 'y': 730, 'ancho': 250, 'alto': 120}
}

# ============================================================================
# WAYPOINTS - FLUJO CORRECTO
# Sala espera → Mesa → Pasillo → Vestuario → Box → Resonador
# ============================================================================
WAYPOINTS = {
    'esperando': (150, 950),
    'entrada': (150, 920),
    'sala_espera': (150, 700),
    'mesa': (150, 555),
    'salida_sala': (270, 555),
    'pasillo_v': (375, 555),
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
    'salida': (150, 950)
}

# Velocidad
VELOCIDAD_PACIENTE = 120
VELOCIDAD_SIMULACION_DEFAULT = 30
FPS = 60
MOSTRAR_RESUMEN_FINAL = True
