from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud import crud_inventario
from app.models.auth import Usuario
from app.schemas.inventario import (
    DetalleMovimientoCreate,
    DetalleMovimientoRead,
    DetalleMovimientoUpdate,
    MovimientoCreate,
    MovimientoRead,
    MovimientoUpdate,
    TipoMovimientoCreate,
    TipoMovimientoRead,
    TipoMovimientoUpdate,
)

router = APIRouter()


# ── Tipos de Movimiento ───────────────────────────────────────────────────

@router.get("/tipos", response_model=list[TipoMovimientoRead])
def listar_tipos_movimiento(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_tipos_movimiento(db, skip=skip, limit=limit)


@router.post("/tipos", response_model=TipoMovimientoRead, status_code=status.HTTP_201_CREATED)
def crear_tipo_movimiento(
    data: TipoMovimientoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.create_tipo_movimiento(db, data)


@router.get("/tipos/{id_tipo}", response_model=TipoMovimientoRead)
def obtener_tipo_movimiento(
    id_tipo: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.get_tipo_movimiento(db, id_tipo)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Tipo de movimiento no encontrado")
    return obj


@router.patch("/tipos/{id_tipo}", response_model=TipoMovimientoRead)
def actualizar_tipo_movimiento(
    id_tipo: int,
    data: TipoMovimientoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_tipo_movimiento(db, id_tipo, data)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Tipo de movimiento no encontrado")
    return obj


@router.delete("/tipos/{id_tipo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_movimiento(
    id_tipo: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_inventario.delete_tipo_movimiento(db, id_tipo):
        raise HTTPException(
            status_code=404, detail="Tipo de movimiento no encontrado")


# ── Movimientos ───────────────────────────────────────────────────────────

@router.get("/", response_model=list[MovimientoRead])
def listar_movimientos(
    id_tipo_movimiento: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_movimientos(db, id_tipo_movimiento=id_tipo_movimiento, skip=skip, limit=limit)


@router.post("/", response_model=MovimientoRead, status_code=status.HTTP_201_CREATED)
def crear_movimiento(
    data: MovimientoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.create_movimiento(db, data)


@router.get("/{id_movimiento}", response_model=MovimientoRead)
def obtener_movimiento(
    id_movimiento: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.get_movimiento(db, id_movimiento)
    if not obj:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return obj


@router.patch("/{id_movimiento}", response_model=MovimientoRead)
def actualizar_movimiento(
    id_movimiento: int,
    data: MovimientoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_movimiento(db, id_movimiento, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    return obj


@router.delete("/{id_movimiento}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_movimiento(
    id_movimiento: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_inventario.delete_movimiento(db, id_movimiento):
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")


# ── Detalles de Movimiento ────────────────────────────────────────────────

@router.patch("/detalles/{id_detalle}", response_model=DetalleMovimientoRead)
def actualizar_detalle_movimiento(
    id_detalle: int,
    data: DetalleMovimientoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_detalle_movimiento(db, id_detalle, data)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Detalle de movimiento no encontrado")
    return obj


@router.delete("/detalles/{id_detalle}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_detalle_movimiento(
    id_detalle: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_inventario.delete_detalle_movimiento(db, id_detalle):
        raise HTTPException(
            status_code=404, detail="Detalle de movimiento no encontrado")


@router.get("/{id_movimiento}/detalles", response_model=list[DetalleMovimientoRead])
def listar_detalles(
    id_movimiento: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_detalles_movimiento(db, id_movimiento=id_movimiento, skip=skip, limit=limit)


@router.post("/{id_movimiento}/detalles", response_model=DetalleMovimientoRead, status_code=status.HTTP_201_CREATED)
def crear_detalle_movimiento(
    id_movimiento: int,
    data: DetalleMovimientoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    data.id_movimiento = id_movimiento
    return crud_inventario.create_detalle_movimiento(db, data)
