"""
SOAP Client for communication with SUNAT services.
Migrated from packages/ws/src/Ws/Services/
"""

from typing import Optional, Dict, Any
import logging
import base64
import zipfile
import io
from zeep import Client, Transport
from zeep.wsse.username import UsernameToken
from requests import Session
from requests.auth import HTTPBasicAuth


logger = logging.getLogger(__name__)


class SunatEndpoints:
    """
    SUNAT service endpoints.
    Migrated from packages/ws/src/Ws/Services/SunatEndpoints.php
    """
    
    # FACTURACION SERVICES
    FE_BETA = 'https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService'
    FE_HOMOLOGACION = 'https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService'
    FE_PRODUCCION = 'https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService'
    FE_CONSULTA_CDR = 'https://e-factura.sunat.gob.pe/ol-it-wsconscpegem/billConsultService'
    
    # GUIA DE REMISION SERVICES (deprecated, use API endpoint)
    GUIA_BETA = 'https://e-beta.sunat.gob.pe/ol-ti-itemision-guia-gem-beta/billService'
    GUIA_PRODUCCION = 'https://e-guiaremision.sunat.gob.pe/ol-ti-itemision-guia-gem/billService'
    
    # RETENCION Y PERCEPCION SERVICES
    RETENCION_BETA = 'https://e-beta.sunat.gob.pe/ol-ti-itemision-otroscpe-gem-beta/billService'
    RETENCION_PRODUCCION = 'https://e-factura.sunat.gob.pe/ol-ti-itemision-otroscpe-gem/billService'
    
    # WSDL Uri
    WSDL_ENDPOINT = 'https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl'


class SoapClient:
    """
    SOAP Client for SUNAT web services.
    """
    
    def __init__(self):
        """Initialize SOAP client."""
        self.username: Optional[str] = None
        self.password: Optional[str] = None
        self.service_url: Optional[str] = None
        self.client: Optional[Client] = None
        self.session = Session()
    
    def set_credentials(self, username: str, password: str):
        """
        Set SOAP credentials.
        
        Args:
            username: Username
            password: Password
        """
        self.username = username
        self.password = password
        self._setup_client()
    
    def set_service(self, service_url: Optional[str]):
        """
        Set service URL.
        
        Args:
            service_url: SOAP service endpoint URL
        """
        self.service_url = service_url
        self._setup_client()
    
    def _setup_client(self):
        """Setup SOAP client with credentials and service URL."""
        if not self.username or not self.password:
            return
        
        try:
            # Setup session with authentication
            self.session.auth = HTTPBasicAuth(self.username, self.password)
            
            # Create transport
            transport = Transport(session=self.session)
            
            # Create SOAP client
            wsdl_url = SunatEndpoints.WSDL_ENDPOINT
            self.client = Client(wsdl_url, transport=transport)
            
            # Set service URL if provided
            if self.service_url:
                # Update service binding
                service = self.client.service
                if hasattr(service, '_binding'):
                    service._binding.address = self.service_url
            
        except Exception as e:
            logger.error(f"Error setting up SOAP client: {e}")
            self.client = None
    
    def send(self, filename: str, xml_content: str) -> Optional[Dict[str, Any]]:
        """
        Send XML document to SUNAT.
        
        Args:
            filename: XML filename
            xml_content: XML content
            
        Returns:
            Response dictionary or None if error
        """
        if not self.client:
            logger.error("SOAP client not initialized")
            return None
        
        try:
            # Compress XML content
            zip_content = self._compress_xml(filename, xml_content)
            if not zip_content:
                return None
            
            # Prepare parameters
            zip_filename = f"{filename}.zip"
            
            # Call SOAP service
            response = self.client.service.sendBill(
                fileName=zip_filename,
                contentFile=zip_content
            )
            
            # Process response
            return self._process_send_response(response)
            
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            return None
    
    def send_summary(self, filename: str, xml_content: str) -> Optional[Dict[str, Any]]:
        """
        Send summary document to SUNAT.
        
        Args:
            filename: XML filename
            xml_content: XML content
            
        Returns:
            Response dictionary or None if error
        """
        if not self.client:
            logger.error("SOAP client not initialized")
            return None
        
        try:
            # Compress XML content
            zip_content = self._compress_xml(filename, xml_content)
            if not zip_content:
                return None
            
            # Prepare parameters
            zip_filename = f"{filename}.zip"
            
            # Call SOAP service
            response = self.client.service.sendSummary(
                fileName=zip_filename,
                contentFile=zip_content
            )
            
            # Process response
            return self._process_summary_response(response)
            
        except Exception as e:
            logger.error(f"Error sending summary: {e}")
            return None
    
    def get_status(self, ticket: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Get status of submitted document.
        
        Args:
            ticket: Ticket ID from submission
            
        Returns:
            Status response or None if error
        """
        if not self.client or not ticket:
            logger.error("SOAP client not initialized or no ticket provided")
            return None
        
        try:
            # Call SOAP service
            response = self.client.service.getStatus(ticket=ticket)
            
            # Process response
            return self._process_status_response(response)
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return None
    
    def _compress_xml(self, filename: str, xml_content: str) -> Optional[bytes]:
        """
        Compress XML content to ZIP.
        
        Args:
            filename: XML filename
            xml_content: XML content
            
        Returns:
            Compressed ZIP bytes or None if error
        """
        try:
            # Create ZIP in memory
            zip_buffer = io.BytesIO()
            
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Add XML file to ZIP
                xml_filename = f"{filename}.xml"
                zip_file.writestr(xml_filename, xml_content.encode('utf-8'))
            
            # Get ZIP bytes and encode as base64
            zip_bytes = zip_buffer.getvalue()
            return base64.b64encode(zip_bytes)
            
        except Exception as e:
            logger.error(f"Error compressing XML: {e}")
            return None
    
    def _process_send_response(self, response) -> Dict[str, Any]:
        """
        Process send bill response.
        
        Args:
            response: SOAP response
            
        Returns:
            Processed response dictionary
        """
        result = {
            'success': False,
            'cdr_zip': None,
            'error': None
        }
        
        try:
            if hasattr(response, 'applicationResponse'):
                result['success'] = True
                result['cdr_zip'] = response.applicationResponse
            else:
                result['error'] = 'No application response received'
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _process_summary_response(self, response) -> Dict[str, Any]:
        """
        Process send summary response.
        
        Args:
            response: SOAP response
            
        Returns:
            Processed response dictionary
        """
        result = {
            'success': False,
            'ticket': None,
            'error': None
        }
        
        try:
            if hasattr(response, 'ticket'):
                result['success'] = True
                result['ticket'] = response.ticket
            else:
                result['error'] = 'No ticket received'
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _process_status_response(self, response) -> Dict[str, Any]:
        """
        Process get status response.
        
        Args:
            response: SOAP response
            
        Returns:
            Processed response dictionary
        """
        result = {
            'success': False,
            'status_code': None,
            'content': None,
            'error': None
        }
        
        try:
            if hasattr(response, 'status'):
                status = response.status
                result['success'] = True
                result['status_code'] = getattr(status, 'statusCode', None)
                result['content'] = getattr(status, 'content', None)
            else:
                result['error'] = 'No status received'
                
        except Exception as e:
            result['error'] = str(e)
        
        return result 