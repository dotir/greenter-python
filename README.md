# Greenter Python - Facturación Electrónica SUNAT

Port de la librería Greenter de PHP a Python para facturación electrónica en Perú.

## Instalación

```bash
pip install -r requirements.txt
```

## Uso Básico

```python
from greenter import See
from greenter.core.models.sale import Invoice
from greenter.core.models.company import Company
from greenter.core.models.client import Client

# Configurar SEE
see = See()
see.set_clave_sol("20123456789", "MODDATOS", "MODDATOS")

# Crear factura
invoice = Invoice(
    serie="F001",
    correlativo="00000001",
    # ... otros campos
)

# Generar XML
xml = see.get_xml_signed(invoice)

# Enviar a SUNAT
response = see.send(invoice)
```

## Estado de la Migración

✅ Modelos básicos (Company, Client, Invoice)
✅ Generación de XML con Jinja2
✅ Cliente SOAP básico
✅ Estructura del proyecto
⏳ Firma digital XML (en desarrollo)
⏳ Validaciones completas
⏳ Reportes PDF

## Contribuir

1. Fork el proyecto
2. Crea tu rama de feature
3. Commit tus cambios
4. Push a la rama
5. Crea un Pull Request 