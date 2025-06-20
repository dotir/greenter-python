#!/usr/bin/env python3
"""
Configuración centralizada para Greenter Python
"""

import os
from pathlib import Path

# Directorios del proyecto
PROJECT_ROOT = Path(__file__).parent
GREENTER_DIR = PROJECT_ROOT / "greenter"
TESTS_DIR = PROJECT_ROOT / "tests"
OUTPUT_DIR = PROJECT_ROOT / "output"
CERTIFICATES_DIR = PROJECT_ROOT / "certificates"
DOCS_DIR = PROJECT_ROOT / "docs"
TEMP_DIR = PROJECT_ROOT / "temp"

# Configuración de certificados
DEFAULT_CERTIFICATE_PATH = CERTIFICATES_DIR / "certificado_prueba.pfx"
DEFAULT_CERTIFICATE_PASSWORD = "123456"

# Endpoints SUNAT
class SunatEndpoints:
    """Endpoints de SUNAT para diferentes entornos."""
    
    # HOMOLOGACIÓN (Pruebas) - SEGURO
    HOMOLOGACION = "https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService"
    BETA = "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService"
    
    # PRODUCCIÓN - ¡CUIDADO! Solo para uso real
    # PRODUCCION = "https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService"
    
    @classmethod
    def get_default(cls):
        """Obtener endpoint por defecto (homologación)."""
        return cls.HOMOLOGACION

# Credenciales públicas de homologación
class HomologacionCredentials:
    """Credenciales públicas para homologación."""
    
    RUC = "20000000001"
    USER = "MODDATOS"
    PASSWORD = "MODDATOS"

# Configuración de archivos de salida
class OutputConfig:
    """Configuración para archivos de salida."""
    
    XML_DIR = OUTPUT_DIR / "xml"
    SIGNED_DIR = OUTPUT_DIR / "signed"
    TEST_DIR = OUTPUT_DIR / "test"
    
    @classmethod
    def ensure_directories(cls):
        """Crear directorios si no existen."""
        for dir_path in [cls.XML_DIR, cls.SIGNED_DIR, cls.TEST_DIR]:
            dir_path.mkdir(parents=True, exist_ok=True)

# Configuración de logging
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.FileHandler',
            'filename': str(PROJECT_ROOT / 'greenter.log'),
            'mode': 'a',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default', 'file'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

# Configuración de tests
class TestConfig:
    """Configuración para tests."""
    
    # Timeout para tests de SUNAT (segundos)
    SUNAT_TIMEOUT = 30
    
    # Certificado para tests
    TEST_CERTIFICATE = DEFAULT_CERTIFICATE_PATH
    TEST_CERTIFICATE_PASSWORD = DEFAULT_CERTIFICATE_PASSWORD
    
    # Endpoint para tests
    TEST_ENDPOINT = SunatEndpoints.HOMOLOGACION

# Variables de entorno
def get_env_var(name: str, default=None):
    """Obtener variable de entorno con valor por defecto."""
    return os.getenv(name, default)

def get_sunat_credentials():
    """Obtener credenciales SUNAT desde variables de entorno."""
    return {
        'ruc': get_env_var('SUNAT_RUC'),
        'user': get_env_var('SUNAT_USER'),
        'password': get_env_var('SUNAT_PASS')
    }

def get_certificate_config():
    """Obtener configuración de certificado desde variables de entorno."""
    return {
        'path': get_env_var('CERTIFICATE_PATH', str(DEFAULT_CERTIFICATE_PATH)),
        'password': get_env_var('CERTIFICATE_PASSWORD', DEFAULT_CERTIFICATE_PASSWORD)
    }

# Configuración por defecto para SEE
DEFAULT_SEE_CONFIG = {
    'certificate_path': str(DEFAULT_CERTIFICATE_PATH),
    'certificate_password': DEFAULT_CERTIFICATE_PASSWORD,
    'endpoint': SunatEndpoints.get_default(),
    'timeout': 30,
    'validate_ssl': True
}

# Información del proyecto
PROJECT_INFO = {
    'name': 'Greenter Python',
    'version': '1.0.0',
    'description': 'Sistema de facturación electrónica para Perú',
    'author': 'Tu Nombre',
    'license': 'MIT',
    'url': 'https://github.com/tu-usuario/greenter-python'
}

# Inicialización
def init_project():
    """Inicializar configuración del proyecto."""
    
    # Crear directorios necesarios
    OutputConfig.ensure_directories()
    CERTIFICATES_DIR.mkdir(exist_ok=True)
    TEMP_DIR.mkdir(exist_ok=True)
    
    # Configurar logging
    import logging.config
    logging.config.dictConfig(LOGGING_CONFIG)
    
    logger = logging.getLogger(__name__)
    logger.info(f"Inicializando {PROJECT_INFO['name']} v{PROJECT_INFO['version']}")

if __name__ == "__main__":
    # Mostrar configuración actual
    print(f"🚀 {PROJECT_INFO['name']} v{PROJECT_INFO['version']}")
    print("=" * 50)
    print(f"📁 Directorio del proyecto: {PROJECT_ROOT}")
    print(f"🔐 Certificado por defecto: {DEFAULT_CERTIFICATE_PATH}")
    print(f"🌐 Endpoint por defecto: {SunatEndpoints.get_default()}")
    print(f"📤 Directorio de salida: {OUTPUT_DIR}")
    
    # Verificar archivos importantes
    print("\n📋 Estado de archivos:")
    files_to_check = [
        ("Certificado de prueba", DEFAULT_CERTIFICATE_PATH),
        ("Directorio greenter", GREENTER_DIR),
        ("Directorio tests", TESTS_DIR),
        ("Directorio output", OUTPUT_DIR),
    ]
    
    for name, path in files_to_check:
        exists = "✅" if path.exists() else "❌"
        print(f"{exists} {name}: {path}")
    
    print(f"\n✨ Configuración lista para usar") 