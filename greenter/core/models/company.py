"""
Company and Address models.
Migrated from packages/core/src/Core/Model/Company/
"""

from typing import Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    """
    Address model for company and client addresses.
    Migrated from packages/core/src/Core/Model/Company/Address.php
    """
    
    ubigueo: Optional[str] = None
    codigo_pais: Optional[str] = Field(default="PE", alias="codigoPais")
    departamento: Optional[str] = None
    provincia: Optional[str] = None
    distrito: Optional[str] = None
    urbanizacion: Optional[str] = None
    direccion: Optional[str] = None
    cod_local: Optional[str] = Field(default="0000", alias="codLocal")
    
    class Config:
        allow_population_by_field_name = True
        
    def get_ubigueo(self) -> Optional[str]:
        return self.ubigueo
        
    def set_ubigueo(self, ubigueo: Optional[str]) -> "Address":
        self.ubigueo = ubigueo
        return self
        
    def get_codigo_pais(self) -> Optional[str]:
        return self.codigo_pais
        
    def set_codigo_pais(self, codigo_pais: Optional[str]) -> "Address":
        self.codigo_pais = codigo_pais
        return self
        
    def get_departamento(self) -> Optional[str]:
        return self.departamento
        
    def set_departamento(self, departamento: Optional[str]) -> "Address":
        self.departamento = departamento
        return self
        
    def get_provincia(self) -> Optional[str]:
        return self.provincia
        
    def set_provincia(self, provincia: Optional[str]) -> "Address":
        self.provincia = provincia
        return self
        
    def get_distrito(self) -> Optional[str]:
        return self.distrito
        
    def set_distrito(self, distrito: Optional[str]) -> "Address":
        self.distrito = distrito
        return self
        
    def get_urbanizacion(self) -> Optional[str]:
        return self.urbanizacion
        
    def set_urbanizacion(self, urbanizacion: Optional[str]) -> "Address":
        self.urbanizacion = urbanizacion
        return self
        
    def get_direccion(self) -> Optional[str]:
        return self.direccion
        
    def set_direccion(self, direccion: Optional[str]) -> "Address":
        self.direccion = direccion
        return self
        
    def get_cod_local(self) -> Optional[str]:
        return self.cod_local
        
    def set_cod_local(self, cod_local: Optional[str]) -> "Address":
        self.cod_local = cod_local
        return self


class Company(BaseModel):
    """
    Company model for invoice issuer information.
    Migrated from packages/core/src/Core/Model/Company/Company.php
    """
    
    ruc: Optional[str] = None
    razon_social: Optional[str] = Field(alias="razonSocial")
    nombre_comercial: Optional[str] = Field(alias="nombreComercial")
    address: Optional[Address] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    
    class Config:
        allow_population_by_field_name = True
        
    def get_ruc(self) -> Optional[str]:
        return self.ruc
        
    def set_ruc(self, ruc: Optional[str]) -> "Company":
        self.ruc = ruc
        return self
        
    def get_razon_social(self) -> Optional[str]:
        return self.razon_social
        
    def set_razon_social(self, razon_social: Optional[str]) -> "Company":
        self.razon_social = razon_social
        return self
        
    def get_nombre_comercial(self) -> Optional[str]:
        return self.nombre_comercial
        
    def set_nombre_comercial(self, nombre_comercial: Optional[str]) -> "Company":
        self.nombre_comercial = nombre_comercial
        return self
        
    def get_address(self) -> Optional[Address]:
        return self.address
        
    def set_address(self, address: Optional[Address]) -> "Company":
        self.address = address
        return self
        
    def get_email(self) -> Optional[str]:
        return self.email
        
    def set_email(self, email: Optional[str]) -> "Company":
        self.email = email
        return self
        
    def get_telephone(self) -> Optional[str]:
        return self.telephone
        
    def set_telephone(self, telephone: Optional[str]) -> "Company":
        self.telephone = telephone
        return self 