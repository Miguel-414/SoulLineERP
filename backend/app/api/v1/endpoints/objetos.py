from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud import crud_inventario
from app.models.auth import Usuario
from app.schemas.inventario import (
    ItemSerializadoCreate,
    ItemSerializadoRead,
    ItemSerializadoUpdate,
    ObjetoCreate,
    ObjetoRead,
    ObjetoUpdate,
    TipoActivoCreate,
    TipoActivoRead,
    TipoActivoUpdate,
)

router = APIRouter()


# ── Tipos de Activo ───────────────────────────────────────────────────────────

@router.get("/tipos-activo", response_model=list[TipoActivoRead])
def listar_tipos_activo(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_tipos_activo(db, skip=skip, limit=limit)


@router.post("/tipos-activo", response_model=TipoActivoRead, status_code=status.HTTP_201_CREATED)
def crear_tipo_activo(
    data: TipoActivoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.create_tipo_activo(db, data)


@router.get("/tipos-activo/{id_tipo_activo}", response_model=TipoActivoRead)
def obtener_tipo_activo(
    id_tipo_activo: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.get_tipo_activo(db, id_tipo_activo)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Tipo de activo no encontrado")
    return obj


@router.patch("/tipos-activo/{id_tipo_activo}", response_model=TipoActivoRead)
def actualizar_tipo_activo(
    id_tipo_activo: int,
    data: TipoActivoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_tipo_activo(db, id_tipo_activo, data)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Tipo de activo no encontrado")
    return obj


@router.delete("/tipos-activo/{id_tipo_activo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tipo_activo(
    id_tipo_activo: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_inventario.delete_tipo_activo(db, id_tipo_activo):
        raise HTTPException(
            status_code=404, detail="Tipo de activo no encontrado")


# ── Objetos ───────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[ObjetoRead])
def listar_objetos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_objetos(db, skip=skip, limit=limit)


@router.post("/", response_model=ObjetoRead, status_code=status.HTTP_201_CREATED)
def crear_objeto(
    data: ObjetoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.create_objeto(db, data)


@router.get("/{id_objeto}", response_model=ObjetoRead)
def obtener_objeto(
    id_objeto: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.get_objeto(db, id_objeto)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return obj


@router.patch("/{id_objeto}", response_model=ObjetoRead)
def actualizar_objeto(
    id_objeto: int,
    data: ObjetoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_objeto(db, id_objeto, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Objeto no encontrado")
    return obj


@router.delete("/{id_objeto}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_objeto(
    id_objeto: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_inventario.delete_objeto(db, id_objeto):
        raise HTTPException(status_code=404, detail="Objeto no encontrado")


# ── Items Serializados ────────────────────────────────────────────────────────

@router.get("/{id_objeto}/items", response_model=list[ItemSerializadoRead])
def listar_items(
    id_objeto: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_inventario.get_items_serializados(db, id_objeto=id_objeto, skip=skip, limit=limit)


@router.post("/{id_objeto}/items", response_model=ItemSerializadoRead, status_code=status.HTTP_201_CREATED)
def crear_item(
    id_objeto: int,
    data: ItemSerializadoCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    data.id_objeto = id_objeto
    return crud_inventario.create_item_serializado(db, data)


@router.patch("/items/{id_item}", response_model=ItemSerializadoRead)
def actualizar_item(
    id_item: int,
    data: ItemSerializadoUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_inventario.update_item_serializado(db, id_item, data)
    if not obj:
        raise HTTPException(
            status_code=404, detail="Item serializado no encontrado")
    return obj
