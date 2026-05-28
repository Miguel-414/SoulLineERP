from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Proveedor(Base):
    __tablename__ = "proveedor"

    id_proveedor: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nit: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    razon_social: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    direccion: Mapped[str] = mapped_column(String(100), nullable=False)

    facturas: Mapped[list["Factura"]] = relationship("Factura", back_populates="proveedor")


class Factura(Base):
    __tablename__ = "factura"

    __table_args__ = (
        CheckConstraint(
            "total_bruto >= 0 AND iva >= 0 AND valor_iva >= 0 AND "
            "retencion_fuente >= 0 AND descuento >= 0 AND valor_total >= 0",
            name="CHK_factura_valores_positivos",
        ),
    )

    id_factura: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    fecha_generacion: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    id_proveedor: Mapped[int] = mapped_column(ForeignKey("proveedor.id_proveedor"), nullable=False)
    total_bruto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    iva: Mapped[Decimal | None] = mapped_column(Numeric(5, 2), default=0)
    valor_iva: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), default=0)
    retencion_fuente: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), default=0)
    descuento: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    proveedor: Mapped["Proveedor"] = relationship("Proveedor", back_populates="facturas")
    detalles: Mapped[list["DetalleFactura"]] = relationship("DetalleFactura", back_populates="factura")


class DetalleFactura(Base):
    __tablename__ = "detalle_factura"

    __table_args__ = (
        CheckConstraint(
            "cantidad >= 1 AND precio_unitario >= 0 AND valor_bruto >= 0 AND "
            "tasa_impuesto >= 0 AND valor_impto_cargo >= 0 AND descuento >= 0 AND valor_total >= 0",
            name="CHK_detalle_factura_valores_positivos",
        ),
    )

    id_detalle_factura: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_factura: Mapped[int] = mapped_column(ForeignKey("factura.id_factura"), nullable=False)
    id_objeto: Mapped[int] = mapped_column(ForeignKey("objeto.id_objeto"), nullable=False)
    id_item_serializado: Mapped[int | None] = mapped_column(ForeignKey("item_serializado.id_item_serializado"), unique=True)
    descripcion_factura: Mapped[str] = mapped_column(Text, nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    valor_bruto: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    tasa_impuesto: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)
    valor_impto_cargo: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    descuento: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    factura: Mapped["Factura"] = relationship("Factura", back_populates="detalles")