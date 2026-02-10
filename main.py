"""
Script para mostrar la estructura de archivos del proyecto
"""

import os

def mostrar_arbol():
    """Muestra el árbol de archivos del proyecto"""
    
    print("=" * 70)
    print("ESTRUCTURA DE ARCHIVOS - SIMULACIÓN RESONADOR V2.0")
    print("=" * 70)
    print()
    
    archivos = {
        'Archivos principales (Python)': [
            'main.py                  ⭐ EJECUTA ESTE',
            'config.py                Configuración',
            'paciente.py              Clase Paciente',
            'simulacion.py            Motor de simulación',
            'visualizacion.py         Interfaz gráfica V2.0',
            'visualizacion_old.py     Backup V1.0',
            'generar_resumen_pdf.py   Genera PDF',
            'verificar.py             Verifica instalación'
        ],
        'Configuración': [
            'requirements.txt         Dependencias',
            '.gitignore               Archivos ignorados por Git'
        ],
        'Documentación': [
            'README.md                ⭐ Documentación principal',
            'GUIA_RAPIDA.md           ⭐ Guía de uso rápido',
            'GUIA_GITHUB.md           Tutorial de GitHub',
            'CHANGELOG.md             Historial de versiones',
            'ESTRUCTURA_ARCHIVOS.md   Este documento',
            'COMO_AGREGAR_ARCHIVOS.md Guía para agregar archivos'
        ],
        'Generados': [
            'Resumen_Ejecutivo_Simulacion_Resonador.pdf'
        ]
    }
    
    total = 0
    
    for categoria, lista in archivos.items():
        print(f"\n📁 {categoria}")
        print("-" * 70)
        for archivo in lista:
            print(f"   {archivo}")
            total += 1
    
    print()
    print("=" * 70)
    print(f"TOTAL: {total} archivos")
    print("=" * 70)
    print()
    print("💡 Para ver detalles de cada archivo: lee ESTRUCTURA_ARCHIVOS.md")
    print()

if __name__ == "__main__":
    mostrar_arbol()
