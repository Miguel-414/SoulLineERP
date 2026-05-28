from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password, verify_password
from app.models.auth import Rol, Usuario
from app.models.personal import Persona
from app.schemas.auth import RolCreate, RolUpdate, UsuarioCreate, UsuarioUpdate
from app.schemas.personal import PersonaCreate, PersonaUpdate


# ── Guardián del admin maestro ────────────────────────────────────────────────
# Función central que otros CRUDs llaman antes de mutar o eliminar un usuario.

def is_master_admin(usuario: Usuario) -> bool:
    return usuario.nombre_usuario == settings.MASTER_ADMIN_USERNAME


# ── Rol ───────────────────────────────────────────────────────────────────────

def get_rol(db: Session, id_rol: int) -> Rol | None:
    return db.get(Rol, id_rol)


def get_rol_by_nombre(db: Session, nombre: str) -> Rol | None:
    return db.query(Rol).filter(Rol.nombre == nombre).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> list[Rol]:
    return db.query(Rol).offset(skip).limit(limit).all()


def create_rol(db: Session, data: RolCreate) -> Rol:
    obj = Rol(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_rol(db: Session, id_rol: int, data: RolUpdate) -> Rol | None:
    obj = get_rol(db, id_rol)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_rol(db: Session, id_rol: int) -> bool:
    obj = get_rol(db, id_rol)
    if not obj:
        return False
    # Impedir borrar el rol superadmin
    if obj.nombre == "superadmin":
        raise ValueError("El rol superadmin no puede eliminarse.")
    db.delete(obj)
    db.commit()
    return True


# ── Persona ───────────────────────────────────────────────────────────────────

def get_persona(db: Session, id_persona: int) -> Persona | None:
    return db.get(Persona, id_persona)


def get_personas(db: Session, skip: int = 0, limit: int = 100) -> list[Persona]:
    return db.query(Persona).offset(skip).limit(limit).all()


def get_persona_by_email(db: Session, email: str) -> Persona | None:
    return db.query(Persona).filter(Persona.email == email).first()


def create_persona(db: Session, data: PersonaCreate) -> Persona:
    obj = Persona(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_persona(db: Session, id_persona: int, data: PersonaUpdate) -> Persona | None:
    obj = get_persona(db, id_persona)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_persona(db: Session, id_persona: int) -> bool:
    obj = get_persona(db, id_persona)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Usuario ───────────────────────────────────────────────────────────────────

def get_usuario(db: Session, id_usuario: int) -> Usuario | None:
    return db.get(Usuario, id_usuario)


def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()


def get_usuario_by_nombre(db: Session, nombre_usuario: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()


def create_usuario(db: Session, data: UsuarioCreate) -> Usuario:
    hashed = hash_password(data.contrasena)
    obj = Usuario(
        nombre_usuario=data.nombre_usuario,
        contrasena=hashed,
        id_rol=data.id_rol,
        id_persona=data.id_persona,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_usuario(db: Session, id_usuario: int, data: UsuarioUpdate) -> Usuario | None:
    obj = get_usuario(db, id_usuario)
    if not obj:
        return None
    if is_master_admin(obj):
        raise ValueError(
            "El usuario administrador maestro no puede modificarse desde la API.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_usuario(db: Session, id_usuario: int) -> bool:
    obj = get_usuario(db, id_usuario)
    if not obj:
        return False
    if is_master_admin(obj):
        raise ValueError(
            "El usuario administrador maestro no puede eliminarse.")
    db.delete(obj)
    db.commit()
    return True


def authenticate_usuario(db: Session, nombre_usuario: str, contrasena: str) -> Usuario | None:
    user = get_usuario_by_nombre(db, nombre_usuario)
    if not user:
        return None
    if not verify_password(contrasena, user.contrasena):
        return None
    return user


# ── Registro atómico (persona + usuario en una sola transacción) ──────────────

def register_usuario(db: Session, persona_data: PersonaCreate, usuario_data) -> Usuario:
    """
    Crea la Persona y el Usuario en una sola transacción.
    Si cualquiera de los dos pasos falla, todo se revierte (rollback).
    usuario_data puede ser UsuarioCreate o UsuarioCreateSinPersona.
    """
    try:
        persona = Persona(**persona_data.model_dump())
        db.add(persona)
        db.flush()  # Genera el id_persona sin hacer commit todavía

        hashed = hash_password(usuario_data.contrasena)
        usuario = Usuario(
            nombre_usuario=usuario_data.nombre_usuario,
            contrasena=hashed,
            id_rol=usuario_data.id_rol,
            id_persona=persona.id_persona,
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario
    except Exception:
        db.rollback()
        raise
