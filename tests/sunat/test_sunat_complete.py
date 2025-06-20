#!/usr/bin/env python3
"""
Test completo para diagnosticar comunicación SUNAT.
"""

import os
import sys
from datetime import datetime
from getpass import getpass

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_sunat_communication():
    """Test completo de comunicación SUNAT con diagnóstico detallado."""
    
    print("🔍 TEST DE DIAGNÓSTICO SUNAT")
    print("=" * 50)
    
    try:
        # Importar módulos
        print("📦 Importando módulos...")
        from greenter.see import See
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.ws.soap_client import SoapClient
        print("✅ Módulos importados")
        
        # Solicitar credenciales
        print("\n🔐 CONFIGURACIÓN DE CREDENCIALES:")
        ruc = input("🏢 RUC (11 dígitos): ").strip()
        if not ruc or len(ruc) != 11:
            print("❌ RUC inválido")
            return False
        
        usuario = input("👤 Usuario Clave SOL: ").strip()
        if not usuario:
            print("❌ Usuario requerido")
            return False
        
        password = getpass("🔑 Contraseña Clave SOL: ").strip()
        if not password:
            print("❌ Contraseña requerida")
            return False
        
        print(f"✅ Credenciales configuradas para RUC: {ruc}")
        
        # Test 1: Verificar certificado
        print("\n🔒 TEST 1: VERIFICANDO CERTIFICADO...")
        cert_file = "certificado_prueba.pfx"
        if not os.path.exists(cert_file):
            print("❌ Certificado de prueba no encontrado")
            print("💡 Ejecutar: python create_test_certificate.py")
            return False
        print(f"✅ Certificado encontrado: {cert_file}")
        
        # Test 2: Crear SOAP Client directamente
        print("\n🌐 TEST 2: PROBANDO SOAP CLIENT DIRECTO...")
        soap_client = SoapClient()
        
        # Configurar credenciales PRIMERO
        soap_client.set_credentials(ruc + usuario, password)
        print("✅ Credenciales configuradas en SOAP client")
        
        # Configurar endpoint DESPUÉS (SOLO HOMOLOGACIÓN/PRUEBAS)
        endpoint = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService"
        # PRODUCCIÓN COMENTADO POR SEGURIDAD:
        # endpoint = "https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService"
        soap_client.set_service(endpoint)
        print(f"✅ Endpoint configurado: {endpoint}")
        
        # Verificar estado del client
        if soap_client.client:
            print("✅ SOAP client inicializado correctamente")
            print(f"   Client type: {type(soap_client.client)}")
            try:
                services = list(soap_client.client.service)
                print(f"   Servicios disponibles: {services}")
            except Exception as e:
                print(f"   Error listando servicios: {e}")
        else:
            print("❌ SOAP client no inicializado")
            return False
        
        # Test 3: Crear factura de prueba
        print("\n📄 TEST 3: CREANDO FACTURA DE PRUEBA...")
        
        # Crear objetos
        direccion = Address(
            ubigueo="150101",
            departamento="LIMA",
            provincia="LIMA", 
            distrito="LIMA",
            direccion="AV. PRUEBA 123"
        )
        
        empresa = Company(
            ruc=ruc,
            razon_social="EMPRESA DE PRUEBA",
            address=direccion,
            nombre_comercial="EMPRESA DE PRUEBA"
        )
        
        cliente = Client(
            tipo_doc="1",
            num_doc="12345678",
            rzn_social="CLIENTE DE PRUEBA"
        )
        
        detalle = SaleDetail(
            cod_producto="PROD001",
            unidad="NIU",
            cantidad=1.0,
            descripcion="Producto de prueba",
            mto_valor_unitario=100.0,
            mto_precio_unitario=118.0,
            mto_valor_venta=100.0,
            porcentaje_igv=18.0,
            igv=18.0,
            tipo_afectacion_igv="10",
            total_impuestos=18.0
        )
        
        leyenda = Legend(
            code="1000",
            value="CIENTO DIECIOCHO CON 00/100 SOLES"
        )
        
        factura = Invoice(
            serie="F001",
            correlativo="00000001",
            fecha_emision=datetime.now(),
            tipo_moneda="PEN",
            company=empresa,
            client=cliente,
            details=[detalle],
            legends=[leyenda],
            mto_oper_gravadas=100.0,
            mto_igv=18.0,
            valor_venta=100.0,
            sub_total=118.0,
            mto_imp_venta=118.0
        )
        
        print("✅ Factura de prueba creada")
        
        # Test 4: Usar SEE completo
        print("\n⚙️  TEST 4: CONFIGURANDO SEE...")
        see = See()
        
        # Configurar certificado
        see.set_certificate(cert_file, "123456")
        print("✅ Certificado configurado en SEE")
        
        # Configurar credenciales
        see.set_clave_sol(ruc, usuario, password)
        print("✅ Credenciales configuradas en SEE")
        
        # Configurar endpoint
        see.set_service(endpoint)
        print("✅ Endpoint configurado en SEE")
        
        # Verificar estado del SEE
        if see.soap_client and see.soap_client.client:
            print("✅ SEE configurado correctamente")
        else:
            print("❌ SEE no configurado correctamente")
            return False
        
        # Test 5: Generar XML
        print("\n📝 TEST 5: GENERANDO XML...")
        xml_content = see.get_xml_signed(factura)
        
        if xml_content:
            print(f"✅ XML generado: {len(xml_content)} caracteres")
            
            # Guardar XML
            filename = f"test_sunat_complete_{ruc}_{factura.get_name()}.xml"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"💾 XML guardado: {filename}")
        else:
            print("❌ Error generando XML")
            return False
        
        # Test 6: Envío a SUNAT
        print("\n🚀 TEST 6: ENVIANDO A SUNAT...")
        print("⏳ Enviando documento...")
        
        response = see.send(factura)
        
        # Análisis detallado de respuesta
        print("\n📊 ANÁLISIS DE RESPUESTA:")
        print("-" * 30)
        print(f"Tipo de respuesta: {type(response)}")
        print(f"Success: {response.success}")
        print(f"Error: {response.error}")
        print(f"Code: {response.code}")
        print(f"Description: {response.description}")
        print(f"CDR Response: {response.cdr_response}")
        print(f"Ticket: {response.ticket}")
        print(f"String representation: {str(response)}")
        
        if response.success:
            print("\n🎉 ¡ENVÍO EXITOSO!")
            if response.cdr_response:
                cdr_file = f"cdr_complete_{ruc}_{factura.get_name()}.xml"
                with open(cdr_file, "w", encoding="utf-8") as f:
                    f.write(response.cdr_response)
                print(f"💾 CDR guardado: {cdr_file}")
        else:
            print("\n❌ ERROR EN ENVÍO")
            print(f"🚨 Error: {response.error}")
        
        return response.success
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Función principal."""
    
    print("🧪 GREENTER PYTHON - TEST COMPLETO SUNAT")
    print("=" * 60)
    
    print("\n📋 INFORMACIÓN:")
    print("• Este test diagnostica problemas de comunicación SUNAT")
    print("• Usa endpoint de HOMOLOGACIÓN (no producción)")
    print("• Requiere credenciales reales de Clave SOL")
    print("• Genera archivos XML y CDR para análisis")
    
    print("\n" + "=" * 60)
    respuesta = input("¿Continuar con el test completo? (s/N): ").strip().lower()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("🚫 Test cancelado")
        return 0
    
    success = test_sunat_communication()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡TEST COMPLETO EXITOSO!")
        print("✨ La comunicación SUNAT está funcionando")
    else:
        print("❌ TEST COMPLETO FALLÓ")
        print("🔧 Revisar errores y configuración")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 