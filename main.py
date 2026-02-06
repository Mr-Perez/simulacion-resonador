"""
SIMULADOR DE RESONADOR - CLÍNICA
=================================
Programa principal de la simulación

Autor: Sistema de Simulación
Fecha: 2026
"""

from simulacion import SimuladorResonador
from visualizacion import Visualizador
import config

def main():
    """Función principal del programa"""
    
    print("=" * 60)
    print("SIMULADOR DE RESONADOR - CLÍNICA")
    print("=" * 60)
    print()
    
    # Crear el simulador
    print("📊 Inicializando simulador...")
    simulador = SimuladorResonador()
    
    # Generar turnos del día
    print("📅 Generando turnos del día...")
    simulador.generar_turnos()
    
    # Crear y ejecutar la visualización
    print("🎨 Iniciando visualización...")
    print()
    print("CONTROLES:")
    print("  - ESPACIO: Pausar/Reanudar")
    print("  - ↑ ↓: Ajustar velocidad de simulación")
    print("  - R: Reiniciar simulación")
    print("  - ESC: Salir")
    print()
    print("=" * 60)
    
    visualizador = Visualizador(simulador)
    visualizador.ejecutar()

if __name__ == "__main__":
    main()
