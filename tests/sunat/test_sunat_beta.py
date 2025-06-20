#!/usr/bin/env python3
"""
TEST SUNAT BETA - Endpoint específico para credenciales públicas
"""

import os
import sys
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

def test_sunat_beta():
    """Test con endpoint beta específico para credenciales públicas."""
    
    print("🧪 TEST SUNAT BETA - ENDPOINT ESPECÍFICO")
    print("=" * 60)
    
    try:
        # Importar módulos
        print("📦 Importando módulos...")
        from greenter.see import See
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        
        print("✅ Módulos importados")
        
        # CREDENCIALES PÚBLICAS BETA
        RUC_BETA = "20000000001"
        USER_BETA = "MODDATOS"  
        PASS_BETA = "MODDATOS"
        
        # ENDPOINTS BETA ESPECÍFICOS
        ENDPOINTS_BETA = [
            "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService",
            "https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService", 
            "https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService"
        ]
        
        print(f"🔐 CREDENCIALES BETA:")
        print(f"🏢 RUC: {RUC_BETA}")
        print(f"👤 Usuario: {USER_BETA}")
        print(f"🔑 Contraseña: {PASS_BETA}")
        
        # Verificar certificado
        cert_path = "certificado_prueba.pfx"
        if not os.path.exists(cert_path):
            print(f"❌ Certificado no encontrado: {cert_path}")
            return False
        
        print(f"✅ Certificado encontrado: {cert_path}")
        
        # Crear factura de prueba
        print("\n📄 CREANDO FACTURA BETA...")
        
        address = Address(
            ubigueo="150101",
            departamento="LIMA", 
            provincia="LIMA",
            distrito="LIMA",
            direccion="AV. BETA SUNAT 123"
        )
        
        company = Company(
            ruc=RUC_BETA,
            razon_social="EMPRESA BETA SUNAT",
            nombre_comercial="EMPRESA BETA",
            address=address
        )
        
        client = Client(
            tipo_doc="1",
            num_doc="12345678",
            rzn_social="CLIENTE BETA"
        )
        
        detail = SaleDetail(
            cod_producto="BETA001",
            unidad="NIU",
            cantidad=1.0,
            descripcion="Producto beta SUNAT",
            mto_valor_unitario=100.0,
            mto_valor_venta=100.0,
            mto_base_igv=100.0,
            porcentaje_igv=18.0,
            igv=18.0,
            tipo_afectacion_igv="10",
            mto_precio_unitario=118.0
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
            mto_imp_venta=118.0
        )
        
        print("✅ Factura beta creada")
        print(f"   📄 Número: {invoice.get_name()}")
        print(f"   🏢 Emisor: {company.razon_social}")
        print(f"   💰 Total: S/ {invoice.mto_imp_venta}")
        
        # Probar cada endpoint
        success = False
        
        for i, endpoint in enumerate(ENDPOINTS_BETA, 1):
            print(f"\n🌐 PROBANDO ENDPOINT {i}/{len(ENDPOINTS_BETA)}:")
            print(f"   URL: {endpoint}")
            
            try:
                # Configurar SEE
                see = See()
                
                # Configurar certificado
                see.set_certificate(cert_path, "123456")
                print("   ✅ Certificado configurado")
                
                # Configurar credenciales beta
                see.set_credentials(RUC_BETA, USER_BETA, PASS_BETA)
                print("   ✅ Credenciales beta configuradas")
                
                # Configurar endpoint específico
                see.set_service(endpoint)
                print(f"   ✅ Endpoint configurado: {endpoint}")
                
                # Generar XML
                xml_content = see.get_xml_signed(invoice)
                if not xml_content:
                    print("   ❌ No se pudo generar XML")
                    continue
                
                print(f"   ✅ XML generado: {len(xml_content)} caracteres")
                
                # Guardar XML para este endpoint
                filename = f"beta_{RUC_BETA}_F001-00000001_ep{i}.xml"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(xml_content)
                print(f"   💾 XML guardado: {filename}")
                
                # Enviar a SUNAT
                print(f"   🚀 ENVIANDO A ENDPOINT {i}...")
                response = see.send(invoice)
                
                print(f"\n   📊 RESPUESTA ENDPOINT {i}:")
                print(f"   ----------------------------------------")
                print(f"   Success: {response.success}")
                print(f"   Error: {response.error}")
                print(f"   Code: {response.code}")
                print(f"   Description: {response.description}")
                
                if response.success:
                    print(f"   🎉 ¡ÉXITO CON ENDPOINT {i}!")
                    success = True
                    break
                else:
                    print(f"   ❌ Falló endpoint {i}: {response.code} - {response.error}")
                
            except Exception as e:
                print(f"   ❌ Error con endpoint {i}: {e}")
                continue
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 ¡TEST BETA EXITOSO!")
            print("✨ Se encontró un endpoint funcional")
        else:
            print("❌ TODOS LOS ENDPOINTS BETA FALLARON")
            print("🔧 Posibles causas:")
            print("   • Credenciales públicas deshabilitadas")
            print("   • Endpoints beta no disponibles")
            print("   • Configuración de autenticación incorrecta")
            print("   • Certificado no válido para beta")
        
        return success
        
    except Exception as e:
        print(f"❌ Error en test beta: {e}")
        return False


def main():
    """Función principal."""
    
    print("🚀 GREENTER PYTHON - TEST SUNAT BETA")
    print("🔬 Probando endpoints específicos para credenciales públicas")
    print("⚠️  SOLO PARA DESARROLLO Y PRUEBAS")
    
    success = test_sunat_beta()
    
    if success:
        print("\n📋 PRÓXIMOS PASOS:")
        print("   1. Usar el endpoint que funcionó")
        print("   2. Probar con credenciales reales")
        print("   3. Implementar en producción")
    else:
        print("\n🔧 ACCIONES RECOMENDADAS:")
        print("   1. Verificar documentación SUNAT actualizada")
        print("   2. Contactar soporte técnico SUNAT")
        print("   3. Probar con certificado real")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 