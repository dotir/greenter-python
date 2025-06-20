# Certificados Digitales

Este directorio contiene los certificados digitales utilizados para la firma de documentos electrónicos.

## ⚠️ IMPORTANTE - SEGURIDAD

- **NUNCA** commits certificados reales (.pfx, .p12) al repositorio
- Los certificados contienen claves privadas sensibles
- Solo commits certificados de prueba claramente identificados

## Archivos

### Certificados de Prueba
- `certificado_prueba.pfx` - Certificado autofirmado para desarrollo
  - Contraseña: `123456`
  - Solo para pruebas y desarrollo
  - NO válido para producción

### Scripts
- `create_test_certificate.py` - Script para generar certificados de prueba

## Uso

### Para Desarrollo
```python
from greenter.see import See

see = See()
see.set_certificate("certificates/certificado_prueba.pfx", "123456")
```

### Para Producción
1. Obtener certificado digital válido de una entidad certificadora autorizada
2. Colocar el certificado en este directorio
3. Configurar la contraseña de forma segura (variables de entorno)
4. Actualizar la configuración de la aplicación

## Entidades Certificadoras Autorizadas en Perú

- ePeru
- Certicámara
- AC Raíz RENIEC
- Otros autorizados por INDECOPI

## Notas

- Los certificados tienen fecha de vencimiento
- Renovar antes del vencimiento para evitar interrupciones
- Mantener backups seguros de los certificados 