"""
Sale models including BaseSale and Invoice.
Migrated from packages/core/src/Core/Model/Sale/
"""

from datetime import datetime
from typing import List, Optional, Union
from pydantic import BaseModel, Field
from .document_interface import DocumentInterface
from .company import Company
from .client import Client


class SaleDetail(BaseModel):
    """
    Sale detail model for invoice line items.
    """
    
    cod_producto: Optional[str] = Field(alias="codProducto")
    unidad: Optional[str] = None
    cantidad: Optional[float] = None
    descripcion: Optional[str] = None
    mto_base_igv: Optional[float] = Field(alias="mtoBaseIgv")
    porcentaje_igv: Optional[float] = Field(alias="porcentajeIgv")
    igv: Optional[float] = None
    tip_afe_igv: Optional[str] = Field(alias="tipAfeIgv")
    total_impuestos: Optional[float] = Field(alias="totalImpuestos")
    mto_valor_venta: Optional[float] = Field(alias="mtoValorVenta")
    mto_valor_unitario: Optional[float] = Field(alias="mtoValorUnitario")
    mto_precio_unitario: Optional[float] = Field(alias="mtoPrecioUnitario")
    
    class Config:
        allow_population_by_field_name = True


class Legend(BaseModel):
    """
    Legend model for additional text information.
    """
    
    code: Optional[str] = None
    value: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True


class Document(BaseModel):
    """
    Document reference model.
    """
    
    tipo_doc: Optional[str] = Field(alias="tipoDoc")
    nro_doc: Optional[str] = Field(alias="nroDoc")
    
    class Config:
        allow_population_by_field_name = True


class PaymentTerms(BaseModel):
    """
    Payment terms model.
    """
    
    tipo: Optional[str] = None
    monto: Optional[float] = None
    
    class Config:
        allow_population_by_field_name = True


class Cuota(BaseModel):
    """
    Installment model for payment terms.
    """
    
    num: Optional[int] = None
    monto: Optional[float] = None
    fecha_pago: Optional[datetime] = Field(alias="fechaPago")
    
    class Config:
        allow_population_by_field_name = True


class Charge(BaseModel):
    """
    Charge model for additional charges.
    """
    
    cod_tipo: Optional[str] = Field(alias="codTipo")
    factor: Optional[float] = None
    monto: Optional[float] = None
    monto_base: Optional[float] = Field(alias="montoBase")
    
    class Config:
        allow_population_by_field_name = True


class SalePerception(BaseModel):
    """
    Sale perception model.
    """
    
    cod_reg: Optional[str] = Field(alias="codReg")
    tasa: Optional[float] = None
    monto: Optional[float] = None
    monto_base: Optional[float] = Field(alias="montoBase")
    
    class Config:
        allow_population_by_field_name = True


class Detraction(BaseModel):
    """
    Detraction model.
    """
    
    cod_bien_detraccion: Optional[str] = Field(alias="codBienDetraccion")
    cod_medio_pago: Optional[str] = Field(alias="codMedioPago")
    cta_financiera: Optional[str] = Field(alias="ctaFinanciera")
    percent: Optional[float] = None
    mount: Optional[float] = None
    
    class Config:
        allow_population_by_field_name = True


class Prepayment(BaseModel):
    """
    Prepayment model.
    """
    
    id: Optional[str] = None
    inst_id: Optional[str] = Field(alias="instId")
    total: Optional[float] = None
    
    class Config:
        allow_population_by_field_name = True


class EmbededDespatch(BaseModel):
    """
    Embedded dispatch model for invoice with embedded guide.
    """
    
    # This is a complex model that would need more detailed migration
    # For now, we'll create a basic structure
    pass


class BaseSale(BaseModel):
    """
    Base sale model that implements DocumentInterface.
    Migrated from packages/core/src/Core/Model/Sale/BaseSale.php
    """
    
    ubl_version: Optional[str] = Field(default="2.0", alias="ublVersion")
    tipo_doc: Optional[str] = Field(alias="tipoDoc")
    serie: Optional[str] = None
    correlativo: Optional[str] = None
    fecha_emision: Optional[datetime] = Field(alias="fechaEmision")
    company: Optional[Company] = None
    client: Optional[Client] = None
    tipo_moneda: Optional[str] = Field(alias="tipoMoneda")
    sum_otros_cargos: Optional[float] = Field(alias="sumOtrosCargos")
    mto_oper_gravadas: Optional[float] = Field(alias="mtoOperGravadas")
    mto_oper_inafectas: Optional[float] = Field(alias="mtoOperInafectas")
    mto_oper_exoneradas: Optional[float] = Field(alias="mtoOperExoneradas")
    mto_oper_exportacion: Optional[float] = Field(alias="mtoOperExportacion")
    mto_oper_gratuitas: Optional[float] = Field(alias="mtoOperGratuitas")
    mto_igv_gratuitas: Optional[float] = Field(alias="mtoIGVGratuitas")
    mto_igv: Optional[float] = Field(alias="mtoIGV")
    mto_base_ivap: Optional[float] = Field(alias="mtoBaseIvap")
    mto_ivap: Optional[float] = Field(alias="mtoIvap")
    mto_base_isc: Optional[float] = Field(alias="mtoBaseIsc")
    mto_isc: Optional[float] = Field(alias="mtoISC")
    mto_base_oth: Optional[float] = Field(alias="mtoBaseOth")
    mto_otros_tributos: Optional[float] = Field(alias="mtoOtrosTributos")
    icbper: Optional[float] = None
    total_impuestos: Optional[float] = Field(alias="totalImpuestos")
    redondeo: Optional[float] = None
    mto_imp_venta: Optional[float] = Field(alias="mtoImpVenta")
    details: Optional[List[SaleDetail]] = None
    legends: Optional[List[Legend]] = None
    guias: Optional[List[Document]] = None
    rel_docs: Optional[List[Document]] = Field(alias="relDocs")
    compra: Optional[str] = None
    forma_pago: Optional[PaymentTerms] = Field(alias="formaPago")
    cuotas: Optional[List[Cuota]] = None
    
    class Config:
        allow_population_by_field_name = True
        
    def get_name(self) -> str:
        """
        Implementation of DocumentInterface.get_name()
        """
        return f"{self.serie}-{self.correlativo}"


class Invoice(BaseSale):
    """
    Invoice model extending BaseSale.
    Migrated from packages/core/src/Core/Model/Sale/Invoice.php
    """
    
    tipo_operacion: Optional[str] = Field(alias="tipoOperacion")
    fec_vencimiento: Optional[datetime] = Field(alias="fecVencimiento")
    sum_dscto_global: Optional[float] = Field(alias="sumDsctoGlobal")
    mto_descuentos: Optional[float] = Field(alias="mtoDescuentos")
    sum_otros_descuentos: Optional[float] = Field(alias="sumOtrosDescuentos")
    descuentos: Optional[List[Charge]] = None
    cargos: Optional[List[Charge]] = None
    mto_cargos: Optional[float] = Field(alias="mtoCargos")
    total_anticipos: Optional[float] = Field(alias="totalAnticipos")
    perception: Optional[SalePerception] = None
    guia_embebida: Optional[EmbededDespatch] = Field(alias="guiaEmbebida")
    anticipos: Optional[List[Prepayment]] = None
    detraccion: Optional[Detraction] = None
    seller: Optional[Client] = None
    valor_venta: Optional[float] = Field(alias="valorVenta")
    sub_total: Optional[float] = Field(alias="subTotal")
    observacion: Optional[str] = None
    # direccion_entrega would be Address from company module
    
    class Config:
        allow_population_by_field_name = True 