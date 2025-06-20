#!/usr/bin/env python3
"""
Test de envío real a SUNAT usando Clave SOL.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_envio_sunat_real():
    """Test de envío real a SUNAT."""
    
    print("🌐 TEST DE ENVÍO REAL A SUNAT")
    print("=" * 50)
    
    # IMPORTANTE: Configurar credenciales reales
    print("\n🔐 CONFIGURACIÓN DE CREDENCIALES:")
    print("⚠️  IMPORTANTE: Este test requiere credenciales reales de SUNAT")
    print("📋 Por favor, proporciona tus credenciales:")
    
    # Solicitar credenciales de forma segura
    ruc = input("🏢 RUC (10 dígitos para persona natural): ").strip()
    usuario = input("👤 Usuario Clave SOL: ").strip()
    
    # Validar RUC de persona natural
    if not ruc.startswith('10') or len(ruc) != 11:
        print("❌ Error: RUC debe ser de persona natural (11 dígitos, empezar con 10)")
        return False
    
    # Importar getpass para contraseña segura
    try:
        import getpass
        password = getpass.getpass("🔑 Contraseña Clave SOL: ")
    except ImportError:
        password = input("🔑 Contraseña Clave SOL: ").strip()
    
    if not all([ruc, usuario, password]):
        print("❌ Error: Todas las credenciales son requeridas")
        return False
    
    print(f"✅ Credenciales configuradas para RUC: {ruc}")
    
    try:
        # Importar módulos
        print("\n📦 IMPORTANDO MÓDULOS...")
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.see import See
        
        print("✅ Módulos importados")
        
        # Crear datos de factura para persona natural
        print("\n🏗️  CREANDO FACTURA DE PRUEBA...")
        
        # Dirección (usar datos genéricos para prueba)
        direccion = Address(
            ubigueo="150101",  # Lima
            departamento="LIMA",
            provincia="LIMA",
            distrito="LIMA",
            direccion="DIRECCION DE PRUEBA 123"
        )
        
        # Empresa (persona natural)
        empresa = Company(
            ruc=ruc,
            razon_social="PERSONA NATURAL DE PRUEBA",  # Cambiar por tu nombre real
            address=direccion,
            nombre_comercial="NEGOCIO DE PRUEBA"
        )
        
        # Cliente de prueba
        cliente = Client(
            tipo_doc="1",  # DNI
            num_doc="12345678",
            rzn_social="CLIENTE DE PRUEBA"
        )
        
        # Detalle de factura simple
        detalle = SaleDetail(
            cod_producto="SERV001",
            unidad="ZZ",  # Servicios
            cantidad=1.0,
            descripcion="Servicio de prueba para validar envío SUNAT",
            mto_valor_unitario=100.0,
            mto_precio_unitario=118.0,
            mto_valor_venta=100.0,
            porcentaje_igv=18.0,
            igv=18.0,
            tipo_afectacion_igv="10",
            total_impuestos=18.0
        )
        
        # Leyenda
        leyenda = Legend(
            code="1000",
            value="CIENTO DIECIOCHO CON 00/100 SOLES"
        )
        
        # Factura
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
        print(f"   📄 Número: {factura.get_name()}")
        print(f"   🏢 Emisor: {empresa.razon_social}")
        print(f"   💰 Total: S/ {factura.mto_imp_venta}")
        
        # Configurar SEE
        print("\n⚙️  CONFIGURANDO SISTEMA SEE...")
        see = See()
        
        # Configurar certificado de prueba
        cert_file = "certificado_prueba.pfx"
        if not os.path.exists(cert_file):
            print("❌ Certificado de prueba no encontrado")
            print("💡 Ejecutar: python create_test_certificate.py")
            return False
        
        see.set_certificate(cert_file, "123456")
        print("✅ Certificado configurado")
        
        # Configurar credenciales SUNAT
        see.set_clave_sol(ruc, usuario, password)
        print("✅ Credenciales Clave SOL configuradas")
        
        # Configurar endpoint de homologación
        # ⚠️  IMPORTANTE: SOLO HOMOLOGACIÓN/PRUEBAS - NO PRODUCCIÓN
        endpoint_homologacion = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService"
        # PRODUCCIÓN COMENTADO POR SEGURIDAD:
        # endpoint_produccion = "https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService"
        see.set_service(endpoint_homologacion)
        print(f"✅ Endpoint configurado: {endpoint_homologacion}")
        
        # Generar XML firmado
        print("\n📄 GENERANDO XML FIRMADO...")
        xml_firmado = see.get_xml_signed(factura)
        
        if not xml_firmado:
            print("❌ Error generando XML firmado")
            return False
        
        print(f"✅ XML firmado generado: {len(xml_firmado)} caracteres")
        
        # Guardar XML para revisión
        archivo_xml = f"factura_sunat_{ruc}_{factura.get_name()}.xml"
        with open(archivo_xml, "w", encoding="utf-8") as f:
            f.write(xml_firmado)
        print(f"💾 XML guardado: {archivo_xml}")
        
        # ENVIAR A SUNAT
        print("\n🚀 ENVIANDO A SUNAT...")
        print("⏳ Esto puede tomar unos segundos...")
        
        response = see.send(factura)
        
        # Procesar respuesta
        print("\n📨 RESPUESTA DE SUNAT:")
        print("=" * 30)
        
        if response.success:
            print("🎉 ¡ENVÍO EXITOSO!")
            print(f"✅ Estado: Exitoso")
            if response.code:
                print(f"📋 Código: {response.code}")
            if response.description:
                print(f"📝 Descripción: {response.description}")
            if response.cdr_response:
                print(f"📄 CDR recibido: Sí")
                # Guardar CDR si está disponible
                cdr_file = f"cdr_{ruc}_{factura.get_name()}.xml"
                with open(cdr_file, "w", encoding="utf-8") as f:
                    f.write(response.cdr_response)
                print(f"💾 CDR guardado: {cdr_file}")
        else:
            print("❌ ERROR EN ENVÍO")
            if response.error:
                print(f"🚨 Error: {response.error}")
            if response.code:
                print(f"📋 Código de error: {response.code}")
            if response.description:
                print(f"📝 Descripción: {response.description}")
        
        # Debug info
        print(f"\n🔍 DEBUG INFO:")
        print(f"   Success: {response.success}")
        print(f"   Error: {response.error}")
        print(f"   Code: {response.code}")
        print(f"   Description: {response.description}")
        
        return response.success
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


def mostrar_informacion_importante():
    """Mostrar información importante sobre el envío a SUNAT."""
    
    print("\n📋 INFORMACIÓN IMPORTANTE:")
    print("=" * 50)
    
    print("\n🔐 CREDENCIALES REQUERIDAS:")
    print("   🏢 RUC: Tu RUC de persona natural (11 dígitos, empieza con 10)")
    print("   👤 Usuario: Tu usuario de Clave SOL")
    print("   🔑 Contraseña: Tu contraseña de Clave SOL")
    
    print("\n⚠️  CONSIDERACIONES IMPORTANTES:")
    print("   • Este test usa HOMOLOGACIÓN de SUNAT (no producción)")
    print("   • El certificado de prueba NO es válido para SUNAT real")
    print("   • Para producción necesitas certificado digital válido")
    print("   • Los datos de la factura son de PRUEBA")
    
    print("\n🌐 ENDPOINTS SUNAT:")
    print("   🧪 Homologación: https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService")
    print("   🏭 Producción: https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService")
    
    print("\n📄 ARCHIVOS QUE SE GENERARÁN:")
    print("   📝 factura_sunat_{RUC}_F001-00000001.xml - XML firmado enviado")
    print("   📨 cdr_{RUC}_F001-00000001.xml - Respuesta CDR de SUNAT (si exitoso)")
    
    print("\n🔄 PRÓXIMOS PASOS SI FUNCIONA:")
    print("   1. Obtener certificado digital real")
    print("   2. Actualizar datos de empresa reales")
    print("   3. Probar en producción")
    print("   4. Implementar manejo completo de CDR")


def main():
    """Función principal."""
    
    mostrar_informacion_importante()
    
    print("\n" + "=" * 50)
    respuesta = input("¿Continuar con el test de envío a SUNAT? (s/N): ").strip().lower()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("🚫 Test cancelado por el usuario")
        return 0
    
    success = test_envio_sunat_real()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡ENVÍO A SUNAT EXITOSO!")
        print("✨ El sistema está funcionando correctamente")
        print("📋 Revisar archivos XML y CDR generados")
    else:
        print("❌ ERROR EN ENVÍO A SUNAT")
        print("🔧 Revisar credenciales y configuración")
        print("💡 Verificar que el RUC esté habilitado para facturación electrónica")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 