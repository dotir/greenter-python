#!/usr/bin/env python3
"""
Test de homologación SUNAT con credenciales públicas.
"""

import os
import sys
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_sunat_homologacion_publico():
    """Test usando credenciales públicas de homologación SUNAT."""
    
    print("🧪 TEST HOMOLOGACIÓN SUNAT - CREDENCIALES PÚBLICAS")
    print("=" * 60)
    
    try:
        # Importar módulos
        print("📦 Importando módulos...")
        from greenter.see import See
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        print("✅ Módulos importados")
        
        # Credenciales públicas de homologación SUNAT
        print("\n🔐 USANDO CREDENCIALES PÚBLICAS DE HOMOLOGACIÓN:")
        ruc_homologacion = "20000000001"  # RUC público de homologación
        usuario_homologacion = "MODDATOS"  # Usuario público
        password_homologacion = "MODDATOS"  # Contraseña pública
        
        print(f"🏢 RUC: {ruc_homologacion}")
        print(f"👤 Usuario: {usuario_homologacion}")
        print(f"🔑 Contraseña: {password_homologacion}")
        print("⚠️  Estas son credenciales públicas para pruebas")
        
        # Verificar certificado
        print("\n🔒 VERIFICANDO CERTIFICADO...")
        cert_file = "certificado_prueba.pfx"
        if not os.path.exists(cert_file):
            print("❌ Certificado de prueba no encontrado")
            print("💡 Ejecutar: python create_test_certificate.py")
            return False
        print(f"✅ Certificado encontrado: {cert_file}")
        
        # Crear factura de homologación
        print("\n📄 CREANDO FACTURA DE HOMOLOGACIÓN...")
        
        # Dirección de la empresa
        direccion = Address(
            ubigueo="150101",
            departamento="LIMA",
            provincia="LIMA", 
            distrito="LIMA",
            direccion="AV. HOMOLOGACION 123"
        )
        
        # Empresa de homologación
        empresa = Company(
            ruc=ruc_homologacion,
            razon_social="EMPRESA HOMOLOGACION SUNAT",
            address=direccion,
            nombre_comercial="EMPRESA HOMOLOGACION"
        )
        
        # Cliente de prueba
        cliente = Client(
            tipo_doc="1",  # DNI
            num_doc="12345678",
            rzn_social="CLIENTE HOMOLOGACION"
        )
        
        # Detalle de factura
        detalle = SaleDetail(
            cod_producto="PROD001",
            unidad="NIU",
            cantidad=1.0,
            descripcion="Producto de homologacion SUNAT",
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
        
        print("✅ Factura de homologación creada")
        print(f"   📄 Número: {factura.get_name()}")
        print(f"   🏢 Emisor: {empresa.razon_social}")
        print(f"   💰 Total: S/ {factura.mto_imp_venta}")
        
        # Configurar SEE
        print("\n⚙️  CONFIGURANDO SEE PARA HOMOLOGACIÓN...")
        see = See()
        
        # Configurar certificado
        see.set_certificate(cert_file, "123456")
        print("✅ Certificado configurado")
        
        # Configurar credenciales de homologación
        see.set_clave_sol(ruc_homologacion, usuario_homologacion, password_homologacion)
        print("✅ Credenciales de homologación configuradas")
        
        # Usar endpoint de homologación específico
        endpoint_homologacion = "https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService"
        see.set_service(endpoint_homologacion)
        print(f"✅ Endpoint configurado: {endpoint_homologacion}")
        
        # Verificar configuración
        if see.soap_client and see.soap_client.client:
            print("✅ SEE configurado correctamente")
        else:
            print("❌ SEE no configurado correctamente")
            return False
        
        # Generar XML
        print("\n📝 GENERANDO XML...")
        xml_content = see.get_xml_signed(factura)
        
        if xml_content:
            print(f"✅ XML generado: {len(xml_content)} caracteres")
            
            # Guardar XML
            filename = f"homologacion_{ruc_homologacion}_{factura.get_name()}.xml"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(xml_content)
            print(f"💾 XML guardado: {filename}")
        else:
            print("❌ Error generando XML")
            return False
        
        # Envío a SUNAT
        print("\n🚀 ENVIANDO A SUNAT HOMOLOGACIÓN...")
        print("⏳ Enviando con credenciales públicas...")
        
        response = see.send(factura)
        
        # Análisis de respuesta
        print("\n📊 ANÁLISIS DE RESPUESTA HOMOLOGACIÓN:")
        print("-" * 40)
        print(f"Success: {response.success}")
        print(f"Error: {response.error}")
        print(f"Code: {response.code}")
        print(f"Description: {response.description}")
        print(f"CDR Response: {response.cdr_response}")
        
        if response.success:
            print("\n🎉 ¡ENVÍO A HOMOLOGACIÓN EXITOSO!")
            print("✨ El sistema funciona correctamente")
            
            if response.cdr_response:
                cdr_file = f"cdr_homologacion_{ruc_homologacion}_{factura.get_name()}.xml"
                with open(cdr_file, "w", encoding="utf-8") as f:
                    f.write(response.cdr_response)
                print(f"💾 CDR guardado: {cdr_file}")
                
        else:
            print("\n⚠️  RESPUESTA CON ERRORES:")
            print(f"🔍 Código: {response.code}")
            print(f"🔍 Error: {response.error}")
            
            # Análisis de códigos de error comunes
            if response.code == "0103":
                print("\n📋 ANÁLISIS ERROR 0103:")
                print("• RUC no autorizado para facturación electrónica")
                print("• Credenciales incorrectas")
                print("• Usuario sin permisos")
                
            elif response.code == "2335":
                print("\n📋 ANÁLISIS ERROR 2335:")
                print("• Certificado digital inválido")
                print("• Firma digital incorrecta")
                
            elif response.code in ["0150", "0151", "0152"]:
                print("\n📋 ANÁLISIS ERROR XML:")
                print("• Estructura XML inválida")
                print("• Datos requeridos faltantes")
        
        return response.success
        
    except Exception as e:
        print(f"❌ Error durante el test: {e}")
        import traceback
        traceback.print_exc()
        return False


def mostrar_informacion_homologacion():
    """Mostrar información sobre homologación SUNAT."""
    
    print("\n📋 INFORMACIÓN SOBRE HOMOLOGACIÓN SUNAT:")
    print("=" * 60)
    
    print("\n🧪 CREDENCIALES PÚBLICAS DE HOMOLOGACIÓN:")
    print("   🏢 RUC: 20000000001")
    print("   👤 Usuario: MODDATOS")
    print("   🔑 Contraseña: MODDATOS")
    print("   🌐 Endpoint: https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService")
    
    print("\n✅ VENTAJAS DE USAR HOMOLOGACIÓN:")
    print("   • Credenciales siempre válidas")
    print("   • No requiere habilitación previa")
    print("   • Permite probar el sistema completo")
    print("   • Sin consecuencias legales")
    
    print("\n⚠️  LIMITACIONES:")
    print("   • Documentos no son válidos legalmente")
    print("   • Solo para pruebas y desarrollo")
    print("   • Certificado de prueba no es real")
    
    print("\n🔄 PARA PASAR A PRODUCCIÓN:")
    print("   1. Habilitar RUC en SUNAT para facturación electrónica")
    print("   2. Obtener certificado digital válido")
    print("   3. Configurar credenciales reales")
    print("   4. Cambiar endpoint a producción")


def main():
    """Función principal."""
    
    mostrar_informacion_homologacion()
    
    print("\n" + "=" * 60)
    respuesta = input("¿Probar con credenciales públicas de homologación? (s/N): ").strip().lower()
    
    if respuesta not in ['s', 'si', 'sí', 'y', 'yes']:
        print("🚫 Test cancelado")
        return 0
    
    success = test_sunat_homologacion_publico()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡TEST DE HOMOLOGACIÓN EXITOSO!")
        print("✨ El sistema Greenter está funcionando correctamente")
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. ✅ Sistema validado")
        print("   2. 🔧 Habilitar tu RUC en SUNAT")
        print("   3. 🔑 Obtener certificado digital real")
        print("   4. 🚀 Configurar para producción")
    else:
        print("❌ TEST DE HOMOLOGACIÓN FALLÓ")
        print("🔧 Revisar configuración del sistema")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 