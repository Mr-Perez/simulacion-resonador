"""
SIMULADOR DE RESONADOR V2.1 - CONTROL MANUAL
=============================================
Versión corregida con flujo correcto y control manual
"""

from simulacion import SimuladorResonador
from visualizacion import Visualizador

def main():
    print("=" * 70)
    print("SIMULADOR DE RESONADOR V2.1 - CONTROL MANUAL")
    print("=" * 70)
    print()
    print("NOVEDADES V2.1:")
    print("  ✓ Control MANUAL: Presiona ENTER para cada paciente")
    print("  ✓ Flujo CORRECTO: Sala → Mesa → Pasillo → Vestuario → Box → Resonador")
    print("  ✓ Layout CORREGIDO: Box dentro del vestuario")
    print("  ✓ Métricas SIEMPRE visibles")
    print("  ✓ Resolución: 1280x960")
    print()
    print("CONTROLES:")
    print("  - ENTER: Iniciar siguiente paciente")
    print("  - ESPACIO: Pausar/Reanudar")
    print("  - ↑ ↓: Ajustar velocidad")
    print("  - R: Reiniciar")
    print("  - ESC: Salir")
    print()
    print("=" * 70)
    print()
    print("Iniciando simulación...")
    
    simulador = SimuladorResonador()
    visualizador = Visualizador(simulador)
    visualizador.ejecutar()

if __name__ == "__main__":
    main()
