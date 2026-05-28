from typing import Optional

from pydantic import BaseModel, ConfigDict


# ── Token (lo que se devuelve al hacer login) ─────────────────────────────────

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Credenciales de login ─────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    nombre_usuario: str
    contrasena: str


# ── Rol ───────────────────────────────────────────────────────────────────────

class RolBase(BaseModel):
    nombre: str
    descripcion: str

class RolCreate(RolBase):
    pass

class RolRead(RolBase):
    id_rol: int
    model_config = ConfigDict(from_attributes=True)


# ── Usuario ───────────────────────────────────────────────────────────────────
# todo para crear un usuario le esta exigiendo que diga que rol va a tener y el id de si mismo
class UsuarioBase(BaseModel):
    nombre_usuario: str
    id_rol: int
    id_persona: int

class UsuarioCreate(UsuarioBase):
    # La contraseña viene en texto plano; se hashea en el CRUD antes de guardar
    contrasena: str

class UsuarioUpdate(BaseModel):
    id_rol: Optional[int] = None

class UsuarioRead(UsuarioBase):
    id_usuario: int
    # Nunca exponer la contraseña en la respuesta
    model_config = ConfigDict(from_attributes=True)


# ── Usuario con info de contexto (token decodificado) ─────────────────────────

class UsuarioActual(BaseModel):
    id_usuario: int
    nombre_usuario: str
    id_rol: int