from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import create_access_token
from app.crud.crud_auth import authenticate_usuario, create_persona, create_usuario, get_persona_by_email, get_usuario_by_nombre
from app.models.auth import Usuario
from app.schemas.auth import Token, UsuarioCreate, UsuarioRead
from app.schemas.personal import PersonaCreate

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Recibe usuario y contraseña (en form-data, estándar OAuth2).
    Retorna un JWT si las credenciales son correctas.
    """
    user = authenticate_usuario(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.nombre_usuario)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def register(
    persona_data: PersonaCreate,
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db),
):
    """
    Crea una Persona y su Usuario asociado.
    Verifica que el email y el nombre de usuario no estén en uso.
    """
    if get_persona_by_email(db, persona_data.email):
        raise HTTPException(
            status_code=400, detail="El email ya está registrado")

    if get_usuario_by_nombre(db, usuario_data.nombre_usuario):
        raise HTTPException(
            status_code=400, detail="El nombre de usuario ya existe")

    persona = create_persona(db, persona_data)
    usuario_data.id_persona = persona.id_persona
    return create_usuario(db, usuario_data)


@router.get("/me", response_model=UsuarioRead)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Retorna la información del usuario autenticado."""
    return current_user
