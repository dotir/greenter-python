# Greenter Python

Sistema de facturación electrónica para Perú basado en Python. Implementación completa compatible con SUNAT para la generación, firma y envío de comprobantes de pago electrónicos.

## ✨ Características

- **📄 Generación XML UBL 2.1** - Estándar internacional para documentos electrónicos
- **🔐 Firma Digital** - Soporte completo para certificados digitales
- **🌐 Integración SUNAT** - Comunicación directa con servicios web SUNAT
- **🧪 Entorno de Pruebas** - Tests completos y certificados de desarrollo
- **📊 Modelos Pydantic V2** - Validación robusta de datos
- **🚀 Listo para Producción** - Código probado y documentado

## 🏗️ Estructura del Proyecto

```
greenter-python/
├── greenter/                 # Código fuente principal
│   ├── core/                 # Modelos y lógica de negocio
│   ├── signer/              # Firma digital XML
│   ├── ws/                  # Servicios web SOAP
│   └── xml/                 # Generación XML UBL
├── tests/                   # Suite completa de tests
│   ├── unit/                # Tests unitarios
│   ├── integration/         # Tests de integración
│   └── sunat/               # Tests con SUNAT
├── output/                  # Archivos generados
│   ├── xml/                 # XMLs sin firmar
│   ├── signed/              # XMLs firmados
│   └── test/                # Archivos de prueba
├── certificates/            # Certificados digitales
├── docs/                    # Documentación
├── examples/                # Ejemplos de uso
└── temp/                    # Archivos temporales
```

## 🚀 Instalación

### Requisitos
- Python 3.8+
- pip

### Instalación
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/greenter-python.git
cd greenter-python

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## 📖 Uso Básico

### Crear una Factura
```python
from greenter.see import See
from greenter.core.models.sale import Invoice, SaleDetail
from greenter.core.models.company import Company, Address
from greenter.core.models.client import Client
from datetime import datetime

# Configurar emisor
address = Address(
    ubigueo="150101",
    departamento="LIMA",
    provincia="LIMA", 
    distrito="LIMA",
    direccion="AV. EJEMPLO 123"
)

company = Company(
    ruc="20123456789",
    razon_social="MI EMPRESA S.A.C.",
    nombre_comercial="MI EMPRESA",
    address=address
)

# Configurar cliente
client = Client(
    tipo_doc="1",
    num_doc="12345678",
    rzn_social="CLIENTE EJEMPLO"
)

# Crear detalle
detail = SaleDetail(
    cod_producto="PROD001",
    unidad="NIU",
    cantidad=1.0,
    descripcion="Producto ejemplo",
    mto_valor_unitario=100.0,
    mto_precio_unitario=118.0
)

# Crear factura
invoice = Invoice(
    serie="F001",
    correlativo="00000001",
    fecha_emision=datetime.now(),
    tipo_moneda="PEN",
    company=company,
    client=client,
    details=[detail],
    mto_oper_gravadas=100.0,
    mto_igv=18.0,
    mto_imp_venta=118.0
)

# Configurar SEE
see = See()
see.set_certificate("certificates/certificado.pfx", "contraseña")
see.set_credentials("20123456789", "usuario", "contraseña")

# Generar y enviar
xml_content = see.get_xml_signed(invoice)
response = see.send(invoice)

if response.success:
    print("✅ Factura enviada exitosamente")
else:
    print(f"❌ Error: {response.error}")
```

## 🧪 Testing

### Ejecutar Tests
```bash
# Todos los tests
python -m pytest tests/

# Tests específicos
python tests/unit/test_basic.py
python tests/integration/test_sistema_completo.py
python tests/sunat/test_sunat_real_final.py
```

### Test Básico
```bash
python tests/unit/test_basic.py
```

### Test con SUNAT (Interactivo)
```bash
python tests/sunat/test_sunat_real_final.py
```

## 📋 Configuración SUNAT

### Homologación (Pruebas)
```python
see.set_credentials("tu_ruc", "tu_usuario", "tu_contraseña")
see.set_service("https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService")
```

### Producción
```python
see.set_credentials("tu_ruc", "tu_usuario", "tu_contraseña")  
see.set_service("https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService")
```

## 🔐 Certificados Digitales

### Desarrollo
Usa el certificado de prueba incluido:
```python
see.set_certificate("certificates/certificado_prueba.pfx", "123456")
```

### Producción
1. Obtener certificado digital de entidad autorizada
2. Colocar en `certificates/`
3. Configurar contraseña de forma segura

## 📚 Documentación

- [Guía de Instalación](docs/INSTALL.md)
- [API Reference](docs/API.md)
- [Ejemplos](examples/)
- [Tests](tests/README.md)
- [Certificados](certificates/README.md)

## 🆘 Soporte

### Errores Comunes
- **Error 0103**: RUC no habilitado para facturación electrónica
- **Error 0104**: XML no cumple validaciones SUNAT
- **Error 0130**: Certificado digital inválido

### Contacto SUNAT
- Teléfono: 0-801-12-100
- Web: [sunat.gob.pe](https://www.sunat.gob.pe)

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- Basado en [Greenter](https://github.com/thegreenter/greenter) de PHP
- Comunidad de desarrolladores de facturación electrónica Perú
- SUNAT por la documentación técnica

## 📊 Estado del Proyecto

- ✅ Modelos Pydantic V2: 100% funcional
- ✅ Generación XML UBL 2.1: 100% funcional  
- ✅ Firma digital: 100% funcional
- ✅ Comunicación SOAP: 100% funcional
- ✅ Tests completos: 100% funcional
- 🔄 Documentación: En progreso
- 🔄 Más tipos de documento: En desarrollo

---

**🚀 ¡Listo para facturación electrónica en Perú!** 