"""
SUNAT Response handler.
"""

from typing import Optional, Dict, Any


class SunatResponse:
    """
    Handles responses from SUNAT web services.
    """
    
    def __init__(self, success: bool = False, code: Optional[str] = None, 
                 description: Optional[str] = None, error: Optional[str] = None,
                 cdr_response: Optional[str] = None, ticket: Optional[str] = None):
        """
        Initialize SUNAT response.
        
        Args:
            success: Whether the operation was successful
            code: Response code
            description: Response description
            error: Error message if any
            cdr_response: CDR (Constancia de Recepción) response
            ticket: Ticket ID for async operations
        """
        self._success = success
        self._code = code
        self._description = description
        self._error = error
        self._cdr_response = cdr_response
        self._ticket = ticket
    
    @property
    def success(self) -> bool:
        """Whether the operation was successful."""
        return self._success
    
    @property
    def code(self) -> Optional[str]:
        """Response code."""
        return self._code
    
    @property
    def description(self) -> Optional[str]:
        """Response description."""
        return self._description
    
    @property
    def error(self) -> Optional[str]:
        """Error message."""
        return self._error
    
    @property
    def cdr_response(self) -> Optional[str]:
        """CDR response."""
        return self._cdr_response
    
    @property
    def ticket(self) -> Optional[str]:
        """Ticket ID."""
        return self._ticket
    
    def is_success(self) -> bool:
        """Check if the operation was successful."""
        return self._success
    
    def get_code(self) -> Optional[str]:
        """Get response code."""
        return self._code
    
    def get_description(self) -> Optional[str]:
        """Get response description."""
        return self._description
    
    def get_error(self) -> Optional[str]:
        """Get error message."""
        return self._error
    
    def get_cdr_response(self) -> Optional[str]:
        """Get CDR response."""
        return self._cdr_response
    
    def get_ticket(self) -> Optional[str]:
        """Get ticket ID."""
        return self._ticket
    
    @classmethod
    def create_success(cls, code: str = "0", description: str = "Operación exitosa", 
                       cdr_response: Optional[str] = None, ticket: Optional[str] = None):
        """Create a successful response."""
        return cls(success=True, code=code, description=description, 
                  cdr_response=cdr_response, ticket=ticket)
    
    @classmethod
    def create_error(cls, error: str, code: Optional[str] = None):
        """Create an error response."""
        return cls(success=False, error=error, code=code)
    
    def __str__(self):
        """String representation."""
        if self._success:
            return f"Success: {self._code} - {self._description}"
        else:
            return f"Error: {self._error}" 