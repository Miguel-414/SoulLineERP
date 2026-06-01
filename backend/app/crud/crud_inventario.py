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
    ObjetoAcumulable,
    TipoMovimiento,
    Movimiento,
    DetalleMovimiento,
)
from app.schemas.inventario import (
    InventarioCreate,
    InventarioUpdate,
    ItemSerializadoCreate,
    ItemSerializadoUpdate,
    ObjetoAcumulableCreate,
    ObjetoAcumulableUpdate,
    ObjetoCreate,
    ObjetoUpdate,
    TipoActivoCreate,
    TipoActivoUpdate,
    UbicacionCreate,
    UbicacionUpdate,
    TipoMovimientoCreate,
    TipoMovimientoUpdate,
    MovimientoCreate,
    MovimientoUpdate,
    DetalleMovimientoCreate,
    DetalleMovimientoUpdate,
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


def delete_item_serializado(db: Session, id_item: int) -> bool:
    obj = get_item_serializado(db, id_item)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

# ── ObjetoAcumulable ─────────────────────────────────────────────────────────────────

# todo ? Por que hay tablas que no tienen aqui su metodo delete


def get_objeto_acumulable(db: Session, id_acumulable: int) -> ObjetoAcumulable:
    return db.get(ObjetoAcumulable, id_acumulable)


def get_objetos_acumulable(db: Session, id_objeto: int | None = None, skip: int = 0, limit: int = 100) -> list[ObjetoAcumulable]:
    q = db.query(ObjetoAcumulable)
    if id_objeto:
        q = q.filter(ObjetoAcumulable.id_objeto == id_objeto)
    return q.offset(skip).limit(limit).all()


def create_objeto_acumulable(db: Session, data: ObjetoAcumulableCreate) -> ObjetoAcumulable:
    obj = ObjetoAcumulable(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_objeto_acumulable(db: Session, id_acumulable: int, data: ObjetoAcumulableUpdate) -> ObjetoAcumulable | None:
    obj = get_objeto_acumulable(db, id_acumulable)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_objeto_acumulable(db: Session, id_acumulable: int) -> bool:
    obj = get_objeto_acumulable(db, id_acumulable)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

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


# ── TipoMovimiento ────────────────────────────────────────────────────────

def get_tipo_movimiento(db: Session, id_tipo_movimiento: int) -> TipoMovimiento | None:
    return db.get(TipoMovimiento, id_tipo_movimiento)


def get_tipos_movimiento(db: Session, skip: int = 0, limit: int = 100) -> list[TipoMovimiento]:
    return db.query(TipoMovimiento).offset(skip).limit(limit).all()


def create_tipo_movimiento(db: Session, data: TipoMovimientoCreate) -> TipoMovimiento:
    obj = TipoMovimiento(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_tipo_movimiento(db: Session, id_tipo_movimiento: int, data: TipoMovimientoUpdate) -> TipoMovimiento | None:
    obj = get_tipo_movimiento(db, id_tipo_movimiento)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_tipo_movimiento(db: Session, id_tipo_movimiento: int) -> bool:
    obj = get_tipo_movimiento(db, id_tipo_movimiento)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Movimiento ────────────────────────────────────────────────────────────

def get_movimiento(db: Session, id_movimiento: int) -> Movimiento | None:
    return db.get(Movimiento, id_movimiento)


def get_movimientos(db: Session, id_tipo_movimiento: int | None = None, skip: int = 0, limit: int = 100) -> list[Movimiento]:
    q = db.query(Movimiento)
    if id_tipo_movimiento:
        q = q.filter(Movimiento.id_tipo_movimiento == id_tipo_movimiento)
    return q.offset(skip).limit(limit).all()


def create_movimiento(db: Session, data: MovimientoCreate) -> Movimiento:
    obj = Movimiento(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_movimiento(db: Session, id_movimiento: int, data: MovimientoUpdate) -> Movimiento | None:
    obj = get_movimiento(db, id_movimiento)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_movimiento(db: Session, id_movimiento: int) -> bool:
    obj = get_movimiento(db, id_movimiento)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── DetalleMovimiento ─────────────────────────────────────────────────────

def get_detalle_movimiento(db: Session, id_detalle: int) -> DetalleMovimiento | None:
    return db.get(DetalleMovimiento, id_detalle)


def get_detalles_movimiento(db: Session, id_movimiento: int | None = None, skip: int = 0, limit: int = 100) -> list[DetalleMovimiento]:
    q = db.query(DetalleMovimiento)
    if id_movimiento:
        q = q.filter(DetalleMovimiento.id_movimiento == id_movimiento)
    return q.offset(skip).limit(limit).all()


def create_detalle_movimiento(db: Session, data: DetalleMovimientoCreate) -> DetalleMovimiento:
    obj = DetalleMovimiento(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_detalle_movimiento(db: Session, id_detalle: int, data: DetalleMovimientoUpdate) -> DetalleMovimiento | None:
    obj = get_detalle_movimiento(db, id_detalle)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_detalle_movimiento(db: Session, id_detalle: int) -> bool:
    obj = get_detalle_movimiento(db, id_detalle)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
