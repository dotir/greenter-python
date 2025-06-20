"""
Error code provider interface and basic implementation.
Migrated from packages/core/src/Core/Validator/
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict


class ErrorCodeProviderInterface(ABC):
    """
    Interface for error code providers.
    """
    
    @abstractmethod
    def get_error_message(self, code: str) -> Optional[str]:
        """
        Get error message for error code.
        
        Args:
            code: Error code
            
        Returns:
            Error message or None if not found
        """
        pass


class BasicErrorCodeProvider(ErrorCodeProviderInterface):
    """
    Basic error code provider with common SUNAT error codes.
    """
    
    def __init__(self):
        """Initialize with basic error codes."""
        self.error_codes: Dict[str, str] = {
            '0': 'Aceptado',
            '1': 'Rechazado',
            '2': 'Anulado',
            '3': 'Observado',
            '4': 'No enviado',
            
            # Common validation errors
            '2001': 'Documento ya fue informado anteriormente',
            '2002': 'No existe el documento',
            '2003': 'Documento no autorizado',
            '2004': 'El RUC no está autorizado',
            '2005': 'El usuario no está autorizado',
            
            # XML validation errors
            '3000': 'Error en la estructura del XML',
            '3001': 'Error en el formato de fecha',
            '3002': 'Error en el formato numérico',
            '3003': 'Código de tipo de documento inválido',
            '3004': 'Número de documento inválido',
            
            # Business validation errors
            '4000': 'Error en los datos del emisor',
            '4001': 'Error en los datos del receptor',
            '4002': 'Error en los datos de la factura',
            '4003': 'Error en los datos de los items',
            '4004': 'Error en los totales',
        }
    
    def get_error_message(self, code: str) -> Optional[str]:
        """
        Get error message for error code.
        
        Args:
            code: Error code
            
        Returns:
            Error message or None if not found
        """
        return self.error_codes.get(code)
    
    def add_error_code(self, code: str, message: str):
        """
        Add or update error code.
        
        Args:
            code: Error code
            message: Error message
        """
        self.error_codes[code] = message 