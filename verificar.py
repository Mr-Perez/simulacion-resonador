"""
SCRIPT DE VERIFICACIÓN DEL SISTEMA
===================================
Verifica que todas las dependencias estén instaladas correctamente
"""

import sys

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("⚠️  ADVERTENCIA: Se recomienda Python 3.8 o superior")
        return False
    return True

def verificar_pygame():
    """Verifica que pygame esté instalado"""
    try:
        import pygame
        print(f"✅ Pygame {pygame.version.ver}")
        return True
    except ImportError:
        print("❌ Pygame NO está instalado")
        print("   Instala con: pip install pygame")
        return False

def verificar_numpy():
    """Verifica que numpy esté instalado"""
    try:
        import numpy
        print(f"✅ NumPy {numpy.__version__}")
        return True
    except ImportError:
        print("❌ NumPy NO está instalado")
        print("   Instala con: pip install numpy")
        return False

def verificar_archivos():
    """Verifica que todos los archivos del proyecto existan"""
    import os
    
    archivos_requeridos = [
        'config.py',
        'paciente.py',
        'simulacion.py',
        'visualizacion.py',
        'main.py',
        'requirements.txt',
        'README.md'
    ]
    
    todos_presentes = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo} - FALTA")
            todos_presentes = False
    
    return todos_presentes

def main():
    """Función principal de verificación"""
    print("=" * 60)
    print("VERIFICACIÓN DEL SISTEMA")
    print("=" * 60)
    print()
    
    print("📦 Verificando Python...")
    python_ok = verificar_python()
    print()
    
    print("📦 Verificando dependencias...")
    pygame_ok = verificar_pygame()
    numpy_ok = verificar_numpy()
    print()
    
    print("📁 Verificando archivos del proyecto...")
    archivos_ok = verificar_archivos()
    print()
    
    print("=" * 60)
    if python_ok and pygame_ok and numpy_ok and archivos_ok:
        print("✅ TODO LISTO - Puedes ejecutar: python main.py")
    else:
        print("⚠️  Hay problemas que debes resolver primero")
        print()
        print("Para instalar las dependencias:")
        print("  pip install -r requirements.txt")
    print("=" * 60)

if __name__ == "__main__":
    main()
