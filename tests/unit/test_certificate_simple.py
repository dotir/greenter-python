#!/usr/bin/env python3
"""
Test simple para verificar certificado de prueba.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_certificate_loading():
    """Test simple de carga de certificado."""
    
    print("🧪 Test de carga de certificado de prueba...")
    
    try:
        from greenter.signer.xml_signer import XmlSigner
        
        # Verificar que existe el certificado
        cert_file = "certificado_prueba.pfx"
        if not os.path.exists(cert_file):
            print(f"❌ Archivo {cert_file} no encontrado")
            return False
        
        print(f"✅ Archivo encontrado: {cert_file}")
        print(f"📏 Tamaño: {os.path.getsize(cert_file)} bytes")
        
        # Crear signer
        signer = XmlSigner()
        print("✅ XmlSigner creado")
        
        # Intentar cargar certificado
        print("🔑 Intentando cargar certificado con contraseña '123456'...")
        
        try:
            result = signer.set_certificate(cert_file, "123456")
            print(f"📋 Resultado set_certificate: {result}")
            
            # Verificar propiedades del signer
            print(f"📄 certificate_path: {signer.certificate_path}")
            print(f"🔑 private_key_path: {signer.private_key_path}")
            print(f"📝 certificate_content (primeros 100 chars): {signer.certificate_content[:100] if signer.certificate_content else 'None'}")
            
            if signer.certificate_content:
                print("✅ Certificado cargado exitosamente")
                return True
            else:
                print("❌ Certificado no se cargó correctamente")
                return False
                
        except Exception as e:
            print(f"❌ Error cargando certificado: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_pkcs12_direct():
    """Test directo de carga PKCS12."""
    
    print("\n🔧 Test directo de PKCS12...")
    
    try:
        from cryptography.hazmat.primitives.serialization import pkcs12
        
        cert_file = "certificado_prueba.pfx"
        password = "123456"
        
        # Leer archivo
        with open(cert_file, 'rb') as f:
            pkcs12_data = f.read()
        
        print(f"📏 Datos PKCS12: {len(pkcs12_data)} bytes")
        
        # Intentar cargar
        private_key, certificate, additional_certificates = pkcs12.load_key_and_certificates(
            pkcs12_data, 
            password.encode('utf-8')
        )
        
        print("✅ PKCS12 cargado exitosamente")
        print(f"🔑 Private key: {type(private_key)}")
        print(f"📄 Certificate: {type(certificate)}")
        print(f"📋 Additional certs: {len(additional_certificates) if additional_certificates else 0}")
        
        # Obtener información del certificado
        subject = certificate.subject
        issuer = certificate.issuer
        
        print(f"📝 Subject: {subject}")
        print(f"📝 Issuer: {issuer}")
        print(f"📅 Valid from: {certificate.not_valid_before}")
        print(f"📅 Valid until: {certificate.not_valid_after}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test PKCS12: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    
    print("🚀 Test de Certificado de Prueba")
    print("=" * 50)
    
    success1 = test_pkcs12_direct()
    success2 = test_certificate_loading()
    
    print("\n" + "=" * 50)
    if success1 and success2:
        print("🎉 ¡CERTIFICADO FUNCIONANDO!")
    elif success1:
        print("⚠️  PKCS12 OK, pero error en XmlSigner")
        print("🔧 Revisar implementación de set_certificate")
    else:
        print("❌ ERROR EN CERTIFICADO")
    
    return 0 if (success1 and success2) else 1


if __name__ == "__main__":
    exit(main()) 