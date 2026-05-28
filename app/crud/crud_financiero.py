from sqlalchemy.orm import Session

from app.models.financiero import DetalleFactura, Factura, Proveedor
from app.schemas.financiero import (
    DetalleFacturaCreate,
    FacturaCreate,
    FacturaUpdate,
    ProveedorCreate,
    ProveedorUpdate,
)


# ── Proveedor ─────────────────────────────────────────────────────────────────

def get_proveedor(db: Session, id_proveedor: int) -> Proveedor | None:
    return db.get(Proveedor, id_proveedor)

def get_proveedor_by_nit(db: Session, nit: str) -> Proveedor | None:
    return db.query(Proveedor).filter(Proveedor.nit == nit).first()

def get_proveedores(db: Session, skip: int = 0, limit: int = 100) -> list[Proveedor]:
    return db.query(Proveedor).offset(skip).limit(limit).all()

def create_proveedor(db: Session, data: ProveedorCreate) -> Proveedor:
    obj = Proveedor(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_proveedor(db: Session, id_proveedor: int, data: ProveedorUpdate) -> Proveedor | None:
    obj = get_proveedor(db, id_proveedor)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj

def delete_proveedor(db: Session, id_proveedor: int) -> bool:
    obj = get_proveedor(db, id_proveedor)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Factura ───────────────────────────────────────────────────────────────────

def get_factura(db: Session, id_factura: int) -> Factura | None:
    return db.get(Factura, id_factura)

def get_facturas(db: Session, id_proveedor: int | None = None, skip: int = 0, limit: int = 100) -> list[Factura]:
    q = db.query(Factura)
    if id_proveedor:
        q = q.filter(Factura.id_proveedor == id_proveedor)
    return q.offset(skip).limit(limit).all()

def create_factura(db: Session, data: FacturaCreate) -> Factura:
    obj = Factura(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update_factura(db: Session, id_factura: int, data: FacturaUpdate) -> Factura | None:
    obj = get_factura(db, id_factura)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


# ── DetalleFactura ────────────────────────────────────────────────────────────

def get_detalles_factura(db: Session, id_factura: int) -> list[DetalleFactura]:
    return db.query(DetalleFactura).filter(DetalleFactura.id_factura == id_factura).all()

def create_detalle_factura(db: Session, data: DetalleFacturaCreate) -> DetalleFactura:
    obj = DetalleFactura(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj