from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud import crud_inventario
from app.models.auth import Usuario
from app.schemas.inventario import (
    InventarioCreate,
    InventarioRead,
    InventarioUpdate,
    UbicacionCreate,
    UbicacionRead,
    UbicacionUpdate,
)

router = APIRouter()


# ── Ubicaciones ───────────────────────────────────────────────────────────────

@router.get("/", response_model=list[UbicacionRead])
def listar_ubicaciones(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_ubicaciones(db, skip=skip, limit=limit)


@router.post("/", response_model=UbicacionRead, status_code=status.HTTP_201_CREATED)
def crear_ubicacion(
    data: UbicacionCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.create_ubicacion(db, data)


@router.get("/{id_ubicacion}", response_model=UbicacionRead)
def obtener_ubicacion(
    id_ubicacion: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.get_ubicacion(db, id_ubicacion)
    if not obj:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return obj


@router.patch("/{id_ubicacion}", response_model=UbicacionRead)
def actualizar_ubicacion(
    id_ubicacion: int,
    data: UbicacionUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_ubicacion(db, id_ubicacion, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return obj


@router.delete("/{id_ubicacion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_ubicacion(
    id_ubicacion: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_inventario.delete_ubicacion(db, id_ubicacion):
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")


# ── Inventario por ubicación ──────────────────────────────────────────────────

@router.get("/{id_ubicacion}/inventario", response_model=list[InventarioRead])
def inventario_por_ubicacion(
    id_ubicacion: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_inventarios(db, id_ubicacion=id_ubicacion, skip=skip, limit=limit)


@router.post("/{id_ubicacion}/inventario", response_model=InventarioRead, status_code=status.HTTP_201_CREATED)
def crear_entrada_inventario(
    id_ubicacion: int,
    data: InventarioCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    data.id_ubicacion = id_ubicacion
    return crud_inventario.create_inventario(db, data)


@router.patch("/inventario/{id_inventario}", response_model=InventarioRead)
def actualizar_inventario(
    id_inventario: int,
    data: InventarioUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_inventario(db, id_inventario, data)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Registro de inventario no encontrado")
    return obj
