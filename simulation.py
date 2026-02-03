import random

# =========================
# CONFIGURACIÓN GENERAL
# =========================

START_MINUTE = 0
END_MINUTE = 12 * 60  # 12 horas = 720 minutos

# Duraciones simbólicas por tipo de estudio (minutos)
STUDIES = {
    "Cerebro": 30,
    "Columna": 30,
    "Articulaciones": 25,
    "Cuerpo completo": 60,
    "Otros": 20
}

STUDY_PROBABILITIES = [
    ("Cerebro", 0.25),
    ("Columna", 0.25),
    ("Articulaciones", 0.33),
    ("Cuerpo completo", 0.02),
    ("Otros", 0.15)
]

# Cambiador (tiempo variable independiente del estudio)
CHANGING_TIME = {
    "min": 5,
    "mode": 10,
    "max": 20
}

# =========================
# FUNCIONES AUXILIARES
# =========================

def elegir_estudio():
    r = random.random()
    acumulado = 0
    for estudio, prob in STUDY_PROBABILITIES:
        acumulado += prob
        if r <= acumulado:
            return estudio
    return "Otros"


def tiempo_cambiador():
    return random.triangular(
        CHANGING_TIME["min"],
        CHANGING_TIME["max"],
        CHANGING_TIME["mode"]
    )

# =========================
# SIMULACIÓN
# =========================

def simular_dia():
    reloj = START_MINUTE
    resonador_libre = START_MINUTE
    pacientes = 0

    eventos = []

    while reloj < END_MINUTE:
        estudio = elegir_estudio()
        duracion_estudio = STUDIES[estudio]
        t_cambio = tiempo_cambiador()

        inicio_estudio = max(reloj + t_cambio, resonador_libre)
        fin_estudio = inicio_estudio + duracion_estudio

        if fin_estudio > END_MINUTE:
            break

        eventos.append({
            "paciente": pacientes + 1,
            "estudio": estudio,
            "cambio": round(t_cambio, 1),
            "inicio": round(inicio_estudio, 1),
            "fin": round(fin_estudio, 1)
        })

        resonador_libre = fin_estudio
        reloj = inicio_estudio
        pacientes += 1

    return eventos

# =========================
# EJECUCIÓN CONTROLADA
# =========================

if __name__ == "__main__":
    resultados = simular_dia()
    for e in resultados:
        print(e)

    print("\nPacientes atendidos:", len(resultados))
