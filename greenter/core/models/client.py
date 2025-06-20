"""
Client model.
Migrated from packages/core/src/Core/Model/Client/Client.php
"""

from typing import Optional
from pydantic import BaseModel, Field
from .company import Address


class Client(BaseModel):
    """
    Client model for invoice recipient information.
    Migrated from packages/core/src/Core/Model/Client/Client.php
    """
    
    tipo_doc: Optional[str] = Field(alias="tipoDoc")
    num_doc: Optional[str] = Field(alias="numDoc")
    rzn_social: Optional[str] = Field(alias="rznSocial")
    address: Optional[Address] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        
    def get_tipo_doc(self) -> Optional[str]:
        return self.tipo_doc
        
    def set_tipo_doc(self, tipo_doc: Optional[str]) -> "Client":
        self.tipo_doc = tipo_doc
        return self
        
    def get_num_doc(self) -> Optional[str]:
        return self.num_doc
        
    def set_num_doc(self, num_doc: Optional[str]) -> "Client":
        self.num_doc = num_doc
        return self
        
    def get_rzn_social(self) -> Optional[str]:
        return self.rzn_social
        
    def set_rzn_social(self, rzn_social: Optional[str]) -> "Client":
        self.rzn_social = rzn_social
        return self
        
    def get_address(self) -> Optional[Address]:
        return self.address
        
    def set_address(self, address: Optional[Address]) -> "Client":
        self.address = address
        return self
        
    def get_email(self) -> Optional[str]:
        return self.email
        
    def set_email(self, email: Optional[str]) -> "Client":
        self.email = email
        return self
        
    def get_telephone(self) -> Optional[str]:
        return self.telephone
        
    def set_telephone(self, telephone: Optional[str]) -> "Client":
        self.telephone = telephone
        return self 