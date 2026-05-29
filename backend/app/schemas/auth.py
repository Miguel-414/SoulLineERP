from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.personal import PersonaCreate


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


class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class RolRead(RolBase):
    id_rol: int
    model_config = ConfigDict(from_attributes=True)


# ── Usuario ───────────────────────────────────────────────────────────────────

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


# ── Registro atómico (un solo body con persona + usuario) ─────────────────────

class RegisterRequest(BaseModel):
    """
    Body unificado para POST /auth/register.
    Agrupa los datos de Persona y Usuario en un solo JSON limpio,
    lo que evita el problema anterior de dos bodies separados.

    Ejemplo:
    {
        "persona": {
            "primer_nombre": "Juan",
            "primer_apellido": "García",
            "nombre": "Juan García",
            "email": "juan@email.com",
            "direccion": "Calle 123",
            "telefono": "3001234567"
        },
        "usuario": {
            "nombre_usuario": "jgarcia",
            "contrasena": "MiPass123!",
            "id_rol": 2
        }
    }
    """
    persona: PersonaCreate
    usuario: "UsuarioCreateSinPersona"


class UsuarioCreateSinPersona(BaseModel):
    """Datos del usuario sin id_persona — lo asigna el endpoint internamente."""
    nombre_usuario: str
    contrasena: str
    id_rol: int
