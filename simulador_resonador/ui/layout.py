import tkinter as tk

class Layout:
    def __init__(self, root, simulation):
        self.simulation = simulation

        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(fill="both", expand=True)

        self.title = tk.Label(
            self.frame,
            text="Simulación de Pacientes – Resonador",
            font=("Arial", 18, "bold")
        )
        self.title.pack(pady=10)

        self.info = tk.Label(
            self.frame,
            text="",
            font=("Arial", 14),
            justify="left"
        )
        self.info.pack(pady=20)

        self.button = tk.Button(
            self.frame,
            text="Siguiente Evento",
            font=("Arial", 12),
            command=self.next_step
        )
        self.button.pack(pady=10)

        self.update_view()

    def next_step(self):
        self.simulation.advance()
        self.update_view()

    def update_view(self):
        state = self.simulation.get_state()
        text = (
            f"Paciente: {state['patient']}\n"
            f"Etapa: {state['stage']}\n"
            f"Estudio: {state['study']}\n"
            f"Tiempo acumulado: {state['time']} min"
        )
        self.info.config(text=text)

