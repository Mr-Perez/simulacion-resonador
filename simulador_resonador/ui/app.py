# simulador_resonador/ui/app.py
import tkinter as tk

class ResonadorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulación Resonador")
        self.geometry("900x600")

        self.label = tk.Label(
            self,
            text="Simulación de Resonador Magnético",
            font=("Arial", 18)
        )
        self.label.pack(pady=20)

