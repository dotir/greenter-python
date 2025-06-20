#!/usr/bin/env python3
"""
Test completo de firma de factura con certificado de prueba.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_complete_signature():
    """Test completo de firma de factura."""
    
    print("🚀 Test completo de firma de factura...")
    
    try:
        # Importar módulos necesarios
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.xml.builder import XmlBuilder
        from greenter.signer.xml_signer import XmlSigner
        
        print("✅ Módulos importados")
        
        # Crear datos de prueba
        print("🏗️  Creando datos de prueba...")
        
        address = Address(
            ubigueo="150101",
            departamento="LIMA",
            provincia="LIMA",
            distrito="LIMA",
            direccion="AV. EJEMPLO 123"
        )
        
        company = Company(
            ruc="20123456789",
            razon_social="EMPRESA DE PRUEBA S.A.C.",
            address=address,
            nombre_comercial="EMPRESA DE PRUEBA"
        )
        
        client = Client(
            tipo_doc="6",
            num_doc="20987654321",
            rzn_social="CLIENTE DE PRUEBA S.A.C."
        )
        
        detail = SaleDetail(
            cod_producto="P001",
            unidad="NIU",
            cantidad=2.0,
            descripcion="Producto de prueba para firma digital",
            mto_valor_unitario=50.0,
            mto_precio_unitario=59.0,
            mto_valor_venta=100.0,
            porcentaje_igv=18.0,
            igv=18.0,
            tipo_afectacion_igv="10",
            total_impuestos=18.0
        )
        
        legend = Legend(
            code="1000",
            value="CIENTO DIECIOCHO CON 00/100 SOLES"
        )
        
        invoice = Invoice(
            serie="F001",
            correlativo="00000001",
            fecha_emision=datetime.now(),
            tipo_moneda="PEN",
            company=company,
            client=client,
            details=[detail],
            legends=[legend],
            mto_oper_gravadas=100.0,
            mto_igv=18.0,
            valor_venta=100.0,
            sub_total=118.0,
            total=118.0
        )
        
        print("✅ Datos de prueba creados")
        
        # Generar XML sin firmar
        print("📄 Generando XML sin firmar...")
        builder = XmlBuilder()
        xml_content = builder.build(invoice)
        
        if not xml_content:
            print("❌ Error generando XML")
            return False
        
        print(f"✅ XML generado: {len(xml_content)} caracteres")
        
        # Guardar XML sin firmar
        with open("factura_sin_firmar.xml", "w", encoding="utf-8") as f:
            f.write(xml_content)
        print("💾 XML sin firmar guardado: factura_sin_firmar.xml")
        
        # Configurar firmador
        print("🔑 Configurando certificado de prueba...")
        signer = XmlSigner()
        signer.set_certificate("certificado_prueba.pfx", "123456")
        
        if not signer.certificate_content:
            print("❌ Error cargando certificado")
            return False
        
        print("✅ Certificado cargado")
        
        # Firmar XML
        print("✍️  Firmando XML...")
        signed_xml = signer.sign(xml_content)
        
        if not signed_xml:
            print("❌ Error firmando XML")
            return False
        
        print(f"✅ XML firmado: {len(signed_xml)} caracteres")
        print(f"📈 Incremento: {len(signed_xml) - len(xml_content)} caracteres")
        
        # Guardar XML firmado
        with open("factura_completa_F001-00000001.xml", "w", encoding="utf-8") as f:
            f.write(signed_xml)
        print("💾 XML firmado guardado: factura_completa_F001-00000001.xml")
        
        # Verificar contenido de la firma
        print("🔍 Verificando contenido de la firma...")
        
        if '<ds:Signature' in signed_xml:
            print("✅ Elemento Signature encontrado")
        else:
            print("❌ Elemento Signature no encontrado")
            return False
        
        if '<ds:SignedInfo>' in signed_xml:
            print("✅ SignedInfo encontrado")
        else:
            print("❌ SignedInfo no encontrado")
            return False
        
        if '<ds:SignatureValue>' in signed_xml:
            print("✅ SignatureValue encontrado")
        else:
            print("❌ SignatureValue no encontrado")
            return False
        
        if '<ds:KeyInfo>' in signed_xml:
            print("✅ KeyInfo encontrado")
        else:
            print("❌ KeyInfo no encontrado")
            return False
        
        print("✅ Estructura de firma verificada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en test de firma: {e}")
        import traceback
        traceback.print_exc()
        return False


def show_results():
    """Mostrar resultados del test."""
    
    print("\n📋 RESULTADOS DEL TEST:")
    print("=" * 50)
    
    files_created = []
    
    # Verificar archivos creados
    test_files = [
        ("certificado_prueba.pfx", "Certificado de prueba"),
        ("factura_sin_firmar.xml", "XML sin firmar"),
        ("factura_completa_F001-00000001.xml", "XML firmado completo")
    ]
    
    for filename, description in test_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {description}: {filename} ({size} bytes)")
            files_created.append(filename)
        else:
            print(f"❌ {description}: {filename} (no encontrado)")
    
    print(f"\n📊 RESUMEN:")
    print(f"   📄 Archivos creados: {len(files_created)}")
    print(f"   🔐 Certificado: certificado_prueba.pfx (contraseña: 123456)")
    print(f"   📝 XML sin firmar: factura_sin_firmar.xml")
    print(f"   ✍️  XML firmado: factura_completa_F001-00000001.xml")
    
    print(f"\n🎯 PRÓXIMOS PASOS:")
    print(f"   1. ✅ Certificado de prueba funcionando")
    print(f"   2. ✅ Generación XML completa")
    print(f"   3. ✅ Firma digital implementada")
    print(f"   4. 🔄 Probar envío a SUNAT (requiere certificado real)")
    print(f"   5. 🔄 Implementar validaciones adicionales")


def main():
    """Función principal."""
    
    print("🚀 Test Completo de Firma Digital")
    print("=" * 50)
    
    # Verificar que existe el certificado
    if not os.path.exists("certificado_prueba.pfx"):
        print("❌ Certificado de prueba no encontrado")
        print("💡 Ejecutar primero: python create_test_certificate.py")
        return 1
    
    success = test_complete_signature()
    
    if success:
        show_results()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡FIRMA DIGITAL COMPLETADA!")
        print("✨ Sistema de facturación electrónica funcionando")
        print("🔐 Certificado de prueba operativo")
    else:
        print("❌ ERROR EN FIRMA DIGITAL")
        print("🔧 Revisar configuración y dependencias")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 