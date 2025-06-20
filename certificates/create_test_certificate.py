#!/usr/bin/env python3
"""
Crear certificado de prueba para desarrollo.
"""

import sys
import os
from datetime import datetime, timedelta

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def create_test_certificate():
    """Crear certificado de prueba usando cryptography."""
    
    print("🔧 Creando certificado de prueba...")
    
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives.serialization import pkcs12
        import ipaddress
        
        print("✅ Biblioteca cryptography disponible")
        
        # Generar clave privada
        print("🔑 Generando clave privada RSA...")
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Crear certificado autofirmado
        print("📄 Creando certificado autofirmado...")
        
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "PE"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Lima"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Lima"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Empresa de Prueba S.A.C."),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "Desarrollo"),
            x509.NameAttribute(NameOID.COMMON_NAME, "Certificado de Prueba Greenter"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName("localhost"),
                x509.DNSName("*.localhost"),
                x509.IPAddress(ipaddress.IPv4Address("127.0.0.1")),
            ]),
            critical=False,
        ).add_extension(
            x509.BasicConstraints(ca=True, path_length=0),
            critical=True,
        ).add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=True,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        ).sign(private_key, hashes.SHA256())
        
        print("✅ Certificado generado")
        
        # Crear archivo PKCS12
        print("📦 Creando archivo PKCS12...")
        
        password = b"123456"
        cert_name = "Certificado de Prueba Greenter"
        
        pkcs12_data = pkcs12.serialize_key_and_certificates(
            name=cert_name.encode('utf-8'),
            key=private_key,
            cert=cert,
            cas=None,
            encryption_algorithm=serialization.BestAvailableEncryption(password)
        )
        
        # Guardar certificado
        cert_filename = "certificado_prueba.pfx"
        with open(cert_filename, "wb") as f:
            f.write(pkcs12_data)
        
        print(f"✅ Certificado guardado: {cert_filename}")
        print(f"📏 Tamaño: {len(pkcs12_data)} bytes")
        print(f"🔑 Contraseña: 123456")
        
        # Probar el certificado
        print("\n🧪 Probando certificado creado...")
        
        from greenter.signer.xml_signer import XmlSigner
        
        signer = XmlSigner()
        if signer.set_certificate(cert_filename, "123456"):
            print("✅ Certificado cargado exitosamente")
            
            # Probar firma
            test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<test>
    <message>Prueba de certificado autogenerado</message>
    <timestamp>2025-06-19</timestamp>
</test>"""
            
            signed_xml = signer.sign(test_xml)
            if signed_xml and len(signed_xml) > len(test_xml):
                print("✅ Firma digital funcionando")
                print(f"📏 XML original: {len(test_xml)} caracteres")
                print(f"📏 XML firmado: {len(signed_xml)} caracteres")
                
                # Guardar test
                with open("certificado_prueba_test.xml", "w", encoding="utf-8") as f:
                    f.write(signed_xml)
                print("💾 Test guardado: certificado_prueba_test.xml")
                
                return True
            else:
                print("❌ Error en la firma")
                return False
        else:
            print("❌ Error cargando certificado")
            return False
            
    except ImportError:
        print("❌ Biblioteca 'cryptography' no disponible")
        print("💡 Instalar con: pip install cryptography")
        return False
    except Exception as e:
        print(f"❌ Error creando certificado: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_certificate_info():
    """Mostrar información sobre certificados."""
    
    print("\n📋 INFORMACIÓN SOBRE CERTIFICADOS:")
    print("=" * 50)
    
    print("\n🔐 CERTIFICADO DE PRUEBA CREADO:")
    print("   📄 Archivo: certificado_prueba.pfx")
    print("   🔑 Contraseña: 123456")
    print("   ⏱️  Validez: 365 días")
    print("   🏢 Emisor: Empresa de Prueba S.A.C.")
    print("   🎯 Propósito: Desarrollo y pruebas")
    
    print("\n⚠️  IMPORTANTE:")
    print("   • Este certificado es SOLO para desarrollo")
    print("   • NO usar en producción")
    print("   • Para producción, usar certificado de entidad certificadora")
    print("   • SUNAT requiere certificados válidos para homologación/producción")
    
    print("\n📋 PRÓXIMOS PASOS:")
    print("   1. ✅ Certificado de prueba creado")
    print("   2. 🔄 Actualizar tests con nueva contraseña")
    print("   3. 🔄 Probar firma de facturas")
    print("   4. 🔄 Enviar a SUNAT (con certificado real)")


def main():
    """Función principal."""
    
    print("🚀 Creación de Certificado de Prueba")
    print("=" * 50)
    
    success = create_test_certificate()
    
    if success:
        show_certificate_info()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡CERTIFICADO DE PRUEBA CREADO!")
        print("✨ Sistema listo para desarrollo")
        print("\n📋 Archivos creados:")
        print("   📄 certificado_prueba.pfx (contraseña: 123456)")
        print("   📄 certificado_prueba_test.xml")
        print("\n🔄 Siguiente paso: Probar firma de facturas")
    else:
        print("❌ ERROR CREANDO CERTIFICADO")
        print("🔧 Revisar dependencias e intentar nuevamente")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 