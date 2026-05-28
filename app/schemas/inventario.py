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