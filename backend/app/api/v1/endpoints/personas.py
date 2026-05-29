from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud.crud_auth import (
    create_persona,
    delete_persona,
    get_persona,
    get_persona_by_email,
    get_personas,
    update_persona,
)
from app.models.auth import Usuario
from app.schemas.personal import PersonaCreate, PersonaRead, PersonaUpdate

router = APIRouter()


@router.get("/", response_model=list[PersonaRead])
def listar_personas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return get_personas(db, skip=skip, limit=limit)


@router.post("/", response_model=PersonaRead, status_code=status.HTTP_201_CREATED)
def crear_persona(
    data: PersonaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """
    Crea una Persona de forma independiente, sin asociarla a un usuario.
    Útil para registrar personal que aún no tiene cuenta en el sistema.
    """
    if get_persona_by_email(db, data.email):
        raise HTTPException(
            status_code=400, detail="El email ya está registrado")
    return create_persona(db, data)


@router.get("/{id_persona}", response_model=PersonaRead)
def obtener_persona(
    id_persona: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = get_persona(db, id_persona)
    if not obj:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return obj


@router.patch("/{id_persona}", response_model=PersonaRead)
def actualizar_persona(
    id_persona: int,
    data: PersonaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = update_persona(db, id_persona, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return obj


@router.delete("/{id_persona}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_persona(
    id_persona: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not delete_persona(db, id_persona):
        raise HTTPException(status_code=404, detail="Persona no encontrada")
