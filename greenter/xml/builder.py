"""
XML Builder using Jinja2 templates.
Migrated from packages/xml/src/Xml/Builder/
"""

from typing import Dict, Any, Optional
import logging
from jinja2 import Environment, FileSystemLoader, DictLoader, select_autoescape
from pathlib import Path

from ..core.models.document_interface import DocumentInterface


logger = logging.getLogger(__name__)


class XmlBuilder:
    """
    XML Builder using Jinja2 templates.
    Generates XML documents from Python objects.
    """
    
    def __init__(self, options: Dict[str, Any] = None):
        """
        Initialize XML Builder.
        
        Args:
            options: Jinja2 environment options
        """
        self.options = options or {}
        self.env: Optional[Environment] = None
        self._setup_environment()
    
    def _setup_environment(self):
        """Setup Jinja2 environment with appropriate settings."""
        try:
            # Determine template loader
            template_dir = self.options.get('template_dir', self._get_default_template_dir())
            
            if isinstance(template_dir, str) and Path(template_dir).exists():
                loader = FileSystemLoader(template_dir)
            else:
                # Use built-in templates
                loader = DictLoader(self._get_default_templates())
            
            # Create environment
            self.env = Environment(
                loader=loader,
                autoescape=select_autoescape(['html', 'xml']) if self.options.get('autoescape', False) else False,
                cache_size=0 if not self.options.get('cache', False) else 400,
                auto_reload=True
            )
            
            # Add custom filters
            self._add_custom_filters()
            
        except Exception as e:
            logger.error(f"Error setting up Jinja2 environment: {e}")
            raise
    
    def _get_default_template_dir(self) -> str:
        """Get default template directory."""
        current_dir = Path(__file__).parent
        return str(current_dir / "templates")
    
    def _get_default_templates(self) -> Dict[str, str]:
        """Get default templates as dictionary."""
        return {
            'invoice.xml': self._get_invoice_template(),
            'note.xml': self._get_note_template(),
            'despatch.xml': self._get_despatch_template(),
        }
    
    def _add_custom_filters(self):
        """Add custom Jinja2 filters for XML generation."""
        if not self.env:
            return
        
        def format_currency(value: float, decimals: int = 2) -> str:
            """Format currency with specified decimals."""
            if value is None:
                return "0.00"
            return f"{value:.{decimals}f}"
        
        def format_date(date_obj, format_str: str = "%Y-%m-%d") -> str:
            """Format date object."""
            if date_obj is None:
                return ""
            return date_obj.strftime(format_str)
        
        def format_datetime(datetime_obj, format_str: str = "%Y-%m-%dT%H:%M:%S") -> str:
            """Format datetime object."""
            if datetime_obj is None:
                return ""
            return datetime_obj.strftime(format_str)
        
        # Register filters
        self.env.filters['currency'] = format_currency
        self.env.filters['date'] = format_date
        self.env.filters['datetime'] = format_datetime
    
    def update_options(self, options: Dict[str, Any]):
        """
        Update builder options and recreate environment.
        
        Args:
            options: New options to merge
        """
        self.options.update(options)
        self._setup_environment()
    
    def build(self, document: DocumentInterface) -> Optional[str]:
        """
        Build XML from document.
        
        Args:
            document: Document to convert to XML
            
        Returns:
            XML string or None if error
        """
        if not self.env:
            logger.error("Jinja2 environment not initialized")
            return None
        
        try:
            # Determine template name based on document type
            template_name = self._get_template_name(document)
            
            # Get template
            template = self.env.get_template(template_name)
            
            # Convert document to dictionary for template rendering
            context = self._document_to_dict(document)
            
            # Render template
            xml_content = template.render(**context)
            
            return xml_content
            
        except Exception as e:
            logger.error(f"Error building XML: {e}")
            return None
    
    def _get_template_name(self, document: DocumentInterface) -> str:
        """
        Get template name for document type.
        
        Args:
            document: Document instance
            
        Returns:
            Template filename
        """
        # Map document types to templates
        doc_type = type(document).__name__.lower()
        
        template_map = {
            'invoice': 'invoice.xml',
            'note': 'note.xml',
            'despatch': 'despatch.xml',
            'summary': 'summary.xml',
            'voided': 'voided.xml',
        }
        
        return template_map.get(doc_type, 'invoice.xml')
    
    def _document_to_dict(self, document: DocumentInterface) -> Dict[str, Any]:
        """
        Convert document to dictionary for template rendering.
        
        Args:
            document: Document instance
            
        Returns:
            Dictionary representation
        """
        try:
            # If using Pydantic models, use dict() method
            if hasattr(document, 'dict'):
                return {'doc': document.dict(by_alias=True)}
            
            # Fallback to manual conversion
            return {'doc': self._object_to_dict(document)}
            
        except Exception as e:
            logger.error(f"Error converting document to dict: {e}")
            return {'doc': {}}
    
    def _object_to_dict(self, obj: Any) -> Dict[str, Any]:
        """
        Convert object to dictionary recursively.
        
        Args:
            obj: Object to convert
            
        Returns:
            Dictionary representation
        """
        if hasattr(obj, '__dict__'):
            result = {}
            for key, value in obj.__dict__.items():
                if not key.startswith('_'):
                    result[key] = self._object_to_dict(value) if hasattr(value, '__dict__') else value
            return result
        return obj
    
    def _get_invoice_template(self) -> str:
        """Get basic invoice template."""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
         xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2">
    <ext:UBLExtensions>
        <ext:UBLExtension>
            <ext:ExtensionContent>
                <!-- Digital signature will be added here -->
            </ext:ExtensionContent>
        </ext:UBLExtension>
    </ext:UBLExtensions>
    <cbc:UBLVersionID>{{ doc.ublVersion or "2.1" }}</cbc:UBLVersionID>
    <cbc:CustomizationID>2.0</cbc:CustomizationID>
    <cbc:ID>{{ doc.serie }}-{{ doc.correlativo }}</cbc:ID>
    <cbc:IssueDate>{{ doc.fechaEmision | date }}</cbc:IssueDate>
    <cbc:InvoiceTypeCode>{{ doc.tipoDoc }}</cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode>{{ doc.tipoMoneda or "PEN" }}</cbc:DocumentCurrencyCode>
    
    {% if doc.company %}
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="6">{{ doc.company.ruc }}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>{{ doc.company.razonSocial }}</cbc:Name>
            </cac:PartyName>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{{ doc.company.razonSocial }}</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>
    {% endif %}
    
    {% if doc.client %}
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyIdentification>
                <cbc:ID schemeID="{{ doc.client.tipoDoc }}">{{ doc.client.numDoc }}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{{ doc.client.rznSocial }}</cbc:RegistrationName>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>
    {% endif %}
    
    <!-- Invoice lines would go here -->
    
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="{{ doc.tipoMoneda or 'PEN' }}">{{ doc.mtoOperGravadas | currency }}</cbc:LineExtensionAmount>
        <cbc:TaxInclusiveAmount currencyID="{{ doc.tipoMoneda or 'PEN' }}">{{ doc.mtoImpVenta | currency }}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="{{ doc.tipoMoneda or 'PEN' }}">{{ doc.mtoImpVenta | currency }}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
</Invoice>'''
    
    def _get_note_template(self) -> str:
        """Get basic note template."""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Credit/Debit Note template -->
<CreditNote xmlns="urn:oasis:names:specification:ubl:schema:xsd:CreditNote-2">
    <!-- Note template content -->
</CreditNote>'''
    
    def _get_despatch_template(self) -> str:
        """Get basic despatch template."""
        return '''<?xml version="1.0" encoding="UTF-8"?>
<!-- Despatch Advice template -->
<DespatchAdvice xmlns="urn:oasis:names:specification:ubl:schema:xsd:DespatchAdvice-2">
    <!-- Despatch template content -->
</DespatchAdvice>''' 