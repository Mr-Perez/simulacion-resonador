import tkinter as tk
import threading
import time
import random
import numpy as np

# =========================
# CONFIGURACIÓN GENERAL
# =========================

SCALE_TIME = 1        # 1 segundo = 1 minuto
DAY_MINUTES = 12 * 60
PATIENT_RADIUS = 10

# =========================
# POSICIONES
# =========================

POS_WAITING = (100, 150)
POS_DESK = (200, 150)
POS_HALLWAY = (350, 150)
POS_CHANGING = (450, 100)
POS_BOX = (500, 100)
POS_RESONATOR = (450, 250)
POS_EXIT = (100, 250)

# =========================
# ESTADÍSTICA
# =========================

STUDIES = [
    ("Cerebro", 0.25, 25, 4),
    ("Columna", 0.25, 30, 5),
    ("Articulaciones", 0.33, 20, 3),
    ("Cuerpo Completo", 0.02, 28, 4),
    ("Otros", 0.15, 22, 3),
]

def truncated_normal(mu, sigma):
    return max(1, np.random.normal(mu, sigma))

def sample_study():
    r = random.random()
    acc = 0
    for name, p, mu, sigma in STUDIES:
        acc += p
        if r <= acc:
            return name, truncated_normal(mu, sigma)

# =========================
# CLASE PACIENTE
# =========================

class Patient:
    def __init__(self, canvas, pid):
        self.canvas = canvas
        self.pid = pid
        self.x, self.y = POS_WAITING
        self.obj = canvas.create_oval(
            self.x - PATIENT_RADIUS,
            self.y - PATIENT_RADIUS,
            self.x + PATIENT_RADIUS,
            self.y + PATIENT_RADIUS,
            fill="blue"
        )
        self.text = canvas.create_text(self.x, self.y, text=str(pid), fill="white")

    def move_to(self, target, minutes):
        steps = int(minutes * 10)
        dx = (target[0] - self.x) / steps
        dy = (target[1] - self.y) / steps

        for _ in range(steps):
            self.canvas.move(self.obj, dx, dy)
            self.canvas.move(self.text, dx, dy)
            self.canvas.update()
            time.sleep(0.1 * SCALE_TIME)

        self.x, self.y = target

# =========================
# SIMULACIÓN PRINCIPAL
# =========================

resonator_lock = threading.Lock()
current_time = 0

def patient_process(pid):
    global current_time

    patient = Patient(canvas, pid)

    # Llegada y validación
    patient.move_to(POS_DESK, 1)
    time.sleep(truncated_normal(5, 1) * SCALE_TIME)

    # Pasillo → Vestidor → Box
    patient.move_to(POS_HALLWAY, 2)
    patient.move_to(POS_CHANGING, 2)
    patient.move_to(POS_BOX, truncated_normal(6, 1.5))

    # Espera resonador
    with resonator_lock:
        patient.move_to(POS_RESONATOR, 2)

        study, scan_time = sample_study()
        time.sleep(scan_time * SCALE_TIME)

    # Salida
    patient.move_to(POS_EXIT, truncated_normal(4, 1))

def simulate_day():
    pid = 1
    start_time = time.time()

    while (time.time() - start_time) / SCALE_TIME < DAY_MINUTES:
        threading.Thread(target=patient_process, args=(pid,), daemon=True).start()
        pid += 1
        time.sleep(1 * SCALE_TIME)  # agenda densa

# =========================
# INTERFAZ
# =========================

root = tk.Tk()
root.title("Simulación Resonador - Estadística + Flujo")

canvas = tk.Canvas(root, width=700, height=400, bg="white")
canvas.pack()

# Sala de espera
canvas.create_rectangle(50, 100, 300, 200, outline="black", width=2)
canvas.create_text(175, 90, text="Sala de Espera")

# Sillas
for i in range(3):
    canvas.create_rectangle(70 + i*40, 160, 100 + i*40, 190, fill="gray")

# Mesa atención
canvas.create_rectangle(180, 120, 260, 150, fill="tan")
canvas.create_text(220, 110, text="Mesa")

# Pasillo
canvas.create_rectangle(300, 80, 400, 320, fill="#eeeeee")
canvas.create_text(350, 60, text="Pasillo")

# Vestidor
canvas.create_rectangle(400, 50, 550, 180, outline="black", width=2)
canvas.create_text(475, 40, text="Vestidor")

# Box
canvas.create_rectangle(470, 80, 530, 140, fill="#cccccc")
canvas.create_text(500, 150, text="Box")

# Resonador
canvas.create_rectangle(400, 200, 650, 350, outline="black", width=2)
canvas.create_text(525, 190, text="Resonador")

# Lanzar simulación
threading.Thread(target=simulate_day, daemon=True).start()

root.mainloop()
