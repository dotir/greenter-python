#!/usr/bin/env python3
"""
Test básico para verificar la migración de Greenter.
"""

import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'greenter-python'))

def test_basic_models():
    """Test básico de los modelos migrados."""
    
    print("🧪 Iniciando tests básicos...")
    
    try:
        # Test 1: Importar modelos básicos
        print("📦 Test 1: Importando modelos...")
        from greenter.core.models.company import Company, Address
        from greenter.core.models.client import Client
        from greenter.core.models.sale import Invoice, SaleDetail, Legend
        print("✅ Modelos importados exitosamente")
        
        # Test 2: Crear objetos básicos
        print("🏗️  Test 2: Creando objetos...")
        
        address = Address(
            ubigueo="150101",
            departamento="LIMA",
            provincia="LIMA",
            distrito="LIMA",
            direccion="AV. EJEMPLO 123"
        )
        
        company = Company(
            ruc="20123456789",
            razon_social="EMPRESA EJEMPLO S.A.C.",
            address=address
        )
        
        client = Client(
            tipo_doc="6",
            num_doc="20987654321",
            rzn_social="CLIENTE EJEMPLO S.A.C."
        )
        
        detail = SaleDetail(
            cod_producto="P001",
            unidad="NIU",
            cantidad=1.0,
            descripcion="Producto de ejemplo"
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
            legends=[legend]
        )
        
        print("✅ Objetos creados exitosamente")
        
        # Test 3: Verificar propiedades
        print("🔍 Test 3: Verificando propiedades...")
        
        assert company.get_ruc() == "20123456789"
        assert client.get_num_doc() == "20987654321"
        assert invoice.get_name() == "F001-00000001"
        
        print("✅ Propiedades verificadas")
        
        # Test 4: Importar clase principal SEE
        print("🎯 Test 4: Importando clase SEE...")
        from greenter.see import See
        
        see = See()
        print("✅ Clase SEE importada y instanciada")
        
        # Test 5: Test de serialización Pydantic
        print("📄 Test 5: Probando serialización...")
        
        invoice_dict = invoice.dict()
        assert 'serie' in invoice_dict
        assert 'correlativo' in invoice_dict
        
        print("✅ Serialización funcionando")
        
        print("\n🎉 ¡Todos los tests básicos pasaron exitosamente!")
        print("✨ La migración de Greenter a Python está funcionando correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        return False


def test_xml_generation():
    """Test básico de generación XML."""
    
    print("\n🔧 Test de generación XML...")
    
    try:
        from greenter.xml.builder import XmlBuilder
        from greenter.core.models.sale import Invoice
        from greenter.core.models.company import Company
        from greenter.core.models.client import Client
        from datetime import datetime
        
        # Crear objetos mínimos
        company = Company(ruc="20123456789", razon_social="TEST COMPANY")
        client = Client(tipo_doc="6", num_doc="20987654321", rzn_social="TEST CLIENT")
        
        invoice = Invoice(
            serie="F001",
            correlativo="00000001",
            fecha_emision=datetime.now(),
            company=company,
            client=client
        )
        
        # Crear builder
        builder = XmlBuilder()
        
        # Generar XML
        xml_content = builder.build(invoice)
        
        if xml_content:
            print("✅ XML generado exitosamente")
            print(f"📏 Tamaño: {len(xml_content)} caracteres")
            
            # Verificar contenido básico
            assert '<?xml version="1.0"' in xml_content
            assert 'F001-00000001' in xml_content
            assert '20123456789' in xml_content
            
            print("✅ Contenido XML verificado")
            return True
        else:
            print("❌ No se pudo generar XML")
            return False
            
    except Exception as e:
        print(f"❌ Error en generación XML: {e}")
        return False


def main():
    """Función principal."""
    
    print("🚀 Greenter Python - Verificación de Migración")
    print("=" * 50)
    
    # Ejecutar tests
    success = True
    
    success &= test_basic_models()
    success &= test_xml_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡MIGRACIÓN EXITOSA!")
        print("✨ Greenter ha sido migrado correctamente a Python")
        print("\n📋 Próximos pasos:")
        print("   1. Instalar dependencias: pip install -r requirements.txt")
        print("   2. Configurar certificado digital")
        print("   3. Probar con credenciales SUNAT")
        print("   4. Implementar casos de uso específicos")
    else:
        print("❌ MIGRACIÓN INCOMPLETA")
        print("🔧 Revisar errores y dependencias")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main()) 