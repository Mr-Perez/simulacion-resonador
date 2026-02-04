import tkinter as tk
from ui.layout import Layout
from simulation.engine import SimulationEngine

def main():
    root = tk.Tk()
    root.title("Simulación Resonador")
    root.geometry("900x600")

    simulation = SimulationEngine()
    layout = Layout(root, simulation)

    root.mainloop()

if __name__ == "__main__":
    main()
