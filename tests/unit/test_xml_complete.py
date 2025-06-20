#!/usr/bin/env python3
"""
Test completo de generación XML para verificar conformidad con SUNAT.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_complete_xml_generation():
    """Test completo de generación XML con todos los campos requeridos."""
    
    print("🧪 Test completo de generación XML...")
    
    try:
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.xml.builder import XmlBuilder
        
        # Crear dirección completa
        address = Address(
            ubigueo="150101",
            departamento="LIMA", 
            provincia="LIMA",
            distrito="LIMA",
            direccion="AV. EJEMPLO 123",
            urbanizacion="URB. EJEMPLO"
        )
        
        # Crear empresa completa
        company = Company(
            ruc="20000000001",
            razon_social="EMPRESA DE PRUEBA S.A.C.",
            nombre_comercial="EMPRESA DE PRUEBA S.A.C.",
            address=address
        )
        
        # Crear cliente completo
        client = Client(
            tipo_doc="1",  # DNI
            num_doc="12345678",
            rzn_social="CLIENTE DE PRUEBA"
        )
        
        # Crear detalle de venta
        detail = SaleDetail(
            cod_producto="P001",
            unidad="NIU",  # Unidad de medida
            cantidad=1.0,
            descripcion="Producto de ejemplo",
            mto_valor_unitario=100.00,
            mto_precio_unitario=118.00,
            mto_valor_venta=100.00,
            mto_base_igv=100.00,
            porcentaje_igv=18.0,
            igv=18.00,
            tip_afe_igv="10",  # Gravado - Operación Onerosa
            total_impuestos=18.00
        )
        
        # Crear leyenda
        legend = Legend(
            code="1000",
            value="CIENTO DIECIOCHO CON 00/100 SOLES"
        )
        
        # Crear factura completa
        invoice = Invoice(
            ubl_version="2.1",
            tipo_doc="01",  # Factura
            serie="F001",
            correlativo="00000001",
            fecha_emision=datetime(2025, 6, 19),
            tipo_moneda="PEN",
            company=company,
            client=client,
            details=[detail],
            legends=[legend],
            # Importes
            mto_oper_gravadas=100.00,
            mto_igv=18.00,
            total_impuestos=18.00,
            mto_imp_venta=118.00
        )
        
        print("📋 Datos de la factura:")
        print(f"   Serie: {invoice.serie}")
        print(f"   Correlativo: {invoice.correlativo}")
        print(f"   Fecha: {invoice.fecha_emision}")
        print(f"   RUC Emisor: {invoice.company.ruc}")
        print(f"   Cliente: {invoice.client.rzn_social}")
        print(f"   Total: {invoice.mto_imp_venta} {invoice.tipo_moneda}")
        
        # Verificar serialización con alias
        print("\n🔍 Verificando serialización...")
        invoice_dict = invoice.dict(by_alias=True)
        
        print(f"   fechaEmision: {invoice_dict.get('fechaEmision')}")
        print(f"   tipoDoc: {invoice_dict.get('tipoDoc')}")
        print(f"   tipoMoneda: {invoice_dict.get('tipoMoneda')}")
        print(f"   mtoOperGravadas: {invoice_dict.get('mtoOperGravadas')}")
        print(f"   mtoImpVenta: {invoice_dict.get('mtoImpVenta')}")
        
        # Generar XML
        print("\n🔧 Generando XML...")
        builder = XmlBuilder()
        xml_content = builder.build(invoice)
        
        if not xml_content:
            print("❌ Error: No se pudo generar XML")
            return False
        
        print(f"✅ XML generado exitosamente ({len(xml_content)} caracteres)")
        
        # Verificar contenido XML
        print("\n📄 Verificando contenido XML...")
        
        required_elements = [
            '<?xml version="1.0"',
            'F001-00000001',
            '2025-06-19',
            '20000000001',
            '12345678',
            'EMPRESA DE PRUEBA S.A.C.',
            'CLIENTE DE PRUEBA',
            '100.00',
            '118.00',
            'PEN'
        ]
        
        missing_elements = []
        for element in required_elements:
            if element not in xml_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"❌ Elementos faltantes en XML: {missing_elements}")
            return False
        
        print("✅ Todos los elementos requeridos están presentes")
        
        # Guardar XML
        filename = f"factura_completa_{invoice.get_name()}.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"💾 XML guardado como: {filename}")
        
        # Mostrar primeras líneas del XML
        print("\n📝 Primeras líneas del XML generado:")
        lines = xml_content.split('\n')[:15]
        for i, line in enumerate(lines, 1):
            print(f"   {i:2d}: {line}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    
    print("🚀 Test Completo de Generación XML - SUNAT")
    print("=" * 50)
    
    success = test_complete_xml_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡TEST EXITOSO!")
        print("✨ XML generado correctamente según estándares SUNAT")
        print("\n📋 Próximos pasos:")
        print("   1. Verificar XML con validador SUNAT")
        print("   2. Firmar digitalmente el XML")
        print("   3. Enviar a SUNAT para homologación")
    else:
        print("❌ TEST FALLIDO")
        print("🔧 Revisar errores en la generación XML")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 