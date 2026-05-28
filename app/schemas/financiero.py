from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ── Proveedor ─────────────────────────────────────────────────────────────────

class ProveedorBase(BaseModel):
    nit: str
    razon_social: str
    email: EmailStr
    telefono: str
    direccion: str

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(BaseModel):
    razon_social: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorRead(ProveedorBase):
    id_proveedor: int
    model_config = ConfigDict(from_attributes=True)


# ── Factura ───────────────────────────────────────────────────────────────────

class FacturaBase(BaseModel):
    fecha_generacion: datetime
    id_proveedor: int
    total_bruto: Decimal
    iva: Optional[Decimal] = Decimal("0")
    valor_iva: Optional[Decimal] = Decimal("0")
    retencion_fuente: Optional[Decimal] = Decimal("0")
    descuento: Optional[Decimal] = Decimal("0")
    valor_total: Decimal

class FacturaCreate(FacturaBase):
    pass

class FacturaUpdate(BaseModel):
    total_bruto: Optional[Decimal] = None
    iva: Optional[Decimal] = None
    valor_iva: Optional[Decimal] = None
    retencion_fuente: Optional[Decimal] = None
    descuento: Optional[Decimal] = None
    valor_total: Optional[Decimal] = None

class FacturaRead(FacturaBase):
    id_factura: int
    model_config = ConfigDict(from_attributes=True)


# ── DetalleFactura ────────────────────────────────────────────────────────────

class DetalleFacturaBase(BaseModel):
    id_factura: int
    id_objeto: int
    id_item_serializado: Optional[int] = None
    descripcion_factura: str
    cantidad: int
    precio_unitario: Decimal
    valor_bruto: Decimal
    tasa_impuesto: Decimal = Decimal("0")
    valor_impto_cargo: Decimal
    descuento: Decimal = Decimal("0")
    valor_total: Decimal

class DetalleFacturaCreate(DetalleFacturaBase):
    pass

class DetalleFacturaRead(DetalleFacturaBase):
    id_detalle_factura: int
    model_config = ConfigDict(from_attributes=True)