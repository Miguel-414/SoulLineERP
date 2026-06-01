"""
CRUD para el módulo de personas y responsables.
"""

from sqlalchemy.orm import Session

from app.models.personal import Persona, ResponsableObjeto, ResponsableUbicacion
from app.schemas.personal import (
    PersonaCreate,
    PersonaUpdate,
    ResponsableObjetoCreate,
    ResponsableObjetoUpdate,
    ResponsableUbicacionCreate,
    ResponsableUbicacionUpdate,
)


# ── Persona ────────────────────────────────────────────────────────────────

def get_persona(db: Session, id_persona: int) -> Persona | None:
    return db.get(Persona, id_persona)


def get_personas(db: Session, skip: int = 0, limit: int = 100) -> list[Persona]:
    return db.query(Persona).offset(skip).limit(limit).all()


def create_persona(db: Session, data: PersonaCreate) -> Persona:
    obj = Persona(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_persona(db: Session, id_persona: int, data: PersonaUpdate) -> Persona | None:
    obj = get_persona(db, id_persona)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_persona(db: Session, id_persona: int) -> bool:
    obj = get_persona(db, id_persona)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── ResponsableObjeto ──────────────────────────────────────────────────────

def get_responsable_objeto(db: Session, id_responsable: int) -> ResponsableObjeto | None:
    return db.get(ResponsableObjeto, id_responsable)


def get_responsables_objeto(
    db: Session,
    id_inventario: int | None = None,
    id_persona: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ResponsableObjeto]:
    q = db.query(ResponsableObjeto)
    if id_inventario:
        q = q.filter(ResponsableObjeto.id_inventario == id_inventario)
    if id_persona:
        q = q.filter(ResponsableObjeto.id_persona == id_persona)
    return q.offset(skip).limit(limit).all()


def create_responsable_objeto(db: Session, data: ResponsableObjetoCreate) -> ResponsableObjeto:
    obj = ResponsableObjeto(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_responsable_objeto(
    db: Session, id_responsable: int, data: ResponsableObjetoUpdate
) -> ResponsableObjeto | None:
    obj = get_responsable_objeto(db, id_responsable)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_responsable_objeto(db: Session, id_responsable: int) -> bool:
    obj = get_responsable_objeto(db, id_responsable)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── ResponsableUbicacion ───────────────────────────────────────────────────

def get_responsable_ubicacion(db: Session, id_responsable: int) -> ResponsableUbicacion | None:
    return db.get(ResponsableUbicacion, id_responsable)


def get_responsables_ubicacion(
    db: Session,
    id_ubicacion: int | None = None,
    id_persona: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ResponsableUbicacion]:
    q = db.query(ResponsableUbicacion)
    if id_ubicacion:
        q = q.filter(ResponsableUbicacion.id_ubicacion == id_ubicacion)
    if id_persona:
        q = q.filter(ResponsableUbicacion.id_persona == id_persona)
    return q.offset(skip).limit(limit).all()


def create_responsable_ubicacion(db: Session, data: ResponsableUbicacionCreate) -> ResponsableUbicacion:
    obj = ResponsableUbicacion(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_responsable_ubicacion(
    db: Session, id_responsable: int, data: ResponsableUbicacionUpdate
) -> ResponsableUbicacion | None:
    obj = get_responsable_ubicacion(db, id_responsable)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_responsable_ubicacion(db: Session, id_responsable: int) -> bool:
    obj = get_responsable_ubicacion(db, id_responsable)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
