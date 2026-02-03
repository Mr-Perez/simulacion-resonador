import random
from datetime import timedelta

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------
HORA_APERTURA = 8 * 60          # 08:00 en minutos
HORA_CIERRE = 20 * 60           # 20:00 en minutos
JORNADA = HORA_CIERRE - HORA_APERTURA

random.seed()

# -----------------------------
# DISTRIBUCIONES
# -----------------------------
def triangular(a, b, c):
    return round(random.triangular(a, b, c), 2)

# -----------------------------
# TIPOS DE ESTUDIO
# -----------------------------
ESTUDIOS = {
    "Cerebro": {
        "prob": 0.25,
        "scan": (18, 22, 25)
    },
    "Columna": {
        "prob": 0.25,
        "scan": (20, 25, 30)
    },
    "Articulaciones": {
        "prob": 0.33,
        "scan": (15, 18, 22)
    },
    "Cuerpo completo": {
        "prob": 0.02,
        "scan": (35, 40, 45)
    },
    "Otros": {
        "prob": 0.15,
        "scan": (20, 25, 30)
    }
}

def elegir_estudio():
    r = random.random()
    acumulado = 0
    for estudio, data in ESTUDIOS.items():
        acumulado += data["prob"]
        if r <= acumulado:
            return estudio
    return "Otros"

# -----------------------------
# SIMULACIÓN
# -----------------------------
def simular_dia():
    tiempo_actual = 0
    paciente_id = 1
    resultados = []

    while tiempo_actual < JORNADA:
        estudio = elegir_estudio()

        llegada = triangular(0, 10, 30)
        validacion = triangular(3, 5, 8)
        cambiador = triangular(5, 8, 15)
        scan = triangular(*ESTUDIOS[estudio]["scan"])
        salida = triangular(2, 3, 6)

        inicio_servicio = max(tiempo_actual, llegada)
        fin_servicio = inicio_servicio + validacion + cambiador + scan + salida

        if fin_servicio > JORNADA:
            break

        resultados.append({
            "Paciente": paciente_id,
            "Estudio": estudio,
            "Llegada": llegada,
            "Horario llegada": HORA_APERTURA + llegada,
            "Validación": validacion,
            "Cambiador": cambiador,
            "Scan": scan,
            "Salida": salida,
            "Tiempo total servicio": fin_servicio - llegada
        })

        tiempo_actual = fin_servicio
        paciente_id += 1

    return resultados

# -----------------------------
# EJECUCIÓN
# -----------------------------
print("\nSIMULACIÓN COMPLETA DEL DÍA\n")

datos = simular_dia()

for d in datos:
    print(
        f"Paciente {d['Paciente']:>2} | "
        f"{d['Estudio']:<15} | "
        f"Llegada: {d['Llegada']:>6} min | "
        f"Total servicio: {d['Tiempo total servicio']:>6} min"
    )

print(f"\nTotal de estudios realizados: {len(datos)}")

input("\nPresioná ENTER para cerrar el programa...")
