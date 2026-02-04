# simulador_resonador/main.py
from ui.app import ResonadorApp

def main():
    app = ResonadorApp()
    app.mainloop()   # 🔥 esto mantiene viva la ventana

if __name__ == "__main__":
    main()

