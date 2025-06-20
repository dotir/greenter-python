#!/usr/bin/env python3
"""
Script de utilidad para ejecutar tests de Greenter Python
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(cmd, description):
    """Ejecutar comando y mostrar resultado."""
    print(f"\n🔧 {description}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def run_unit_tests():
    """Ejecutar tests unitarios."""
    return run_command("python -m pytest tests/unit/ -v", "Ejecutando tests unitarios")

def run_integration_tests():
    """Ejecutar tests de integración."""
    return run_command("python -m pytest tests/integration/ -v", "Ejecutando tests de integración")

def run_basic_test():
    """Ejecutar test básico."""
    return run_command("python tests/unit/test_basic.py", "Ejecutando test básico")

def run_xml_tests():
    """Ejecutar tests de XML."""
    return run_command("python tests/unit/test_xml_only.py", "Ejecutando test de generación XML")

def run_signature_test():
    """Ejecutar test de firma digital."""
    return run_command("python tests/integration/test_signature_complete.py", "Ejecutando test de firma digital")

def run_system_test():
    """Ejecutar test del sistema completo."""
    return run_command("python tests/integration/test_sistema_completo.py", "Ejecutando test del sistema completo")

def run_sunat_interactive():
    """Ejecutar test interactivo con SUNAT."""
    print("\n🌐 Test interactivo con SUNAT")
    print("=" * 50)
    print("⚠️  Este test requiere credenciales reales")
    print("🔒 Solo usa endpoints de homologación (seguro)")
    
    confirm = input("\n¿Continuar? (s/N): ").lower().strip()
    if confirm == 's':
        return run_command("python tests/sunat/test_sunat_real_final.py", "Ejecutando test SUNAT interactivo")
    else:
        print("❌ Test cancelado")
        return True

def run_all_safe():
    """Ejecutar todos los tests seguros (sin SUNAT)."""
    print("🧪 EJECUTANDO TODOS LOS TESTS SEGUROS")
    print("=" * 60)
    
    tests = [
        ("Test básico", run_basic_test),
        ("Tests unitarios", run_unit_tests),
        ("Tests de integración", run_integration_tests),
    ]
    
    results = []
    for name, test_func in tests:
        success = test_func()
        results.append((name, success))
    
    print("\n📊 RESUMEN DE RESULTADOS")
    print("=" * 30)
    for name, success in results:
        status = "✅ ÉXITO" if success else "❌ FALLO"
        print(f"{status}: {name}")
    
    all_passed = all(success for _, success in results)
    
    if all_passed:
        print("\n🎉 ¡TODOS LOS TESTS PASARON!")
        print("✨ Tu sistema está funcionando perfectamente")
    else:
        print("\n⚠️  ALGUNOS TESTS FALLARON")
        print("🔧 Revisar errores arriba")
    
    return all_passed

def show_help():
    """Mostrar ayuda."""
    print("""
🚀 GREENTER PYTHON - EJECUTOR DE TESTS

Uso: python run_tests.py [opción]

Opciones disponibles:
  basic           - Test básico del sistema
  unit           - Tests unitarios
  integration    - Tests de integración  
  xml            - Test de generación XML
  signature      - Test de firma digital
  system         - Test del sistema completo
  sunat          - Test interactivo con SUNAT (requiere credenciales)
  all            - Todos los tests seguros (sin SUNAT)
  help           - Mostrar esta ayuda

Ejemplos:
  python run_tests.py basic      # Test básico
  python run_tests.py all        # Todos los tests seguros
  python run_tests.py sunat      # Test con SUNAT (interactivo)

Notas:
  • Los tests 'sunat' requieren credenciales reales
  • Solo se usan endpoints de homologación (seguro)
  • Los archivos de salida se guardan en output/
""")

def main():
    """Función principal."""
    
    # Verificar que estamos en el directorio correcto
    if not os.path.exists("greenter"):
        print("❌ Error: Ejecutar desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Verificar entorno virtual
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Advertencia: No se detectó entorno virtual activo")
        print("   Recomendado: source .venv/bin/activate")
    
    # Parsear argumentos
    if len(sys.argv) < 2:
        show_help()
        return
    
    option = sys.argv[1].lower()
    
    # Mapeo de opciones
    options = {
        'basic': run_basic_test,
        'unit': run_unit_tests,
        'integration': run_integration_tests,
        'xml': run_xml_tests,
        'signature': run_signature_test,
        'system': run_system_test,
        'sunat': run_sunat_interactive,
        'all': run_all_safe,
        'help': show_help,
    }
    
    if option in options:
        if option == 'help':
            options[option]()
        else:
            print(f"🚀 GREENTER PYTHON - {option.upper()}")
            success = options[option]()
            sys.exit(0 if success else 1)
    else:
        print(f"❌ Opción desconocida: {option}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 