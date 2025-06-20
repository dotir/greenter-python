#!/usr/bin/env python3
"""
Test rápido con la contraseña 'llerena1'.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

print("🔑 Probando certificado con contraseña: 'llerena1'")

try:
    from greenter.signer.xml_signer import XmlSigner
    
    cert_file = "1071454788.pfx"
    password = "llerena1"
    
    print(f"📄 Archivo: {cert_file} ({os.path.getsize(cert_file)} bytes)")
    
    signer = XmlSigner()
    
    if signer.set_certificate(cert_file, password):
        print("🎉 ¡CERTIFICADO CARGADO EXITOSAMENTE!")
        
        # Probar firma
        test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<test>
    <message>Prueba de firma con llerena1</message>
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
            with open("test_llerena1_firmado.xml", "w", encoding="utf-8") as f:
                f.write(signed_xml)
            print("💾 Test guardado: test_llerena1_firmado.xml")
            
            # Verificar elementos de firma
            if "<ds:Signature" in signed_xml:
                print("✅ Elemento ds:Signature encontrado")
            if "<ds:SignatureValue>" in signed_xml:
                print("✅ Valor de firma encontrado")
            if "<ds:X509Certificate>" in signed_xml:
                print("✅ Certificado X509 incluido")
            
            print("\n🎉 ¡CONTRASEÑA CORRECTA ENCONTRADA!")
            print("🔑 Contraseña del certificado: 'llerena1'")
            
        else:
            print("❌ Error: Firma no funciona correctamente")
    else:
        print("❌ Error: No se pudo cargar el certificado con 'llerena1'")
        
except Exception as e:
    print(f"❌ Error durante el test: {e}")
    import traceback
    traceback.print_exc() 