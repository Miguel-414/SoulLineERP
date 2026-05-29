from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.crud import crud_financiero
from app.models.auth import Usuario
from app.schemas.financiero import (
    DetalleFacturaCreate,
    DetalleFacturaRead,
    FacturaCreate,
    FacturaRead,
    FacturaUpdate,
    ProveedorCreate,
    ProveedorRead,
    ProveedorUpdate,
)

router = APIRouter()


# ── Proveedores ───────────────────────────────────────────────────────────────

@router.get("/proveedores", response_model=list[ProveedorRead])
def listar_proveedores(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_financiero.get_proveedores(db, skip=skip, limit=limit)


@router.post("/proveedores", response_model=ProveedorRead, status_code=status.HTTP_201_CREATED)
def crear_proveedor(
    data: ProveedorCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if crud_financiero.get_proveedor_by_nit(db, data.nit):
        raise HTTPException(
            status_code=400, detail="Ya existe un proveedor con ese NIT")
    return crud_financiero.create_proveedor(db, data)


@router.get("/proveedores/{id_proveedor}", response_model=ProveedorRead)
def obtener_proveedor(
    id_proveedor: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_financiero.get_proveedor(db, id_proveedor)
    if not obj:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return obj


@router.patch("/proveedores/{id_proveedor}", response_model=ProveedorRead)
def actualizar_proveedor(
    id_proveedor: int,
    data: ProveedorUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_financiero.update_proveedor(db, id_proveedor, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    return obj


@router.delete("/proveedores/{id_proveedor}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_proveedor(
    id_proveedor: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    if not crud_financiero.delete_proveedor(db, id_proveedor):
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")


# ── Facturas ──────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[FacturaRead])
def listar_facturas(
    id_proveedor: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_financiero.get_facturas(db, id_proveedor=id_proveedor, skip=skip, limit=limit)


@router.post("/", response_model=FacturaRead, status_code=status.HTTP_201_CREATED)
def crear_factura(
    data: FacturaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_financiero.create_factura(db, data)


@router.get("/{id_factura}", response_model=FacturaRead)
def obtener_factura(
    id_factura: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_financiero.get_factura(db, id_factura)
    if not obj:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return obj


@router.patch("/{id_factura}", response_model=FacturaRead)
def actualizar_factura(
    id_factura: int,
    data: FacturaUpdate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    obj = crud_financiero.update_factura(db, id_factura, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return obj


# ── Detalles de Factura ───────────────────────────────────────────────────────

@router.get("/{id_factura}/detalles", response_model=list[DetalleFacturaRead])
def listar_detalles(
    id_factura: int,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    return crud_financiero.get_detalles_factura(db, id_factura)


@router.post("/{id_factura}/detalles", response_model=DetalleFacturaRead, status_code=status.HTTP_201_CREATED)
def crear_detalle(
    id_factura: int,
    data: DetalleFacturaCreate,
    db: Session = Depends(get_db),
    _: Usuario = Depends(get_current_user),
):
    data.id_factura = id_factura
    return crud_financiero.create_detalle_factura(db, data)
