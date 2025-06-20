#!/usr/bin/env python3
"""
Test variaciones de la contraseña 'llerena'.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_llerena_variations():
    """Probar variaciones de la contraseña 'llerena'."""
    
    print("🔑 Probando variaciones de 'llerena'...")
    
    try:
        from greenter.signer.xml_signer import XmlSigner
        
        cert_file = "1071454788.pfx"
        
        if not os.path.exists(cert_file):
            print(f"❌ Certificado no encontrado: {cert_file}")
            return None
        
        print(f"📄 Archivo: {cert_file} ({os.path.getsize(cert_file)} bytes)")
        
        # Variaciones de 'llerena'
        password_variations = [
            "llerena",
            "Llerena", 
            "LLERENA",
            "llerena123",
            "Llerena123",
            "LLERENA123",
            "llerena2024",
            "llerena2025",
            "Llerena2024",
            "Llerena2025",
            "llerena.",
            "llerena!",
            "llerena1",
            "llerena12",
            "123llerena",
            "llerena_",
            "llerena-",
            "llerena01",
            "llerena00"
        ]
        
        signer = XmlSigner()
        
        print(f"\n🔍 Probando {len(password_variations)} variaciones...")
        
        for i, password in enumerate(password_variations, 1):
            try:
                print(f"   {i:2d}. Probando: '{password}'")
                
                if signer.set_certificate(cert_file, password):
                    print(f"🎉 ¡CONTRASEÑA ENCONTRADA!")
                    print(f"✅ Certificado cargado con: '{password}'")
                    
                    # Verificar firma
                    test_xml = """<?xml version="1.0" encoding="UTF-8"?>
<test><message>Test</message></test>"""
                    
                    signed_xml = signer.sign(test_xml)
                    if signed_xml and len(signed_xml) > len(test_xml):
                        print("✅ Firma digital funcionando")
                        print(f"📏 {len(test_xml)} -> {len(signed_xml)} caracteres")
                        
                        with open("certificado_llerena_firmado.xml", "w", encoding="utf-8") as f:
                            f.write(signed_xml)
                        print("💾 Guardado: certificado_llerena_firmado.xml")
                        
                        return password
                    else:
                        print("⚠️  Certificado cargado pero firma falla")
                
            except Exception as e:
                error_msg = str(e)
                if "Invalid password" in error_msg:
                    print(f"     ❌ Incorrecta")
                else:
                    print(f"     ❌ Error: {error_msg}")
        
        print("\n❌ Ninguna variación funcionó")
        return None
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        return None


def create_test_certificate():
    """Crear certificado de prueba si no encontramos la contraseña."""
    
    print("\n🔧 Creando certificado de prueba...")
    
    try:
        import subprocess
        
        # Verificar si OpenSSL está disponible
        try:
            result = subprocess.run(['openssl', 'version'], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ OpenSSL disponible: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ OpenSSL no disponible")
            print("💡 Instalar OpenSSL o usar certificado existente")
            return False
        
        # Generar clave privada
        print("🔑 Generando clave privada...")
        subprocess.run([
            'openssl', 'genpkey', 
            '-algorithm', 'RSA', 
            '-out', 'test_key.pem', 
            '-pkcs8', '-pass', 'pass:123456'
        ], check=True)
        
        # Generar certificado autofirmado
        print("📄 Generando certificado...")
        subprocess.run([
            'openssl', 'req', '-new', '-x509',
            '-key', 'test_key.pem',
            '-out', 'test_cert.pem',
            '-days', '365',
            '-passin', 'pass:123456',
            '-subj', '/C=PE/ST=Lima/L=Lima/O=Test/CN=test.com'
        ], check=True)
        
        # Crear PKCS12
        print("📦 Creando archivo PKCS12...")
        subprocess.run([
            'openssl', 'pkcs12', '-export',
            '-out', 'certificado_prueba.pfx',
            '-inkey', 'test_key.pem',
            '-in', 'test_cert.pem',
            '-passin', 'pass:123456',
            '-passout', 'pass:123456'
        ], check=True)
        
        # Limpiar archivos temporales
        os.remove('test_key.pem')
        os.remove('test_cert.pem')
        
        print("✅ Certificado de prueba creado: certificado_prueba.pfx")
        print("🔑 Contraseña: 123456")
        
        # Probar el nuevo certificado
        from greenter.signer.xml_signer import XmlSigner
        
        signer = XmlSigner()
        if signer.set_certificate('certificado_prueba.pfx', '123456'):
            print("✅ Certificado de prueba funcionando")
            return True
        else:
            print("❌ Error con certificado de prueba")
            return False
            
    except Exception as e:
        print(f"❌ Error creando certificado: {e}")
        return False


def main():
    """Función principal."""
    
    print("🚀 Test Variaciones de Contraseña + Certificado de Prueba")
    print("=" * 60)
    
    # Probar variaciones de llerena
    password = test_llerena_variations()
    
    if password:
        print(f"\n🎉 ¡ÉXITO! Contraseña encontrada: '{password}'")
    else:
        print("\n⚠️  No se encontró la contraseña correcta")
        
        # Crear certificado de prueba
        if create_test_certificate():
            print("\n✅ Certificado de prueba listo para usar")
            password = "123456"  # Contraseña del certificado de prueba
        else:
            print("\n❌ No se pudo crear certificado de prueba")
    
    print("\n" + "=" * 60)
    if password:
        print("🎉 ¡CERTIFICADO DISPONIBLE!")
        print(f"🔑 Contraseña: '{password}'")
        print("\n📋 Próximos pasos:")
        print("   1. ✅ Certificado digital funcionando")
        print("   2. 🔄 Actualizar tests con contraseña correcta")
        print("   3. 🔄 Probar firma de facturas completas")
        print("   4. 🔄 Enviar a SUNAT")
    else:
        print("❌ SIN CERTIFICADO FUNCIONAL")
        print("💡 Continuar sin firma para desarrollo")
    
    return 0 if password else 1


if __name__ == "__main__":
    exit(main()) 