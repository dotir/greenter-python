#!/usr/bin/env python3
"""
Test para encontrar la contraseña correcta del certificado.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_certificate_passwords():
    """Probar diferentes contraseñas comunes para el certificado."""
    
    print("🔑 Probando contraseñas del certificado...")
    
    try:
        from greenter.signer.xml_signer import XmlSigner
        
        cert_file = "1071454788.pfx"
        
        if not os.path.exists(cert_file):
            print(f"❌ Certificado no encontrado: {cert_file}")
            return False
        
        print(f"📄 Certificado: {cert_file} ({os.path.getsize(cert_file)} bytes)")
        
        # Lista de contraseñas comunes
        common_passwords = [
            "",  # Sin contraseña
            "123456",
            "password",
            "123456789",
            "1071454788",  # El mismo RUC
            "admin",
            "12345",
            "qwerty",
            "abc123",
            "Password123",
            "sunat",
            "SUNAT",
            "certificado",
            "test",
            "demo"
        ]
        
        signer = XmlSigner()
        
        print(f"\n🔍 Probando {len(common_passwords)} contraseñas...")
        
        for i, password in enumerate(common_passwords, 1):
            try:
                print(f"   {i:2d}. Probando: '{password}'" + (" (vacía)" if password == "" else ""))
                
                if signer.set_certificate(cert_file, password):
                    print(f"🎉 ¡CONTRASEÑA ENCONTRADA!")
                    print(f"✅ Certificado cargado con contraseña: '{password}'")
                    
                    # Verificar que realmente funciona
                    test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<test>
    <message>Test de firma</message>
</test>"""
                    
                    signed_xml = signer.sign(test_xml)
                    if signed_xml and len(signed_xml) > len(test_xml):
                        print("✅ Firma digital funcionando correctamente")
                        print(f"📏 XML original: {len(test_xml)} caracteres")
                        print(f"📏 XML firmado: {len(signed_xml)} caracteres")
                        
                        # Guardar resultado
                        with open("certificado_test_firmado.xml", "w", encoding="utf-8") as f:
                            f.write(signed_xml)
                        print("💾 Test de firma guardado: certificado_test_firmado.xml")
                        
                        return password
                    else:
                        print("⚠️  Certificado cargado pero firma no funciona")
                
            except Exception as e:
                error_msg = str(e)
                if "Invalid password" in error_msg:
                    print(f"     ❌ Contraseña incorrecta")
                elif "PKCS12" in error_msg:
                    print(f"     ❌ Error PKCS12: {error_msg}")
                else:
                    print(f"     ❌ Error: {error_msg}")
        
        print("\n❌ No se encontró la contraseña correcta")
        print("\n💡 Opciones:")
        print("   1. Verificar que el archivo .pfx es válido")
        print("   2. Contactar al emisor del certificado")
        print("   3. Regenerar el certificado si es de prueba")
        print("   4. Usar un certificado diferente")
        
        return None
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return None


def show_certificate_info():
    """Mostrar información del certificado."""
    
    print("\n📋 INFORMACIÓN DEL CERTIFICADO:")
    print("=" * 50)
    
    cert_file = "1071454788.pfx"
    
    if os.path.exists(cert_file):
        size = os.path.getsize(cert_file)
        print(f"📄 Archivo: {cert_file}")
        print(f"📏 Tamaño: {size:,} bytes")
        
        # Información adicional si es posible
        try:
            from cryptography.hazmat.primitives import serialization
            
            with open(cert_file, 'rb') as f:
                cert_data = f.read()
            
            print(f"🔍 Formato: PKCS#12")
            print(f"📊 Datos binarios: {len(cert_data)} bytes")
            
        except ImportError:
            print("💡 Para más información, instalar: pip install cryptography")
        except Exception as e:
            print(f"⚠️  No se pudo analizar: {e}")
    else:
        print(f"❌ Certificado no encontrado: {cert_file}")
    
    print("\n🔑 SOBRE CERTIFICADOS DIGITALES:")
    print("   • Formato .pfx/.p12 contiene clave privada + certificado")
    print("   • Siempre están protegidos con contraseña")
    print("   • Contraseña es establecida al crear/exportar el certificado")
    print("   • Sin contraseña correcta, no se puede usar")


def main():
    """Función principal."""
    
    print("🚀 Test de Contraseña de Certificado Digital")
    print("=" * 60)
    
    password = test_certificate_passwords()
    
    if not password:
        show_certificate_info()
    
    print("\n" + "=" * 60)
    if password is not None:
        print("🎉 ¡CERTIFICADO CONFIGURADO EXITOSAMENTE!")
        print(f"🔑 Contraseña encontrada: '{password}'")
        print("\n📋 Próximos pasos:")
        print("   1. ✅ Certificado digital funcionando")
        print("   2. 🔄 Probar firma de facturas")
        print("   3. 🔄 Enviar a SUNAT")
        print("\n💡 Actualizar tests con la contraseña correcta")
    else:
        print("⚠️  CERTIFICADO REQUIERE CONFIGURACIÓN")
        print("🔧 Verificar certificado y contraseña")
        print("💡 El sistema funcionará sin firma (solo para pruebas)")
    
    return 0 if password is not None else 1


if __name__ == "__main__":
    exit(main()) 