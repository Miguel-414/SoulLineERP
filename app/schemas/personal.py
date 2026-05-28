from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


# ── Persona ───────────────────────────────────────────────────────────────────

class PersonaBase(BaseModel):
    primer_nombre: str
    segundo_nombre: Optional[str] = None
    primer_apellido: str
    segundo_apellido: Optional[str] = None
    nombre: str
    email: EmailStr
    direccion: str
    telefono: str

class PersonaCreate(PersonaBase):
    pass

class PersonaUpdate(BaseModel):
    segundo_nombre: Optional[str] = None
    segundo_apellido: Optional[str] = None
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None

class PersonaRead(PersonaBase):
    id_persona: int
    fecha_registro: datetime
    model_config = ConfigDict(from_attributes=True)


# ── ResponsableObjeto ─────────────────────────────────────────────────────────

class ResponsableObjetoBase(BaseModel):
    id_inventario: int
    id_persona: int
    fecha_inicio: date
    fecha_fin: Optional[date] = None

class ResponsableObjetoCreate(ResponsableObjetoBase):
    pass

class ResponsableObjetoRead(ResponsableObjetoBase):
    id_responsable_objeto: int
    fecha_registro: datetime
    model_config = ConfigDict(from_attributes=True)