# Tests

Este directorio contiene todas las pruebas del proyecto Greenter Python.

## Estructura

### `unit/` - Tests Unitarios
Tests que prueban componentes individuales:
- `test_basic.py` - Tests básicos de modelos y funcionalidad core
- `test_xml_*.py` - Tests de generación XML
- `test_certificate_*.py` - Tests de manejo de certificados

### `integration/` - Tests de Integración  
Tests que prueban la integración entre componentes:
- `test_signature_*.py` - Tests de firma digital completa
- `test_sistema_*.py` - Tests del sistema completo end-to-end

### `sunat/` - Tests de SUNAT
Tests que requieren comunicación con SUNAT:
- `test_sunat_*.py` - Tests de envío a SUNAT
- `test_*_real*.py` - Tests con credenciales reales
- `test_*_homologacion*.py` - Tests con credenciales de homologación

## Ejecución

### Ejecutar todos los tests
```bash
python -m pytest tests/
```

### Ejecutar tests por categoría
```bash
# Solo tests unitarios
python -m pytest tests/unit/

# Solo tests de integración  
python -m pytest tests/integration/

# Solo tests de SUNAT (requieren credenciales)
python -m pytest tests/sunat/
```

### Ejecutar tests específicos
```bash
# Test básico
python tests/unit/test_basic.py

# Test del sistema completo
python tests/integration/test_sistema_completo.py

# Test con credenciales reales (interactivo)
python tests/sunat/test_sunat_real_final.py
```

## Configuración

### Variables de Entorno
Para tests de SUNAT, puedes configurar:
```bash
export SUNAT_RUC="tu_ruc"
export SUNAT_USER="tu_usuario"  
export SUNAT_PASS="tu_contraseña"
```

### Certificados
Los tests usan `certificates/certificado_prueba.pfx` por defecto.

## Notas Importantes

- Los tests de SUNAT requieren conexión a internet
- Los tests con credenciales reales solo usan endpoints de homologación
- Los XMLs generados se guardan en `output/test/`
- Nunca commits credenciales reales en el código 