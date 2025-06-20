"""
Sistema de Emisión del Contribuyente (SEE).
Main entry point for the Greenter system.
Migrated from packages/lite/src/Greenter/See.php
"""

from typing import Optional, Dict, Any
from datetime import datetime
import logging

from .core.models.document_interface import DocumentInterface
from .core.models.sale import BaseSale
from .xml.builder import XmlBuilder
from .ws.soap_client import SoapClient
from .signer.xml_signer import XmlSigner
from .validator.error_code_provider import ErrorCodeProviderInterface


logger = logging.getLogger(__name__)


class See:
    """
    Sistema de Emision del Contribuyente.
    Main class for electronic invoicing in Peru.
    """
    
    def __init__(self):
        """Initialize the SEE system with default components."""
        self.xml_builder: Optional[XmlBuilder] = None
        self.soap_client: Optional[SoapClient] = None
        self.xml_signer: Optional[XmlSigner] = None
        self.error_code_provider: Optional[ErrorCodeProviderInterface] = None
        
        # Twig/Jinja2 render options
        self.builder_options: Dict[str, Any] = {
            'autoescape': False,
            'cache': False
        }
        
        # Initialize default components
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize default components."""
        try:
            self.xml_builder = XmlBuilder(self.builder_options)
            self.soap_client = SoapClient()
            self.xml_signer = XmlSigner()
        except ImportError as e:
            logger.warning(f"Could not initialize component: {e}")
    
    def set_builder_options(self, options: Dict[str, Any]) -> None:
        """
        Set XML Builder Options.
        
        Args:
            options: Dictionary with builder options
        """
        self.builder_options.update(options)
        if self.xml_builder:
            self.xml_builder.update_options(self.builder_options)
    
    def set_cache_path(self, directory: Optional[str]) -> None:
        """
        Set cache directory path.
        
        Args:
            directory: Cache directory path, None to disable cache
        """
        cache_option = False if not directory else directory
        self.builder_options['cache'] = cache_option
        if self.xml_builder:
            self.xml_builder.update_options(self.builder_options)
    
    def set_certificate(self, certificate: str) -> None:
        """
        Set digital certificate for XML signing.
        
        Args:
            certificate: Certificate content or path
        """
        if self.xml_signer:
            self.xml_signer.set_certificate(certificate)
    
    def set_credentials(self, user: str, password: str) -> None:
        """
        Set SOAP credentials.
        
        Args:
            user: Username
            password: Password
        """
        if self.soap_client:
            self.soap_client.set_credentials(user, password)
    
    def set_clave_sol(self, ruc: str, user: str, password: str) -> None:
        """
        Set Clave SOL credentials for secondary user.
        
        Args:
            ruc: Company RUC
            user: Username
            password: Password
        """
        if self.soap_client:
            self.soap_client.set_credentials(f"{ruc}{user}", password)
    
    def set_service(self, service_url: Optional[str]) -> None:
        """
        Set SOAP service URL.
        
        Args:
            service_url: SOAP service endpoint URL
        """
        if self.soap_client:
            self.soap_client.set_service(service_url)
    
    def set_error_code_provider(self, provider: Optional[ErrorCodeProviderInterface]) -> None:
        """
        Set error code provider.
        
        Args:
            provider: Error code provider instance
        """
        self.error_code_provider = provider
    
    def get_xml_signed(self, document: DocumentInterface) -> Optional[str]:
        """
        Get signed XML from document.
        
        Args:
            document: Document to convert to XML
            
        Returns:
            Signed XML string or None if error
        """
        if not self.xml_builder:
            logger.error("XML Builder not initialized")
            return None
            
        try:
            # Generate XML
            xml_content = self.xml_builder.build(document)
            
            # Sign XML if signer is available
            if self.xml_signer and xml_content:
                xml_content = self.xml_signer.sign(xml_content)
            
            return xml_content
            
        except Exception as e:
            logger.error(f"Error generating signed XML: {e}")
            return None
    
    def send(self, document: DocumentInterface) -> Optional[Dict[str, Any]]:
        """
        Send document to SUNAT.
        
        Args:
            document: Document to send
            
        Returns:
            Response dictionary or None if error
        """
        if not self.soap_client:
            logger.error("SOAP Client not initialized")
            return None
        
        try:
            # Get signed XML
            xml_content = self.get_xml_signed(document)
            if not xml_content:
                return None
            
            # Determine filename
            filename = self._get_filename(document)
            
            # Send via SOAP
            response = self.soap_client.send(filename, xml_content)
            
            return response
            
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            return None
    
    def send_xml(self, document_type: str, filename: str, xml_content: str) -> Optional[Dict[str, Any]]:
        """
        Send pre-generated XML.
        
        Args:
            document_type: Type of document
            filename: XML filename
            xml_content: XML content
            
        Returns:
            Response dictionary or None if error
        """
        if not self.soap_client:
            logger.error("SOAP Client not initialized")
            return None
        
        try:
            response = self.soap_client.send(filename, xml_content)
            return response
            
        except Exception as e:
            logger.error(f"Error sending XML: {e}")
            return None
    
    def send_xml_file(self, xml_content: str) -> Optional[Dict[str, Any]]:
        """
        Send XML file content.
        
        Args:
            xml_content: Complete XML content
            
        Returns:
            Response dictionary or None if error
        """
        try:
            # Parse XML to determine document type and extract filename
            # This would need XML parsing logic
            # For now, we'll use a simple approach
            
            # Extract document info from XML
            doc_info = self._extract_document_info(xml_content)
            if not doc_info:
                return None
            
            return self.send_xml(
                doc_info['type'], 
                doc_info['filename'], 
                xml_content
            )
            
        except Exception as e:
            logger.error(f"Error sending XML file: {e}")
            return None
    
    def get_status(self, ticket: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Get status of submitted document.
        
        Args:
            ticket: Ticket ID from submission
            
        Returns:
            Status response or None if error
        """
        if not self.soap_client:
            logger.error("SOAP Client not initialized")
            return None
        
        try:
            response = self.soap_client.get_status(ticket)
            return response
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return None
    
    def _get_filename(self, document: DocumentInterface) -> str:
        """
        Generate filename for document.
        
        Args:
            document: Document instance
            
        Returns:
            Generated filename
        """
        # This would need to be implemented based on document type
        # For now, return a basic filename
        if hasattr(document, 'get_name'):
            return document.get_name()
        return f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _extract_document_info(self, xml_content: str) -> Optional[Dict[str, str]]:
        """
        Extract document information from XML content.
        
        Args:
            xml_content: XML content
            
        Returns:
            Dictionary with document info or None if error
        """
        try:
            # This would need proper XML parsing
            # For now, return a basic structure
            return {
                'type': 'invoice',
                'filename': f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        except Exception as e:
            logger.error(f"Error extracting document info: {e}")
            return None 