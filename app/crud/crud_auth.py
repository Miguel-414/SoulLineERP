from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.auth import Usuario
from app.models.personal import Persona
from app.schemas.auth import UsuarioCreate
from app.schemas.personal import PersonaCreate


# ── Persona ───────────────────────────────────────────────────────────────────

def get_persona(db: Session, id_persona: int) -> Persona | None:
    return db.get(Persona, id_persona)

def get_persona_by_email(db: Session, email: str) -> Persona | None:
    return db.query(Persona).filter(Persona.email == email).first()

def create_persona(db: Session, data: PersonaCreate) -> Persona:
    obj = Persona(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


# ── Usuario ───────────────────────────────────────────────────────────────────

def get_usuario(db: Session, id_usuario: int) -> Usuario | None:
    return db.get(Usuario, id_usuario)

def get_usuario_by_nombre(db: Session, nombre_usuario: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()

def create_usuario(db: Session, data: UsuarioCreate) -> Usuario:
    # Hashear la contraseña ANTES de guardarla
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

def authenticate_usuario(db: Session, nombre_usuario: str, contrasena: str) -> Usuario | None:
    """
    Busca el usuario por nombre y verifica la contraseña.
    Retorna el usuario si las credenciales son correctas, None si no.
    """
    user = get_usuario_by_nombre(db, nombre_usuario)
    if not user:
        return None
    if not verify_password(contrasena, user.contrasena):
        return None
    return user