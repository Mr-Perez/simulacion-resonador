import random
from datetime import timedelta

# ----------------------------
# CONFIGURACIÓN GENERAL
# ----------------------------

START_HOUR = 8          # 08:00 AM
TOTAL_MINUTES = 12 * 60 # 720 minutos

# Tipos de estudio y duración promedio del scan (en minutos)
STUDY_TYPES = {
    "Columna": 40,
    "Cerebro": 30,
    "Articulaciones": 25
}

# ----------------------------
# FUNCIONES AUXILIARES
# ----------------------------

def minutes_to_clock(minutes):
    """Convierte minutos desde las 08:00 a hora reloj"""
    time = timedelta(minutes=minutes)
    hours = START_HOUR + time.seconds // 3600
    mins = (time.seconds % 3600) // 60
    return f"{hours:02d}:{mins:02d}"

def random_validation_time():
    return random.uniform(3, 7)

def random_changing_time():
    return random.uniform(5, 12)

def random_exit_time():
    return random.uniform(2, 5)

def scan_time(study_type):
    base = STUDY_TYPES[study_type]
    return random.uniform(base * 0.9, base * 1.1)

# ----------------------------
# SIMULACIÓN
# ----------------------------

current_time = 0
patient_id = 1
results = []

while current_time < TOTAL_MINUTES:

    study = random.choice(list(STUDY_TYPES.keys()))

    arrival_time = current_time
    validation = random_validation_time()
    changing = random_changing_time()
    scan = scan_time(study)
    exit_time = random_exit_time()

    total_service_time = validation + changing + scan + exit_time

    end_time = arrival_time + total_service_time

    if end_time > TOTAL_MINUTES:
        break

    results.append({
        "Paciente": patient_id,
        "Estudio": study,
        "Llegada_min": round(arrival_time, 2),
        "Hora_llegada": minutes_to_clock(arrival_time),
        "Validacion": round(validation, 2),
        "Cambiador": round(changing, 2),
        "Scan": round(scan, 2),
        "Salida": round(exit_time, 2),
        "Total_servicio": round(total_service_time, 2)
    })

    current_time = end_time
    patient_id += 1

# ----------------------------
# RESULTADOS
# ----------------------------

print("\nSIMULACIÓN DIARIA DE RMN (08:00 - 20:00)\n")

for r in results:
    print(
        f"Paciente {r['Paciente']:02d} | "
        f"{r['Estudio']:15} | "
        f"Llegada: {r['Llegada_min']:6} min | "
        f"Hora: {r['Hora_llegada']} | "
        f"Valid: {r['Validacion']:5} | "
        f"Camb: {r['Cambiador']:5} | "
        f"Scan: {r['Scan']:5} | "
        f"Salida: {r['Salida']:4} | "
        f"Total: {r['Total_servicio']:6}"
    )

print("\n------------------------------------")
print(f"Total de pacientes atendidos: {len(results)}")
print(f"Hora de cierre del resonador: {minutes_to_clock(current_time)}")
input("\nPresioná ENTER para cerrar el programa...")
