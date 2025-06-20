"""
Document Interface - Base interface for all documents.
Migrated from packages/core/src/Core/Model/DocumentInterface.php
"""

from abc import ABC, abstractmethod


class DocumentInterface(ABC):
    """
    Interface for all document types in the Greenter system.
    """
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get Name for Document.
        
        Returns:
            str: The document name
        """
        pass 