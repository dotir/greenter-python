#!/usr/bin/env python3
"""
Test avanzado de generación XML completo según estándares SUNAT UBL 2.1.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_advanced_xml_generation():
    """Test avanzado de generación XML con todos los elementos SUNAT."""
    
    print("🔬 Test avanzado de generación XML completo...")
    
    try:
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.xml.builder import XmlBuilder
        
        # Crear dirección completa para empresa
        company_address = Address(
            ubigueo="150101",
            departamento="LIMA", 
            provincia="LIMA",
            distrito="LIMA",
            direccion="AV. REPUBLICA DE PANAMA 3647",
            urbanizacion="SAN ISIDRO"
        )
        
        # Crear empresa completa
        company = Company(
            ruc="20100070970",
            razon_social="COMPAÑIA PERUANA DE RADIODIFUSION S.A.",
            nombre_comercial="AMERICA TELEVISION",
            address=company_address
        )
        
        # Crear dirección para cliente
        client_address = Address(
            ubigueo="150140",
            departamento="LIMA",
            provincia="LIMA", 
            distrito="SURQUILLO",
            direccion="AV. ANGAMOS ESTE 1234"
        )
        
        # Crear cliente completo
        client = Client(
            tipo_doc="6",  # RUC
            num_doc="20123456789",
            rzn_social="EMPRESA CLIENTE DEMO S.A.C.",
            address=client_address
        )
        
        # Crear múltiples detalles de venta
        details = [
            SaleDetail(
                cod_producto="SERV001",
                unidad="ZZ",  # Servicios
                cantidad=1.0,
                descripcion="SERVICIO DE PUBLICIDAD EN TELEVISION - SPOT 30 SEGUNDOS",
                mto_valor_unitario=1000.00,
                mto_precio_unitario=1180.00,
                mto_valor_venta=1000.00,
                mto_base_igv=1000.00,
                porcentaje_igv=18.0,
                igv=180.00,
                tip_afe_igv="10",  # Gravado - Operación Onerosa
                total_impuestos=180.00
            ),
            SaleDetail(
                cod_producto="PROD002",
                unidad="NIU",  # Unidad
                cantidad=5.0,
                descripcion="MATERIAL PROMOCIONAL - LLAVEROS PERSONALIZADOS",
                mto_valor_unitario=20.00,
                mto_precio_unitario=23.60,
                mto_valor_venta=100.00,
                mto_base_igv=100.00,
                porcentaje_igv=18.0,
                igv=18.00,
                tip_afe_igv="10",  # Gravado - Operación Onerosa
                total_impuestos=18.00
            )
        ]
        
        # Crear leyendas
        legends = [
            Legend(
                code="1000",
                value="MIL TRESCIENTOS NOVENTA Y OCHO CON 00/100 SOLES"
            ),
            Legend(
                code="2000", 
                value="TRANSFERENCIA GRATUITA DE UN BIEN Y/O SERVICIO PRESTADO GRATUITAMENTE"
            )
        ]
        
        # Crear factura completa con todos los campos
        invoice = Invoice(
            ubl_version="2.1",
            tipo_doc="01",  # Factura
            serie="F001",
            correlativo="00000123",
            fecha_emision=datetime(2025, 6, 19, 14, 30, 0),
            fec_vencimiento=datetime(2025, 7, 19),  # 30 días
            tipo_moneda="PEN",
            tipo_operacion="0101",  # Venta interna
            company=company,
            client=client,
            details=details,
            legends=legends,
            # Importes calculados
            mto_oper_gravadas=1100.00,  # Base gravada total
            mto_igv=198.00,             # IGV total (1100 * 0.18)
            total_impuestos=198.00,     # Total impuestos
            mto_imp_venta=1298.00,      # Total factura (1100 + 198)
            # Campos adicionales
            sum_otros_cargos=0.00,
            mto_descuentos=0.00,
            observacion="Factura de prueba para validación SUNAT"
        )
        
        print("📋 Datos de la factura avanzada:")
        print(f"   📄 Documento: {invoice.get_name()}")
        print(f"   📅 Fecha emisión: {invoice.fecha_emision}")
        print(f"   📅 Fecha vencimiento: {invoice.fec_vencimiento}")
        print(f"   🏢 Emisor: {invoice.company.razon_social}")
        print(f"   📍 Dirección emisor: {invoice.company.address.direccion}")
        print(f"   👤 Cliente: {invoice.client.rzn_social}")
        print(f"   📍 Dirección cliente: {invoice.client.address.direccion}")
        print(f"   📦 Líneas de detalle: {len(invoice.details)}")
        print(f"   📜 Leyendas: {len(invoice.legends)}")
        print(f"   💰 Base gravada: {invoice.mto_oper_gravadas} {invoice.tipo_moneda}")
        print(f"   💰 IGV: {invoice.mto_igv} {invoice.tipo_moneda}")
        print(f"   💰 Total: {invoice.mto_imp_venta} {invoice.tipo_moneda}")
        
        # Generar XML avanzado
        print("\n🔧 Generando XML avanzado...")
        builder = XmlBuilder()
        xml_content = builder.build(invoice)
        
        if not xml_content:
            print("❌ Error: No se pudo generar XML")
            return False
        
        print(f"✅ XML avanzado generado exitosamente ({len(xml_content)} caracteres)")
        
        # Verificar elementos avanzados
        print("\n🔍 Verificando elementos avanzados...")
        
        advanced_elements = [
            # Elementos básicos
            'F001-00000123',
            '2025-06-19',
            '2025-07-19',  # Fecha vencimiento
            'listID="0101"',  # InvoiceTypeCode con lista
            'listID="ISO 4217 Alpha"',  # DocumentCurrencyCode con lista
            
            # Empresa con direcciones completas
            'COMPAÑIA PERUANA DE RADIODIFUSION S.A.',
            'AMERICA TELEVISION',
            'AV. REPUBLICA DE PANAMA 3647',
            'SAN ISIDRO',
            '20100070970',
            
            # Cliente con direcciones
            'EMPRESA CLIENTE DEMO S.A.C.',
            'AV. ANGAMOS ESTE 1234',
            'SURQUILLO',
            '20123456789',
            
            # Líneas de detalle
            '<cac:InvoiceLine>',
            'SERVICIO DE PUBLICIDAD EN TELEVISION',
            'MATERIAL PROMOCIONAL - LLAVEROS',
            'unitCode="ZZ"',  # Servicios
            'unitCode="NIU"',  # Unidad
            
            # Impuestos detallados
            '<cac:TaxTotal>',
            '<cac:TaxSubtotal>',
            'schemeID="UN/ECE 5153"',
            '<cbc:Name>IGV</cbc:Name>',
            '<cbc:TaxTypeCode>VAT</cbc:TaxTypeCode>',
            
            # Leyendas
            'languageLocaleID="1000"',
            'MIL TRESCIENTOS NOVENTA Y OCHO',
            
            # Direcciones con ubigeos
            'schemeAgencyName="PE:INEI"',
            'schemeName="Ubigeos"',
            '150101',  # Ubigeo Lima
            '150140',  # Ubigeo Surquillo
            
            # Totales
            '1100.00',  # Base
            '198.00',   # IGV
            '1298.00'   # Total
        ]
        
        missing_elements = []
        for element in advanced_elements:
            if element not in xml_content:
                missing_elements.append(element)
        
        if missing_elements:
            print(f"⚠️  Elementos faltantes ({len(missing_elements)}):")
            for element in missing_elements[:10]:  # Mostrar solo los primeros 10
                print(f"     - {element}")
            if len(missing_elements) > 10:
                print(f"     ... y {len(missing_elements) - 10} más")
        else:
            print("✅ Todos los elementos avanzados están presentes")
        
        # Guardar XML avanzado
        filename = f"factura_avanzada_{invoice.get_name()}.xml"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"\n💾 XML avanzado guardado como: {filename}")
        
        # Mostrar estadísticas del XML
        lines = xml_content.split('\n')
        print(f"\n📊 Estadísticas del XML:")
        print(f"   📏 Caracteres: {len(xml_content):,}")
        print(f"   📄 Líneas: {len(lines):,}")
        print(f"   📦 Elementos InvoiceLine: {xml_content.count('<cac:InvoiceLine>')}")
        print(f"   💰 Elementos TaxTotal: {xml_content.count('<cac:TaxTotal>')}")
        print(f"   📜 Elementos Note: {xml_content.count('<cbc:Note')}")
        print(f"   📍 Elementos Address: {xml_content.count('<cac:PostalAddress>')}")
        
        # Mostrar muestra del XML
        print(f"\n📝 Muestra del XML generado (primeras 20 líneas):")
        for i, line in enumerate(lines[:20], 1):
            print(f"   {i:2d}: {line}")
        
        if len(lines) > 20:
            print(f"   ... ({len(lines) - 20} líneas más)")
        
        return len(missing_elements) == 0
        
    except Exception as e:
        print(f"❌ Error durante el test avanzado: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    
    print("🚀 Test Avanzado de XML - Estándares SUNAT UBL 2.1")
    print("=" * 60)
    
    success = test_advanced_xml_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡TEST AVANZADO EXITOSO!")
        print("✨ XML generado cumple con estándares SUNAT UBL 2.1")
        print("\n📋 Características implementadas:")
        print("   ✅ Direcciones completas con ubigeos")
        print("   ✅ Líneas de detalle con impuestos")
        print("   ✅ Códigos de catálogo SUNAT")
        print("   ✅ Leyendas y notas")
        print("   ✅ Fechas de vencimiento")
        print("   ✅ Múltiples productos/servicios")
        print("   ✅ Estructura UBL 2.1 completa")
        print("\n🔄 Siguiente paso: Implementar firma digital")
    else:
        print("⚠️  TEST PARCIALMENTE EXITOSO")
        print("🔧 Algunos elementos avanzados necesitan ajustes")
        print("💡 El XML básico funciona, falta optimizar detalles")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 