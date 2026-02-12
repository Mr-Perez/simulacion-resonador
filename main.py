"""
SIMULADOR DE RESONADOR V3.0 - GRILLA FLEXIBLE
==============================================
Sistema automático con llegadas realistas
"""

from simulacion import SimuladorResonador
from visualizacion import Visualizador

def main():
    print("=" * 70)
    print("SIMULADOR DE RESONADOR V3.0 - GRILLA FLEXIBLE")
    print("=" * 70)
    print()
    print("CARACTERÍSTICAS V3.0:")
    print("  ✓ GRILLA FLEXIBLE: Turnos cuando termina el anterior")
    print("  ✓ LLEGADAS REALISTAS: Escalonadas según probabilidades")
    print("  ✓ SIMULACIÓN AUTOMÁTICA: Sin ENTER, corre sola")
    print("  ✓ Core: Anticipa tiempo para dar turnos precisos")
    print()
    print("PROBABILIDADES:")
    print("  • Llegada temprano (-5 min): 20%")
    print("  • Llegada puntual (0 min): 30%")
    print("  • Llegada tarde (5-10 min): 50%")
    print()
    print("CONTROLES:")
    print("  - ESPACIO: Pausar/Reanudar")
    print("  - V: Velocidad x2")
    print("  - S: Ver resumen")
    print("  - R: Reiniciar")
    print("  - ESC: Salir")
    print()
    print("=" * 70)
    print()
    print("Iniciando simulación automática...")
    print()
    
    simulador = SimuladorResonador()
    visualizador = Visualizador(simulador)
    visualizador.ejecutar()

if __name__ == "__main__":
    main()
