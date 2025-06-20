#!/usr/bin/env python3
"""
Test simplificado para generar XML de facturas sin enviar a SUNAT.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'greenter-python'))

def test_xml_generation():
    """Test de generación de XML de factura."""
    
    print("🚀 Test de generación XML")
    print("=" * 50)
    
    try:
        # Importar modelos
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.xml.builder import XmlBuilder
        
        print("📦 Modelos importados correctamente")
        
        # Configurar empresa
        company_address = Address(
            ubigueo="150101",
            departamento="LIMA",
            provincia="LIMA", 
            distrito="LIMA",
            direccion="AV. PRUEBA 123"
        )
        
        company = Company(
            ruc="20000000001",  # RUC de prueba
            razon_social="EMPRESA DE PRUEBA S.A.C.",
            nombre_comercial="EMPRESA PRUEBA",
            address=company_address
        )
        
        # Cliente
        client = Client(
            tipo_doc="1",  # DNI
            num_doc="12345678",
            rzn_social="CLIENTE DE PRUEBA"
        )
        
        # Detalle de la factura
        detail = SaleDetail(
            cod_producto="P001",
            unidad="NIU",
            cantidad=1.0,
            descripcion="Producto de prueba",
            mto_valor_unitario=100.0,
            mto_precio_unitario=118.0,
            mto_valor_venta=100.0,
            mto_base_igv=100.0,
            porcentaje_igv=18.0,
            igv=18.0,
            tip_afe_igv="10",
            total_impuestos=18.0
        )
        
        # Leyenda
        legend = Legend(
            code="1000",
            value="CIENTO DIECIOCHO CON 00/100 SOLES"
        )
        
        # Crear factura
        invoice = Invoice(
            serie="F001",
            correlativo="00000001",
            fecha_emision=datetime.now(),
            tipo_doc="01",  # Factura
            tipo_moneda="PEN",
            company=company,
            client=client,
            details=[detail],
            legends=[legend],
            # Totales
            mto_oper_gravadas=100.0,
            mto_oper_inafectas=0.0,
            mto_oper_exoneradas=0.0,
            mto_oper_exportacion=0.0,
            mto_oper_gratuitas=0.0,
            mto_igv_gratuitas=0.0,
            mto_igv=18.0,
            mto_base_ivap=0.0,
            mto_ivap=0.0,
            mto_base_isc=0.0,
            mto_isc=0.0,
            mto_base_oth=0.0,
            mto_otros_tributos=0.0,
            total_impuestos=18.0,
            valor_venta=100.0,
            sub_total=118.0,
            mto_imp_venta=118.0,
            # Otros campos requeridos
            sum_otros_cargos=0.0,
            rel_docs=[],
            forma_pago=None,
            tipo_operacion="0101",
            fec_vencimiento=None,
            sum_dscto_global=0.0,
            mto_descuentos=0.0,
            sum_otros_descuentos=0.0,
            mto_cargos=0.0,
            total_anticipos=0.0,
            guia_embebida=None
        )
        
        print("✅ Factura creada correctamente")
        print(f"📄 Factura: {invoice.get_name()}")
        print(f"💰 Total: S/ {invoice.mto_imp_venta}")
        
        # Generar XML
        print("\n📄 Generando XML de la factura...")
        builder = XmlBuilder()
        xml_content = builder.build(invoice)
        
        if xml_content:
            print("✅ XML generado correctamente")
            print(f"📏 Tamaño: {len(xml_content)} caracteres")
            
            # Guardar XML para revisión
            xml_filename = f"factura_{invoice.get_name()}.xml"
            with open(xml_filename, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            print(f"💾 XML guardado en: {xml_filename}")
            
            # Mostrar inicio del XML
            print("\n📋 Inicio del XML generado:")
            print("-" * 50)
            lines = xml_content.split('\n')[:10]
            for line in lines:
                print(line)
            print("...")
            print("-" * 50)
            
            return True
        else:
            print("❌ No se pudo generar XML")
            return False
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    
    print("🧪 Greenter Python - Test de generación XML")
    print("=" * 60)
    print("📋 Este test solo genera XML sin enviar a SUNAT")
    print("=" * 60)
    
    success = test_xml_generation()
    
    if success:
        print("\n🎉 ¡Test exitoso!")
        print("✨ XML generado correctamente")
        print("\n📋 Próximos pasos:")
        print("   1. Revisar el archivo XML generado")
        print("   2. Configurar certificado digital para firmar")
        print("   3. Configurar credenciales SUNAT")
        print("   4. Probar envío a SUNAT")
    else:
        print("\n❌ Test falló")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 