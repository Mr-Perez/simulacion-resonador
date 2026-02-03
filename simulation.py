# ============================================================
# SIMULACIÓN DE RESONADOR MAGNÉTICO
# Agenda densa + demanda constante
# Bloque horario: 08:00 a 20:00 (720 minutos)
# ============================================================

import random

# -----------------------------
# PARÁMETROS GENERALES
# -----------------------------

INICIO_DIA = 0
FIN_DIA = 720  # 12 horas * 60 minutos

# Estudios simbólicos (duración estimada en minutos)
ESTUDIOS = {
    "cerebro": 30,
    "columna": 40,
    "abdomen": 45
}

# Distribución del tiempo de cambiador (min, moda, max)
CAMBIADOR_MIN = 5
CAMBIADOR_MODA = 10
CAMBIADOR_MAX = 20


# -----------------------------
# FUNCIONES AUXILIARES
# -----------------------------

def tiempo_cambiador():
    """
    Tiempo que tarda una persona en cambiarse.
    Independiente del tipo de estudio.
    """
    return random.triangular(
        CAMBIADOR_MIN,
        CAMBIADOR_MAX,
        CAMBIADOR_MODA
    )


def seleccionar_estudio():
    """
    Selecciona un estudio de forma aleatoria.
    Demanda constante.
    """
    return random.choice(list(ESTUDIOS.keys()))


# -----------------------------
# SIMULACIÓN PRINCIPAL
# -----------------------------

def simular_dia():
    reloj = INICIO_DIA
    resonador_libre = INICIO_DIA

    pacientes = []
    paciente_id = 1

    while True:
        estudio = seleccionar_estudio()
        duracion_estudio = ESTUDIOS[estudio]
        duracion_cambio = tiempo_cambiador()

        fin_cambio = reloj + duracion_cambio

        inicio_estudio = max(fin_cambio, resonador_libre)
        fin_estudio = inicio_estudio + duracion_estudio

        if fin_estudio > FIN_DIA:
            break

        pacientes.append({
            "paciente": paciente_id,
            "estudio": estudio,
            "cambio": round(duracion_cambio, 2),
            "inicio_estudio": round(inicio_estudio, 2),
            "fin_estudio": round(fin_estudio, 2)
        })

        resonador_libre = fin_estudio
        reloj = inicio_estudio
        paciente_id += 1

    return pacientes


# -----------------------------
# EJECUCIÓN
# -----------------------------

def main():
    pacientes = simular_dia()

    print("\nSIMULACIÓN COMPLETA DEL DÍA")
    print("-" * 40)

    for p in pacientes:
        print(
            f"Paciente {p['paciente']:>3} | "
            f"Estudio: {p['estudio']:<8} | "
            f"Cambio: {p['cambio']:>5} min | "
            f"Inicio: {p['inicio_estudio']:>6} | "
            f"Fin: {p['fin_estudio']:>6}"
        )

    print("\n----------------------------------------")
    print(f"Total de estudios realizados: {len(pacientes)}")
    print(f"Tiempo total utilizado del resonador: {round(pacientes[-1]['fin_estudio'], 2)} minutos")
    print("----------------------------------------")

    input("\nPresioná ENTER para cerrar el programa...")


if __name__ == "__main__":
    main()
