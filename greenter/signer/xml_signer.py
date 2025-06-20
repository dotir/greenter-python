"""
XML Digital Signer using xmlsec.
Migrated from packages/xmldsig functionality.
"""

from typing import Optional
import logging
import tempfile
import os
from pathlib import Path

try:
    import xmlsec
    import lxml.etree as etree
    XMLSEC_AVAILABLE = True
except ImportError:
    XMLSEC_AVAILABLE = False
    logging.warning("xmlsec not available. XML signing will not work.")


logger = logging.getLogger(__name__)


class XmlSigner:
    """
    XML Digital Signer for SUNAT documents.
    """
    
    def __init__(self):
        """Initialize XML signer."""
        self.certificate_path: Optional[str] = None
        self.private_key_path: Optional[str] = None
        self.certificate_content: Optional[str] = None
        
        if not XMLSEC_AVAILABLE:
            logger.warning("xmlsec not available. XML signing disabled.")
    
    def set_certificate(self, certificate: str):
        """
        Set certificate for signing.
        
        Args:
            certificate: Certificate content or file path
        """
        if os.path.isfile(certificate):
            # It's a file path
            self.certificate_path = certificate
            with open(certificate, 'r') as f:
                self.certificate_content = f.read()
        else:
            # It's certificate content
            self.certificate_content = certificate
            # Save to temporary file for xmlsec
            self._save_certificate_to_temp()
    
    def set_private_key(self, private_key_path: str):
        """
        Set private key path.
        
        Args:
            private_key_path: Path to private key file
        """
        self.private_key_path = private_key_path
    
    def sign(self, xml_content: str) -> Optional[str]:
        """
        Sign XML content.
        
        Args:
            xml_content: XML content to sign
            
        Returns:
            Signed XML content or None if error
        """
        if not XMLSEC_AVAILABLE:
            logger.warning("xmlsec not available. Returning unsigned XML.")
            return xml_content
        
        if not self.certificate_path:
            logger.error("No certificate configured")
            return None
        
        try:
            # Parse XML
            doc = etree.fromstring(xml_content.encode('utf-8'))
            
            # Find signature placeholder
            signature_node = self._find_signature_placeholder(doc)
            if signature_node is None:
                logger.error("No signature placeholder found in XML")
                return None
            
            # Create signature template
            signature = self._create_signature_template(doc, signature_node)
            
            # Sign the document
            signed_doc = self._sign_document(doc, signature)
            if signed_doc is None:
                return None
            
            # Return signed XML
            return etree.tostring(signed_doc, encoding='unicode', pretty_print=True)
            
        except Exception as e:
            logger.error(f"Error signing XML: {e}")
            return None
    
    def _save_certificate_to_temp(self):
        """Save certificate content to temporary file."""
        if not self.certificate_content:
            return
        
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as f:
                f.write(self.certificate_content)
                self.certificate_path = f.name
                
        except Exception as e:
            logger.error(f"Error saving certificate to temp file: {e}")
    
    def _find_signature_placeholder(self, doc):
        """
        Find signature placeholder in XML document.
        
        Args:
            doc: XML document
            
        Returns:
            Signature node or None
        """
        # Look for UBLExtensions/UBLExtension/ExtensionContent
        namespaces = {
            'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
        
        # Find extension content for signature
        ext_content = doc.xpath('//ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent', 
                               namespaces=namespaces)
        
        if ext_content:
            return ext_content[0]
        
        return None
    
    def _create_signature_template(self, doc, signature_node):
        """
        Create signature template.
        
        Args:
            doc: XML document
            signature_node: Node where signature will be placed
            
        Returns:
            Signature template
        """
        # This is a simplified signature template
        # In a real implementation, you would create a proper XML signature template
        # following the XML Digital Signature standard
        
        signature_template = '''
        <ds:Signature xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Id="SignatureKG">
            <ds:SignedInfo>
                <ds:CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
                <ds:SignatureMethod Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1"/>
                <ds:Reference URI="">
                    <ds:Transforms>
                        <ds:Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
                    </ds:Transforms>
                    <ds:DigestMethod Algorithm="http://www.w3.org/2000/09/xmldsig#sha1"/>
                    <ds:DigestValue></ds:DigestValue>
                </ds:Reference>
            </ds:SignedInfo>
            <ds:SignatureValue></ds:SignatureValue>
            <ds:KeyInfo>
                <ds:X509Data>
                    <ds:X509Certificate></ds:X509Certificate>
                </ds:X509Data>
            </ds:KeyInfo>
        </ds:Signature>
        '''
        
        return etree.fromstring(signature_template)
    
    def _sign_document(self, doc, signature_template):
        """
        Sign the document using xmlsec.
        
        Args:
            doc: XML document
            signature_template: Signature template
            
        Returns:
            Signed document or None if error
        """
        if not XMLSEC_AVAILABLE:
            return None
        
        try:
            # This is a placeholder for actual xmlsec signing
            # In a real implementation, you would:
            # 1. Initialize xmlsec library
            # 2. Load certificate and private key
            # 3. Create signature context
            # 4. Sign the document
            # 5. Return signed document
            
            # For now, just return the original document
            # This would need proper xmlsec implementation
            logger.warning("XML signing not fully implemented. Returning unsigned document.")
            return doc
            
        except Exception as e:
            logger.error(f"Error in xmlsec signing: {e}")
            return None
    
    def __del__(self):
        """Cleanup temporary files."""
        if (self.certificate_path and 
            self.certificate_path.startswith(tempfile.gettempdir())):
            try:
                os.unlink(self.certificate_path)
            except:
                pass 