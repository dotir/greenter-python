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
from zeep.exceptions import Fault as ZeepFault
from requests import Session
from requests.auth import HTTPBasicAuth


logger = logging.getLogger(__name__)


class SunatEndpoints:
    """
    SUNAT service endpoints.
    Migrated from packages/ws/src/Ws/Services/SunatEndpoints.php
    
    ⚠️  CONFIGURADO SOLO PARA HOMOLOGACIÓN/PRUEBAS
    """
    
    # FACTURACION SERVICES - HOMOLOGACIÓN/PRUEBAS
    FE_BETA = 'https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService'
    FE_HOMOLOGACION = 'https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService'
    
    # PRODUCCIÓN COMENTADO POR SEGURIDAD:
    # FE_PRODUCCION = 'https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService'
    # FE_CONSULTA_CDR = 'https://e-factura.sunat.gob.pe/ol-it-wsconscpegem/billConsultService'
    
    # GUIA DE REMISION SERVICES - SOLO PRUEBAS
    GUIA_BETA = 'https://e-beta.sunat.gob.pe/ol-ti-itemision-guia-gem-beta/billService'
    # GUIA_PRODUCCION = 'https://e-guiaremision.sunat.gob.pe/ol-ti-itemision-guia-gem/billService'
    
    # RETENCION Y PERCEPCION SERVICES - SOLO PRUEBAS
    RETENCION_BETA = 'https://e-beta.sunat.gob.pe/ol-ti-itemision-otroscpe-gem-beta/billService'
    # RETENCION_PRODUCCION = 'https://e-factura.sunat.gob.pe/ol-ti-itemision-otroscpe-gem/billService'
    
    # WSDL Uri - HOMOLOGACIÓN
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
            print("⚠️  No credentials provided for SOAP client")
            return
        
        try:
            # For SUNAT, try without authentication for WSDL first
            # Authentication is only needed for service calls
            transport = Transport(session=Session())
            
            # Use service URL for WSDL if available, otherwise use default
            # Try different WSDL URL formats
            if self.service_url:
                wsdl_url = f"{self.service_url}?wsdl"
            else:
                wsdl_url = SunatEndpoints.WSDL_ENDPOINT
            
            # Create SOAP client with WSDL
            self.client = Client(wsdl_url, transport=transport)
            
            # Setup WSSE authentication for service calls
            wsse = UsernameToken(self.username, self.password)
            self.client.wsse = wsse
            
            logger.info(f"SOAP client initialized successfully for service: {self.service_url or 'default'}")
            print(f"✅ SOAP client initialized successfully")
            
        except Exception as e:
            logger.error(f"Error setting up SOAP client: {e}")
            print(f"Error setting up SOAP client: {e}")
            
            # Try fallback with different WSDL approaches
            try:
                logger.info("Trying fallback WSDL approaches...")
                print("⚠️  Trying fallback approaches...")
                
                # List of WSDL URLs to try (SOLO HOMOLOGACIÓN/PRUEBAS)
                fallback_wsdls = [
                    SunatEndpoints.WSDL_ENDPOINT,  # Default with ?wsdl
                    f"{self.service_url}?wsdl" if self.service_url else None,
                    "https://e-beta.sunat.gob.pe/ol-ti-itcpfegem-beta/billService?wsdl",
                    "https://www.sunat.gob.pe/ol-ti-itcpgem-sqa/billService?wsdl"
                    # PRODUCCIÓN COMENTADO POR SEGURIDAD:
                    # "https://e-factura.sunat.gob.pe/ol-ti-itcpfegem/billService?wsdl"
                ]
                
                # Remove None values
                fallback_wsdls = [url for url in fallback_wsdls if url]
                
                for i, fallback_wsdl in enumerate(fallback_wsdls):
                    try:
                        print(f"   Probando WSDL {i+1}/{len(fallback_wsdls)}: {fallback_wsdl}")
                        
                        transport = Transport(session=Session())
                        self.client = Client(fallback_wsdl, transport=transport)
                        
                        # Setup WSSE authentication for service calls
                        wsse = UsernameToken(self.username, self.password)
                        self.client.wsse = wsse
                        
                        # Set service URL if provided
                        if self.service_url:
                            try:
                                binding = self.client.service._binding
                                binding.address = self.service_url
                            except:
                                # If binding modification fails, continue anyway
                                pass
                        
                        logger.info(f"SOAP client initialized with fallback WSDL: {fallback_wsdl}")
                        print(f"✅ SOAP client initialized with WSDL: {fallback_wsdl}")
                        return  # Success, exit the method
                        
                    except Exception as fallback_error:
                        print(f"   ❌ Falló WSDL {i+1}: {fallback_error}")
                        continue
                
                # If we get here, all fallbacks failed
                logger.error("All fallback WSDLs failed")
                print("❌ Todos los WSDLs de fallback fallaron")
                self.client = None
                
            except Exception as e2:
                logger.error(f"Fallback process failed: {e2}")
                print(f"❌ Proceso de fallback falló: {e2}")
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
            print("❌ SOAP client not initialized in send()")
            return None
        
        try:
            print(f"🔧 Preparando envío: {filename}")
            
            # Compress XML content
            zip_content = self._compress_xml(filename, xml_content)
            if not zip_content:
                print("❌ Error comprimiendo XML")
                return None
            
            print(f"✅ XML comprimido: {len(zip_content)} bytes")
            
            # Prepare parameters
            zip_filename = f"{filename}.zip"
            
            print(f"📤 Enviando a SUNAT: {zip_filename}")
            
            # Call SOAP service
            try:
                response = self.client.service.sendBill(
                    fileName=zip_filename,
                    contentFile=zip_content
                )
                
                print(f"📨 Respuesta recibida: {type(response)}")
                
                # Process response
                result = self._process_send_response(response)
                print(f"📋 Respuesta procesada: {result}")
                
                return result
                
            except ZeepFault as zeep_fault:
                print(f"❌ ZeepFault detectado: {zeep_fault}")
                print(f"❌ Código: {zeep_fault.code}")
                print(f"❌ Mensaje: {zeep_fault.message}")
                print(f"❌ Detalle: {zeep_fault.detail}")
                
                error_info = {
                    'success': False,
                    'error': f"SUNAT Fault {zeep_fault.code}: {zeep_fault.message}",
                    'code': zeep_fault.code,
                    'description': zeep_fault.message,
                    'detail': str(zeep_fault.detail) if zeep_fault.detail else None
                }
                
                return error_info
                
            except Exception as soap_error:
                print(f"❌ Error en llamada SOAP: {soap_error}")
                print(f"❌ Tipo de error: {type(soap_error)}")
                
                # Intentar extraer información útil del error
                error_info = {
                    'success': False,
                    'error': str(soap_error),
                    'code': None,
                    'description': None
                }
                
                # Manejo específico para zeep.exceptions.Fault
                if hasattr(soap_error, 'code') and hasattr(soap_error, 'message'):
                    error_info['code'] = soap_error.code
                    error_info['description'] = soap_error.message
                    error_info['error'] = f"SOAP Fault {soap_error.code}: {soap_error.message}"
                    print(f"🔍 Zeep Fault Code: {soap_error.code}")
                    print(f"🔍 Zeep Fault Message: {soap_error.message}")
                
                # Si es un error de SOAP Fault estándar, extraer detalles
                elif hasattr(soap_error, 'fault'):
                    fault = soap_error.fault
                    error_info['code'] = getattr(fault, 'faultcode', None)
                    error_info['description'] = getattr(fault, 'faultstring', None)
                    error_info['error'] = f"SOAP Fault {error_info['code']}: {error_info['description']}"
                    print(f"🔍 SOAP Fault Code: {error_info['code']}")
                    print(f"🔍 SOAP Fault String: {error_info['description']}")
                
                # Intentar obtener más detalles del error
                print(f"🔍 Atributos del error: {dir(soap_error)}")
                
                # Intentar obtener detalles específicos de zeep
                if hasattr(soap_error, 'detail'):
                    print(f"🔍 Detail: {soap_error.detail}")
                    error_info['detail'] = str(soap_error.detail)
                
                if hasattr(soap_error, 'args') and soap_error.args:
                    print(f"🔍 Args: {soap_error.args}")
                    if len(soap_error.args) > 0:
                        error_info['error'] = str(soap_error.args[0])
                
                return error_info
            
        except Exception as e:
            logger.error(f"Error sending document: {e}")
            print(f"❌ Error enviando documento: {e}")
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
            'cdr_response': None,
            'error': None,
            'code': None,
            'description': None
        }
        
        try:
            print(f"🔍 Analizando respuesta SOAP: {response}")
            print(f"🔍 Tipo de respuesta: {type(response)}")
            print(f"🔍 Atributos disponibles: {dir(response) if response else 'None'}")
            
            if response is None:
                result['error'] = 'Respuesta SOAP es None'
                return result
            
            # Intentar diferentes formatos de respuesta SUNAT
            if hasattr(response, 'applicationResponse'):
                print("✅ Encontrado applicationResponse")
                result['success'] = True
                result['cdr_zip'] = response.applicationResponse
                
                # Decodificar CDR si está en base64
                if result['cdr_zip']:
                    try:
                        import base64
                        cdr_decoded = base64.b64decode(result['cdr_zip'])
                        result['cdr_response'] = cdr_decoded.decode('utf-8', errors='ignore')
                        print(f"✅ CDR decodificado: {len(result['cdr_response'])} caracteres")
                    except Exception as decode_error:
                        print(f"⚠️  Error decodificando CDR: {decode_error}")
                        
            elif hasattr(response, 'status'):
                print("✅ Encontrado status")
                status = response.status
                result['code'] = getattr(status, 'statusCode', None)
                result['description'] = getattr(status, 'content', None)
                
                if result['code'] == '0':
                    result['success'] = True
                else:
                    result['error'] = f"SUNAT Error {result['code']}: {result['description']}"
                    
            elif hasattr(response, 'faultcode') or hasattr(response, 'faultstring'):
                print("❌ Encontrado SOAP Fault")
                result['error'] = f"SOAP Fault: {getattr(response, 'faultstring', 'Unknown fault')}"
                result['code'] = getattr(response, 'faultcode', None)
                
            else:
                print("⚠️  Formato de respuesta desconocido")
                result['error'] = f'Formato de respuesta desconocido: {str(response)[:200]}'
                
        except Exception as e:
            print(f"❌ Error procesando respuesta: {e}")
            result['error'] = f'Error procesando respuesta: {str(e)}'
        
        print(f"📋 Resultado procesado: {result}")
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