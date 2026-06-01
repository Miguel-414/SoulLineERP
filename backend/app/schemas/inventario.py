"""
Schemas de Pydantic para el módulo de inventario.

¿Para qué sirven los schemas?
- Validan los datos que entran (body de un POST/PUT)
- Definen la forma de los datos que salen (respuesta de la API)
- Son independientes de los modelos de SQLAlchemy

Convención de nombres:
  - XxxBase    → campos comunes (sin id, sin fechas automáticas)
  - XxxCreate  → lo que el cliente manda para crear
  - XxxUpdate  → lo que el cliente manda para actualizar (campos opcionales)
  - XxxRead    → lo que la API devuelve
"""

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.inventario import EstadoFisicoEnum, EstadoFuncionalEnum, TipoObjetoEnum


# ── TipoActivo ────────────────────────────────────────────────────────────────

class TipoActivoBase(BaseModel):
    nombre: str
    descripcion: str


class TipoActivoCreate(TipoActivoBase):
    pass


class TipoActivoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class TipoActivoRead(TipoActivoBase):
    id_tipo_activo: int
    model_config = ConfigDict(from_attributes=True)


# ── Objeto ────────────────────────────────────────────────────────────────────

class ObjetoBase(BaseModel):
    tipo_objeto: TipoObjetoEnum
    nombre: str
    descripcion: str
    marca: Optional[str] = None
    modelo: Optional[str] = None
    id_tipo_activo: int


class ObjetoCreate(ObjetoBase):
    pass


class ObjetoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None


class ObjetoRead(ObjetoBase):
    id_objeto: int
    model_config = ConfigDict(from_attributes=True)


# ── ItemSerializado ───────────────────────────────────────────────────────────

class ItemSerializadoBase(BaseModel):
    id_objeto: int
    serie: Optional[str] = None
    placa_activo: str
    estado_funcional: EstadoFuncionalEnum
    estado_fisico: EstadoFisicoEnum
    fecha_adquisicion: date
    fecha_puesto_servicio: Optional[date] = None
    n_garantia: Optional[str] = None
    fecha_inicio_garantia: Optional[date] = None
    fecha_fin_garantia: Optional[date] = None


class ItemSerializadoCreate(ItemSerializadoBase):
    pass


class ItemSerializadoUpdate(BaseModel):
    estado_funcional: Optional[EstadoFuncionalEnum] = None
    estado_fisico: Optional[EstadoFisicoEnum] = None
    fecha_puesto_servicio: Optional[date] = None
    n_garantia: Optional[str] = None
    fecha_inicio_garantia: Optional[date] = None
    fecha_fin_garantia: Optional[date] = None


class ItemSerializadoRead(ItemSerializadoBase):
    id_item_serializado: int
    fecha_registro: datetime
    model_config = ConfigDict(from_attributes=True)


# ── Ubicacion ─────────────────────────────────────────────────────────────────

class UbicacionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    id_zona_padre: Optional[int] = None


class UbicacionCreate(UbicacionBase):
    pass


class UbicacionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class UbicacionRead(UbicacionBase):
    id_ubicacion: int
    model_config = ConfigDict(from_attributes=True)


# ── ObjetoAcumulable ──────────────────────────────────────────────────────────

class ObjetoAcumulableBase(BaseModel):
    id_objeto: int
    cantidad: int
    fecha_adquisicion: Optional[date] = None
    forma_adquisicion: Optional[str] = None
    id_factura: Optional[int] = None


class ObjetoAcumulableCreate(ObjetoAcumulableBase):
    pass


class ObjetoAcumulableUpdate(BaseModel):
    cantidad: Optional[int] = None
    fecha_adquisicion: Optional[date] = None
    forma_adquisicion: Optional[str] = None
    id_factura: Optional[int] = None


class ObjetoAcumulableRead(ObjetoAcumulableBase):
    id_objeto_acumulable: int
    fecha_registro: datetime
    model_config = ConfigDict(from_attributes=True)
# ── Inventario ────────────────────────────────────────────────────────────────


class InventarioBase(BaseModel):
    id_objeto: int
    id_item_serializado: Optional[int] = None
    cantidad_actual: int
    id_ubicacion: int
    estado_actual: EstadoFuncionalEnum
    fecha_ultima_actualizacion: datetime


class InventarioCreate(InventarioBase):
    pass


class InventarioUpdate(BaseModel):
    cantidad_actual: Optional[int] = None
    estado_actual: Optional[EstadoFuncionalEnum] = None
    id_ubicacion: Optional[int] = None
    fecha_ultima_actualizacion: Optional[datetime] = None


class InventarioRead(InventarioBase):
    id_inventario: int
    model_config = ConfigDict(from_attributes=True)


# ── TipoMovimiento ────────────────────────────────────────────────────────

class TipoMovimientoBase(BaseModel):
    nombre: str
    descripcion: str


class TipoMovimientoCreate(TipoMovimientoBase):
    pass


class TipoMovimientoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class TipoMovimientoRead(TipoMovimientoBase):
    id_tipo_movimiento: int
    model_config = ConfigDict(from_attributes=True)


# ── Movimiento ────────────────────────────────────────────────────────────

class MovimientoBase(BaseModel):
    fecha_movimiento: date
    id_tipo_movimiento: int


class MovimientoCreate(MovimientoBase):
    pass


class MovimientoUpdate(BaseModel):
    fecha_movimiento: Optional[date] = None
    id_tipo_movimiento: Optional[int] = None


class MovimientoRead(MovimientoBase):
    id_movimiento: int
    model_config = ConfigDict(from_attributes=True)


# ── DetalleMovimiento ─────────────────────────────────────────────────────

class DetalleMovimientoBase(BaseModel):
    id_movimiento: int
    id_objeto: int
    id_item_serializado: Optional[int] = None
    id_inventario_origen: Optional[int] = None
    id_inventario_destino: Optional[int] = None
    id_ubicacion_origen: Optional[int] = None
    id_ubicacion_destino: int
    cantidad_afectada: int
    observaciones: Optional[str] = None


class DetalleMovimientoCreate(DetalleMovimientoBase):
    pass


class DetalleMovimientoUpdate(BaseModel):
    id_ubicacion_destino: Optional[int] = None
    cantidad_afectada: Optional[int] = None
    observaciones: Optional[str] = None


class DetalleMovimientoRead(DetalleMovimientoBase):
    id_detalle_movimiento: int
    model_config = ConfigDict(from_attributes=True)
