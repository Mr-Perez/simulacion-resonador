import random
from datetime import timedelta

# -------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------
INICIO_JORNADA_MIN = 0            # 08:00
FIN_JORNADA_MIN = 12 * 60         # 20:00

TIPOS_ESTUDIO = {
    "Cerebro": (25, 35),
    "Columna": (35, 45),
    "Articulaciones": (20, 30)
}

def minutos_a_hora(minutos):
    base = timedelta(hours=8)
    hora = base + timedelta(minutes=minutos)
    return f"{hora.seconds//3600:02d}:{(hora.seconds//60)%60:02d}"

# -------------------------------
# SIMULACIÓN
# -------------------------------
print("\nSIMULACIÓN DIARIA DE RMN (08:00 - 20:00)\n")

tiempo_actual = 0
tiempo_acumulado = 0
paciente = 1

while tiempo_actual < FIN_JORNADA_MIN:
    tipo = random.choice(list(TIPOS_ESTUDIO.keys()))

    llegada = tiempo_actual
    hora_llegada = minutos_a_hora(llegada)

    validacion = round(random.uniform(3, 7), 2)
    cambiador = round(random.uniform(5, 12), 2)
    scan = round(random.uniform(*TIPOS_ESTUDIO[tipo]), 2)
    salida = round(random.uniform(2, 5), 2)

    total_servicio = round(validacion + cambiador + scan + salida, 2)

    # Acumulación real del sistema
    tiempo_acumulado += total_servicio
    hora_fin = minutos_a_hora(tiempo_acumulado)

    print(
        f"Paciente {paciente:02d} | {tipo:<15} | "
        f"Llegada: {llegada:.2f} min | Hora: {hora_llegada} | "
        f"Valid: {validacion:<4} | Camb: {cambiador:<4} | "
        f"Scan: {scan:<5} | Salida: {salida:<4} | "
        f"Total: {total_servicio:<5} | "
        f"Acum: {tiempo_acumulado:.2f} min | Fin: {hora_fin}"
    )

    tiempo_actual += random.uniform(35, 55)
    paciente += 1

print("\n-----------------------------------")
print(f"Total de pacientes atendidos: {paciente - 1}")
print(f"Hora real de cierre del resonador: {hora_fin}")
input("\nPresioná ENTER para cerrar el programa...")
