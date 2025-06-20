#!/usr/bin/env python3
"""
Test rápido con la contraseña 'llerena' del certificado.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_password_llerena():
    """Probar certificado con contraseña 'llerena'."""
    
    print("🔑 Probando certificado con contraseña: 'llerena'")
    
    try:
        from greenter.signer.xml_signer import XmlSigner
        
        cert_file = "1071454788.pfx"
        password = "llerena"
        
        if not os.path.exists(cert_file):
            print(f"❌ Certificado no encontrado: {cert_file}")
            return False
        
        print(f"📄 Archivo: {cert_file} ({os.path.getsize(cert_file)} bytes)")
        
        signer = XmlSigner()
        
        print(f"🔐 Probando contraseña: '{password}'")
        
        if signer.set_certificate(cert_file, password):
            print("🎉 ¡CERTIFICADO CARGADO EXITOSAMENTE!")
            
            # Probar firma con XML simple
            test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<test>
    <message>Prueba de firma digital</message>
    <timestamp>2025-06-19</timestamp>
</test>"""
            
            print("🔧 Probando firma digital...")
            signed_xml = signer.sign(test_xml)
            
            if signed_xml and len(signed_xml) > len(test_xml):
                print("✅ ¡FIRMA DIGITAL FUNCIONANDO!")
                print(f"📏 XML original: {len(test_xml)} caracteres")
                print(f"📏 XML firmado: {len(signed_xml)} caracteres")
                print(f"📈 Incremento: {len(signed_xml) - len(test_xml)} caracteres")
                
                # Guardar resultado
                with open("test_firma_exitosa.xml", "w", encoding="utf-8") as f:
                    f.write(signed_xml)
                print("💾 Test guardado: test_firma_exitosa.xml")
                
                # Verificar elementos de firma
                if "<ds:Signature" in signed_xml:
                    print("✅ Elemento ds:Signature encontrado")
                if "<ds:SignatureValue>" in signed_xml:
                    print("✅ Valor de firma encontrado")
                if "<ds:X509Certificate>" in signed_xml:
                    print("✅ Certificado X509 incluido")
                
                return True
            else:
                print("❌ Error: Firma no funciona correctamente")
                return False
        else:
            print("❌ Error: No se pudo cargar el certificado")
            print("💡 Verificar que la contraseña sea correcta")
            return False
            
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Test Certificado con Contraseña 'llerena'")
    print("=" * 50)
    
    success = test_password_llerena()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡CERTIFICADO FUNCIONANDO!")
        print("✨ Firma digital operativa")
        print("\n📋 Próximos pasos:")
        print("   1. ✅ Certificado digital")
        print("   2. 🔄 Probar firma de facturas")
        print("   3. 🔄 Enviar a SUNAT")
    else:
        print("❌ CERTIFICADO NO FUNCIONA")
        print("🔧 Verificar contraseña y archivo")
    
    exit(0 if success else 1) 