#!/usr/bin/env python3
"""
Test de envío de facturas a SUNAT.
"""

import sys
import os
from datetime import datetime
from decimal import Decimal

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'greenter-python'))

def test_sunat_send():
    """Test de envío de factura a SUNAT."""
    
    print("🚀 Test de envío a SUNAT")
    print("=" * 50)
    
    try:
        # Importar modelos
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.see import See
        from greenter.ws.soap_client import SoapClient
        
        print("📦 Modelos importados correctamente")
        
        # Configurar empresa (datos de prueba)
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
        
        # Configurar SEE para ambiente de pruebas
        see = See()
        
        # Configurar certificado (necesitas proporcionar la ruta)
        cert_path = input("\n🔐 Ingresa la ruta del certificado .pfx/.p12 (o presiona Enter para omitir): ").strip()
        
        if cert_path and os.path.exists(cert_path):
            cert_password = input("🔑 Ingresa la contraseña del certificado: ").strip()
            
            # Configurar credenciales SUNAT
            sol_user = input("👤 Usuario SOL (formato: RUCUSUARIO): ").strip()
            sol_password = input("🔒 Contraseña SOL: ").strip()
            
            if sol_user and sol_password:
                print("\n🔄 Configurando conexión a SUNAT...")
                
                # Configurar SEE
                see.set_certificate(cert_path, cert_password)
                see.set_credentials(sol_user, sol_password)
                see.set_service("https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService")  # Ambiente BETA
                
                print("📡 Enviando factura a SUNAT...")
                
                # Enviar factura
                result = see.send(invoice)
                
                if result.is_success():
                    print("🎉 ¡Factura enviada exitosamente!")
                    print(f"📋 CDR: {result.get_cdr_response()}")
                    print(f"✅ Código: {result.get_code()}")
                    print(f"📝 Descripción: {result.get_description()}")
                else:
                    print("❌ Error al enviar factura:")
                    print(f"🔴 Error: {result.get_error()}")
                    print(f"📋 Código: {result.get_code()}")
                    
            else:
                print("⚠️ Credenciales SOL no proporcionadas")
        else:
            print("⚠️ Certificado no encontrado o no proporcionado")
            print("📋 Para enviar a SUNAT necesitas:")
            print("   1. Certificado digital (.pfx/.p12)")
            print("   2. Usuario y contraseña SOL")
            print("   3. RUC de la empresa")
        
        # Mostrar XML generado
        print("\n📄 Generando XML de la factura...")
        from greenter.xml.builder import XmlBuilder
        
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
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    
    print("🧪 Greenter Python - Test de envío a SUNAT")
    print("=" * 60)
    print("⚠️  IMPORTANTE: Este test usa el ambiente BETA de SUNAT")
    print("📋 Necesitas tener:")
    print("   • Certificado digital (.pfx/.p12)")
    print("   • Usuario SOL de pruebas")
    print("   • Contraseña SOL de pruebas")
    print("=" * 60)
    
    continuar = input("\n¿Deseas continuar? (s/n): ").strip().lower()
    
    if continuar in ['s', 'si', 'yes', 'y']:
        success = test_sunat_send()
        
        if success:
            print("\n🎉 Test completado")
        else:
            print("\n❌ Test falló")
    else:
        print("👋 Test cancelado")
    
    return 0


if __name__ == "__main__":
    exit(main()) 