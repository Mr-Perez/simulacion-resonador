import tkinter as tk
import time
import threading

# =========================
# CONFIGURACIÓN GENERAL
# =========================

SCALE_TIME = 1  # 1 segundo = 1 minuto
PATIENT_RADIUS = 10

# =========================
# POSICIONES (coordenadas)
# =========================

POS_WAITING = (100, 150)
POS_DESK = (200, 150)
POS_HALLWAY = (350, 150)
POS_CHANGING = (450, 100)
POS_BOX = (500, 100)
POS_RESONATOR = (450, 250)
POS_EXIT = (100, 250)

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
        steps = minutes * 10
        dx = (target[0] - self.x) / steps
        dy = (target[1] - self.y) / steps

        for _ in range(steps):
            self.canvas.move(self.obj, dx, dy)
            self.canvas.move(self.text, dx, dy)
            self.canvas.update()
            time.sleep(0.1 * SCALE_TIME)

        self.x, self.y = target

# =========================
# SIMULACIÓN
# =========================

def simulate():
    patient = Patient(canvas, 1)

    # Llegada
    patient.move_to(POS_DESK, 1)

    # Validación
    time.sleep(3 * SCALE_TIME)

    # Pasillo
    patient.move_to(POS_HALLWAY, 2)

    # Vestidor
    patient.move_to(POS_CHANGING, 2)

    # Box
    patient.move_to(POS_BOX, 4)

    # Resonador
    patient.move_to(POS_RESONATOR, 3)

    # Scan
    time.sleep(20 * SCALE_TIME)

    # Salida
    patient.move_to(POS_EXIT, 5)

# =========================
# INTERFAZ
# =========================

root = tk.Tk()
root.title("Simulación Resonador - Flujo del Paciente")

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
threading.Thread(target=simulate, daemon=True).start()

root.mainloop()
