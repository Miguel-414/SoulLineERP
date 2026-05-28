from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud.crud_auth import (
    create_rol,
    delete_rol,
    get_rol,
    get_rol_by_nombre,
    get_roles,
    update_rol,
)
from app.models.auth import Usuario
from app.schemas.auth import RolCreate, RolRead, RolUpdate

router = APIRouter()


@router.get("/", response_model=list[RolRead])
def listar_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    """Lista todos los roles disponibles en el sistema."""
    return get_roles(db, skip=skip, limit=limit)


@router.post("/", response_model=RolRead, status_code=status.HTTP_201_CREATED)
def crear_rol(
    data: RolCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if get_rol_by_nombre(db, data.nombre):
        raise HTTPException(
            status_code=400, detail=f"Ya existe un rol con el nombre '{data.nombre}'")
    return create_rol(db, data)


@router.get("/{id_rol}", response_model=RolRead)
def obtener_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = get_rol(db, id_rol)
    if not obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return obj


@router.patch("/{id_rol}", response_model=RolRead)
def actualizar_rol(
    id_rol: int,
    data: RolUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = update_rol(db, id_rol, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return obj


@router.delete("/{id_rol}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    try:
        ok = delete_rol(db, id_rol)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    if not ok:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
