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
VENTANA_ANCHO = 1600
VENTANA_ALTO = 950

# Colores profesionales (RGB)
COLOR_FONDO = (245, 247, 250)
COLOR_SALA_ESPERA = (220, 235, 255)
COLOR_MESA = (200, 220, 240)
COLOR_PASILLO = (235, 235, 235)
COLOR_VESTUARIO = (255, 240, 220)
COLOR_BOX = (255, 220, 220)
COLOR_SALA_RESONANCIA = (230, 245, 255)
COLOR_RESONADOR = (100, 150, 220)
COLOR_PACIENTE = (50, 150, 250)
COLOR_PACIENTE_ACTIVO = (255, 100, 100)
COLOR_TEXTO = (40, 40, 40)
COLOR_PANEL = (255, 255, 255)
COLOR_BORDE = (180, 180, 180)
COLOR_SOMBRA = (200, 200, 200)

# Estados de paciente (para visualización)
ESTADOS_PACIENTE = {
    'LLEGADA': 'Llegando',
    'ESPERA': 'En sala de espera',
    'VALIDACION': 'En mesa de atención',
    'CAMINANDO_PASILLO': 'Caminando por pasillo',
    'CAMBIADOR_IN': 'Cambiándose',
    'ESPERANDO_RESONADOR': 'Esperando turno',
    'RESONADOR': 'En resonador',
    'CAMBIADOR_OUT': 'Vistiéndose',
    'SALIDA': 'Saliendo',
    'COMPLETADO': 'Completado'
}

# ============================================================================
# LAYOUT DE LA CLÍNICA - EXACTO SEGÚN CROQUIS DE MIRO
# ============================================================================
# Layout basado en el diseño real con líneas rojas (estructura)
LAYOUT = {
    # Sala de espera (abajo izquierda)
    'sala_espera': {'x': 40, 'y': 450, 'ancho': 420, 'alto': 400},
    
    # Mesa de atención (dentro de sala de espera, arriba)
    'mesa_atencion': {'x': 100, 'y': 470, 'ancho': 300, 'alto': 100},
    
    # Pasillo vertical (centro)
    'pasillo_vertical': {'x': 480, 'y': 80, 'ancho': 140, 'alto': 770},
    
    # Pasillo horizontal superior
    'pasillo_horizontal': {'x': 480, 'y': 80, 'ancho': 700, 'alto': 140},
    
    # Box (arriba derecha, dentro del pasillo horizontal)
    'box': {'x': 850, 'y': 100, 'ancho': 120, 'alto': 100},
    
    # Vestuario (derecha centro)
    'vestuario': {'x': 640, 'y': 350, 'ancho': 280, 'alto': 220},
    
    # Sala de resonancia (derecha abajo)
    'sala_resonancia': {'x': 640, 'y': 590, 'ancho': 500, 'alto': 260},
    
    # Resonador (dentro de sala de resonancia)
    'resonador': {'x': 740, 'y': 660, 'ancho': 300, 'alto': 120}
}

# ============================================================================
# WAYPOINTS - RUTA EXACTA DEL PACIENTE (flechas azules del croquis)
# ============================================================================
WAYPOINTS = {
    # 1. Entrada por sala de espera
    'entrada': (250, 900),
    'sala_espera_centro': (250, 650),
    
    # 2. Mesa de atención
    'mesa': (250, 520),
    
    # 3. Sale de sala de espera hacia pasillo
    'salida_sala_espera': (460, 520),
    
    # 4. Pasillo vertical - sube
    'pasillo_bajo': (550, 520),
    'pasillo_medio': (550, 350),
    'pasillo_alto': (550, 150),
    
    # 5. Pasillo horizontal - va hacia box
    'pasillo_horizontal_inicio': (700, 150),
    'pasillo_horizontal_box': (910, 150),
    
    # 6. Box (opcional, depende del flujo)
    'box': (910, 150),
    
    # 7. Baja al vestuario
    'bajada_vestuario': (780, 150),
    'vestuario_entrada': (780, 460),
    
    # 8. Vestuario
    'vestuario': (780, 460),
    
    # 9. Baja a sala de resonancia
    'bajada_resonancia': (780, 570),
    'sala_resonancia_entrada': (890, 650),
    
    # 10. Resonador
    'resonador': (890, 720),
    
    # 11. Salida (vuelve a vestuario y sale)
    'vestuario_salida': (780, 460),
    'salida': (250, 900)
}

# ============================================================================
# CONFIGURACIÓN DE MOVIMIENTO SUAVE
# ============================================================================
VELOCIDAD_PACIENTE = 100  # Píxeles por segundo (movimiento suave)
INTERPOLACION_SUAVE = True  # Activar movimiento interpolado

# ============================================================================
# CONFIGURACIÓN DE SIMULACIÓN
# ============================================================================
VELOCIDAD_SIMULACION_MIN = 12  # Velocidad mínima: 12 min simulados por segundo (5 seg real = 1 min sim)
VELOCIDAD_SIMULACION_MAX = 480  # Velocidad máxima: 480 min simulados por segundo
VELOCIDAD_SIMULACION_DEFAULT = 30  # Velocidad por defecto
FPS = 60  # Frames por segundo de la visualización

# ============================================================================
# CONFIGURACIÓN DE RESUMEN FINAL
# ============================================================================
MOSTRAR_RESUMEN_FINAL = True  # Mostrar resumen al terminar el día
