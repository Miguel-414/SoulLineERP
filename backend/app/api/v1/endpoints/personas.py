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
from app.crud import crud_personal
from app.models.auth import Usuario
from app.schemas.personal import (
    PersonaCreate,
    PersonaRead,
    PersonaUpdate,
    ResponsableObjetoCreate,
    ResponsableObjetoRead,
    ResponsableObjetoUpdate,
    ResponsableUbicacionCreate,
    ResponsableUbicacionRead,
    ResponsableUbicacionUpdate,
)

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


# ── Responsables de Objetos ───────────────────────────────────────────────

@router.get("/{id_persona}/responsabilidades-objeto", response_model=list[ResponsableObjetoRead])
def listar_responsabilidades_objeto(
    id_persona: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_personal.get_responsables_objeto(db, id_persona=id_persona, skip=skip, limit=limit)


@router.post("/{id_persona}/responsabilidades-objeto", response_model=ResponsableObjetoRead, status_code=status.HTTP_201_CREATED)
def crear_responsable_objeto(
    id_persona: int,
    data: ResponsableObjetoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    data.id_persona = id_persona
    return crud_personal.create_responsable_objeto(db, data)


@router.patch("/responsables-objeto/{id_responsable}", response_model=ResponsableObjetoRead)
def actualizar_responsable_objeto(
    id_responsable: int,
    data: ResponsableObjetoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_personal.update_responsable_objeto(db, id_responsable, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")
    return obj


@router.delete("/responsables-objeto/{id_responsable}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_responsable_objeto(
    id_responsable: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_personal.delete_responsable_objeto(db, id_responsable):
        raise HTTPException(status_code=404, detail="Responsable no encontrado")


# ── Responsables de Ubicaciones ───────────────────────────────────────────

@router.get("/{id_persona}/responsabilidades-ubicacion", response_model=list[ResponsableUbicacionRead])
def listar_responsabilidades_ubicacion(
    id_persona: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_personal.get_responsables_ubicacion(db, id_persona=id_persona, skip=skip, limit=limit)


@router.post("/{id_persona}/responsabilidades-ubicacion", response_model=ResponsableUbicacionRead, status_code=status.HTTP_201_CREATED)
def crear_responsable_ubicacion(
    id_persona: int,
    data: ResponsableUbicacionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    data.id_persona = id_persona
    return crud_personal.create_responsable_ubicacion(db, data)


@router.patch("/responsables-ubicacion/{id_responsable}", response_model=ResponsableUbicacionRead)
def actualizar_responsable_ubicacion(
    id_responsable: int,
    data: ResponsableUbicacionUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_personal.update_responsable_ubicacion(db, id_responsable, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Responsable no encontrado")
    return obj


@router.delete("/responsables-ubicacion/{id_responsable}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_responsable_ubicacion(
    id_responsable: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_personal.delete_responsable_ubicacion(db, id_responsable):
        raise HTTPException(status_code=404, detail="Responsable no encontrado")
