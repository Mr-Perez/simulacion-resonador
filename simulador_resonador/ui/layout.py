import tkinter as tk

class Layout:
    def __init__(self, root, simulation):
        self.simulation = simulation

        # ---------- CONTENEDOR PRINCIPAL ----------
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        # ---------- CANVAS ESPACIAL ----------
        self.canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=350,
            bg="white"
        )
        self.canvas.pack(pady=10)

        # ---------- PANEL DE REPORTE ----------
        self.report_frame = tk.Frame(self.main_frame, pady=10)
        self.report_frame.pack(fill="x")

        self.info = tk.Label(
            self.report_frame,
            text="",
            font=("Arial", 13),
            justify="left"
        )
        self.info.pack()

        self.button = tk.Button(
            self.report_frame,
            text="Siguiente Evento",
            font=("Arial", 12),
            command=self.next_step
        )
        self.button.pack(pady=5)

        # Dibujar layout fijo
        self.draw_layout()
        self.update_view()

    # ---------- LAYOUT ESPACIAL ----------
    def draw_layout(self):
        self.rooms = {
            "Sala de Espera": self.canvas.create_rectangle(50, 50, 250, 150),
            "Vestidor": self.canvas.create_rectangle(300, 50, 450, 150),
            "Resonador": self.canvas.create_rectangle(500, 50, 700, 150),
            "Salida": self.canvas.create_rectangle(300, 220, 450, 300)
        }

        for name, rect in self.rooms.items():
            x1, y1, x2, y2 = self.canvas.coords(rect)
            self.canvas.create_text(
                (x1 + x2) / 2,
                y1 - 10,
                text=name,
                font=("Arial", 10, "bold")
            )

        # Paciente (círculo)
        self.patient_icon = self.canvas.create_oval(
            0, 0, 20, 20, fill="blue"
        )

    # ---------- MOVIMIENTO DEL PACIENTE ----------
    def move_patient(self, stage):
        rect = self.rooms[stage]
        x1, y1, x2, y2 = self.canvas.coords(rect)

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        self.canvas.coords(
            self.patient_icon,
            cx - 10, cy - 10,
            cx + 10, cy + 10
        )

    # ---------- EVENTOS ----------
    def next_step(self):
        self.simulation.advance()
        self.update_view()

    def update_view(self):
        state = self.simulation.get_state()

        self.move_patient(state["stage"])

        text = (
            f"Paciente: {state['patient']}\n"
            f"Etapa: {state['stage']}\n"
            f"Estudio: {state['study']}\n"
            f"Tiempo acumulado: {state['time']} min"
        )
        self.info.config(text=text)
