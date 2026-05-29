from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.core.security import create_access_token
from app.crud.crud_auth import (
    authenticate_usuario,
    delete_usuario,
    get_persona_by_email,
    get_rol,
    get_usuario_by_nombre,
    get_usuarios,
    register_usuario,
    update_usuario,
)
from app.models.auth import Usuario
from app.schemas.auth import RegisterRequest, Token, UsuarioRead, UsuarioUpdate

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Recibe usuario y contraseña (form-data OAuth2). Retorna un JWT."""
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
    data: RegisterRequest,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """
    Crea una Persona y su Usuario en una sola transacción atómica.

    Body esperado:
    {
        "persona": { ...datos de persona... },
        "usuario": { "nombre_usuario": "x", "contrasena": "x", "id_rol": 1 }
    }

    Si el rol no existe, el email o el username ya están tomados, rechaza todo
    antes de tocar la base de datos.
    """
    if get_persona_by_email(db, data.persona.email):
        raise HTTPException(
            status_code=400, detail="El email ya está registrado")

    if get_usuario_by_nombre(db, data.usuario.nombre_usuario):
        raise HTTPException(
            status_code=400, detail="El nombre de usuario ya existe")

    if not get_rol(db, data.usuario.id_rol):
        raise HTTPException(
            status_code=400,
            detail=f"El rol con id={data.usuario.id_rol} no existe. "
            "Consulta GET /api/v1/roles para ver los roles disponibles.",
        )

    try:
        return register_usuario(db, data.persona, data.usuario)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear el usuario: {str(e)}")


@router.get("/me", response_model=UsuarioRead)
def get_me(current_user: Usuario = Depends(get_current_user)):
    """Retorna la información del usuario autenticado."""
    return current_user


@router.get("/usuarios", response_model=list[UsuarioRead])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Lista todos los usuarios registrados."""
    return get_usuarios(db, skip=skip, limit=limit)


@router.patch("/usuarios/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    id_usuario: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    try:
        obj = update_usuario(db, id_usuario, data)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if not obj:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return obj


@router.delete("/usuarios/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(
    id_usuario: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    try:
        ok = delete_usuario(db, id_usuario)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
