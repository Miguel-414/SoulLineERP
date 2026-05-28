"""
CRUD de inventario.

Cada función recibe una `db: Session` y parámetros,
ejecuta la consulta o modificación, y retorna el resultado.
Los endpoints en api/ llaman a estas funciones — así se separan
responsabilidades: los endpoints manejan HTTP, el CRUD maneja datos.
"""

from sqlalchemy.orm import Session

from app.models.inventario import (
    Inventario,
    ItemSerializado,
    Objeto,
    TipoActivo,
    Ubicacion,
)
from app.schemas.inventario import (
    InventarioCreate,
    InventarioUpdate,
    ItemSerializadoCreate,
    ItemSerializadoUpdate,
    ObjetoCreate,
    ObjetoUpdate,
    TipoActivoCreate,
    TipoActivoUpdate,
    UbicacionCreate,
    UbicacionUpdate,
)


# ── TipoActivo ────────────────────────────────────────────────────────────────

def get_tipo_activo(db: Session, id_tipo_activo: int) -> TipoActivo | None:
    return db.get(TipoActivo, id_tipo_activo)

def get_tipos_activo(db: Session, skip: int = 0, limit: int = 100) -> list[TipoActivo]:
    return db.query(TipoActivo).offset(skip).limit(limit).all()

def create_tipo_activo(db: Session, data: TipoActivoCreate) -> TipoActivo:
    obj = TipoActivo(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_tipo_activo(db: Session, id_tipo_activo: int, data: TipoActivoUpdate) -> TipoActivo | None:
    obj = get_tipo_activo(db, id_tipo_activo)
    if not obj:
        return None
    # model_dump(exclude_unset=True) solo incluye los campos que el cliente mandó
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_tipo_activo(db: Session, id_tipo_activo: int) -> bool:
    obj = get_tipo_activo(db, id_tipo_activo)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Objeto ────────────────────────────────────────────────────────────────────

def get_objeto(db: Session, id_objeto: int) -> Objeto | None:
    return db.get(Objeto, id_objeto)

def get_objetos(db: Session, skip: int = 0, limit: int = 100) -> list[Objeto]:
    return db.query(Objeto).offset(skip).limit(limit).all()

def create_objeto(db: Session, data: ObjetoCreate) -> Objeto:
    obj = Objeto(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_objeto(db: Session, id_objeto: int, data: ObjetoUpdate) -> Objeto | None:
    obj = get_objeto(db, id_objeto)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_objeto(db: Session, id_objeto: int) -> bool:
    obj = get_objeto(db, id_objeto)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── ItemSerializado ───────────────────────────────────────────────────────────

def get_item_serializado(db: Session, id_item: int) -> ItemSerializado | None:
    return db.get(ItemSerializado, id_item)

def get_items_serializados(db: Session, id_objeto: int | None = None, skip: int = 0, limit: int = 100) -> list[ItemSerializado]:
    q = db.query(ItemSerializado)
    if id_objeto:
        q = q.filter(ItemSerializado.id_objeto == id_objeto)
    return q.offset(skip).limit(limit).all()

def create_item_serializado(db: Session, data: ItemSerializadoCreate) -> ItemSerializado:
    obj = ItemSerializado(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_item_serializado(db: Session, id_item: int, data: ItemSerializadoUpdate) -> ItemSerializado | None:
    obj = get_item_serializado(db, id_item)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


# ── Ubicacion ─────────────────────────────────────────────────────────────────

def get_ubicacion(db: Session, id_ubicacion: int) -> Ubicacion | None:
    return db.get(Ubicacion, id_ubicacion)

def get_ubicaciones(db: Session, skip: int = 0, limit: int = 100) -> list[Ubicacion]:
    return db.query(Ubicacion).offset(skip).limit(limit).all()

def create_ubicacion(db: Session, data: UbicacionCreate) -> Ubicacion:
    obj = Ubicacion(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_ubicacion(db: Session, id_ubicacion: int, data: UbicacionUpdate) -> Ubicacion | None:
    obj = get_ubicacion(db, id_ubicacion)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_ubicacion(db: Session, id_ubicacion: int) -> bool:
    obj = get_ubicacion(db, id_ubicacion)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Inventario ────────────────────────────────────────────────────────────────

def get_inventario(db: Session, id_inventario: int) -> Inventario | None:
    return db.get(Inventario, id_inventario)

def get_inventarios(db: Session, id_ubicacion: int | None = None, skip: int = 0, limit: int = 100) -> list[Inventario]:
    q = db.query(Inventario)
    if id_ubicacion:
        q = q.filter(Inventario.id_ubicacion == id_ubicacion)
    return q.offset(skip).limit(limit).all()

def create_inventario(db: Session, data: InventarioCreate) -> Inventario:
    obj = Inventario(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_inventario(db: Session, id_inventario: int, data: InventarioUpdate) -> Inventario | None:
    obj = get_inventario(db, id_inventario)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj