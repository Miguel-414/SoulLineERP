"""
Modelos SQLAlchemy para el módulo de inventario.
Cada clase = una tabla en la base de datos.
"""

import enum
from datetime import date, datetime

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


# ── Enumeraciones ─────────────────────────────────────────────────────────────
# Estas clases espejo exacto de los ENUM definidos en MySQL.

class TipoObjetoEnum(str, enum.Enum):
    acumulable = "acumulable"
    unico = "unico"


class EstadoFuncionalEnum(str, enum.Enum):
    OPERATIVO = "OPERATIVO"
    FALLANDO = "FALLANDO"
    RETIRADO = "RETIRADO"


class EstadoFisicoEnum(str, enum.Enum):
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    MALO = "MALO"


# ── Modelos ───────────────────────────────────────────────────────────────────

class TipoActivo(Base):
    __tablename__ = "tipo_activo"

    id_tipo_activo: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relación inversa: un tipo_activo tiene muchos objetos
    objetos: Mapped[list["Objeto"]] = relationship(
        "Objeto", back_populates="tipo_activo")


class Objeto(Base):
    __tablename__ = "objeto"

    id_objeto: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    tipo_objeto: Mapped[TipoObjetoEnum] = mapped_column(
        Enum(TipoObjetoEnum), nullable=False)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    marca: Mapped[str | None] = mapped_column(String(45))
    modelo: Mapped[str | None] = mapped_column(String(45))
    id_tipo_activo: Mapped[int] = mapped_column(
        ForeignKey("tipo_activo.id_tipo_activo"), nullable=False)

    tipo_activo: Mapped["TipoActivo"] = relationship(
        "TipoActivo", back_populates="objetos")
    items_serializados: Mapped[list["ItemSerializado"]] = relationship(
        "ItemSerializado", back_populates="objeto")
    objetos_acumulables: Mapped[list["ObjetoAcumulable"]] = relationship(
        "ObjetoAcumulable", back_populates="objeto")
    inventarios: Mapped[list["Inventario"]] = relationship(
        "Inventario", back_populates="objeto")


class ItemSerializado(Base):
    __tablename__ = "item_serializado"

    id_item_serializado: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_objeto: Mapped[int] = mapped_column(
        ForeignKey("objeto.id_objeto"), nullable=False)
    serie: Mapped[str | None] = mapped_column(String(45), unique=True)
    placa_activo: Mapped[str] = mapped_column(
        String(45), unique=True, nullable=False)
    estado_funcional: Mapped[EstadoFuncionalEnum] = mapped_column(
        Enum(EstadoFuncionalEnum), nullable=False)
    estado_fisico: Mapped[EstadoFisicoEnum] = mapped_column(
        Enum(EstadoFisicoEnum), nullable=False)
    fecha_adquisicion: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_puesto_servicio: Mapped[date | None] = mapped_column(Date)
    n_garantia: Mapped[str | None] = mapped_column(String(45))
    fecha_inicio_garantia: Mapped[date | None] = mapped_column(Date)
    fecha_fin_garantia: Mapped[date | None] = mapped_column(Date)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())

    objeto: Mapped["Objeto"] = relationship(
        "Objeto", back_populates="items_serializados")


class Ubicacion(Base):
    __tablename__ = "ubicacion"

    id_ubicacion: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(String(45))
    # Auto-relación: una ubicación puede tener una ubicación padre (zonas anidadas)
    id_zona_padre: Mapped[int | None] = mapped_column(
        ForeignKey("ubicacion.id_ubicacion"))

    zona_padre: Mapped["Ubicacion | None"] = relationship(
        "Ubicacion", remote_side="Ubicacion.id_ubicacion")
    inventarios: Mapped[list["Inventario"]] = relationship(
        "Inventario", back_populates="ubicacion")


class Inventario(Base):
    __tablename__ = "inventario"

    __table_args__ = (
        CheckConstraint("cantidad_actual >= 0",
                        name="CHK_inventario_valor_positivo"),
    )

    id_inventario: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_objeto: Mapped[int] = mapped_column(
        ForeignKey("objeto.id_objeto"), nullable=False)
    id_item_serializado: Mapped[int | None] = mapped_column(
        ForeignKey("item_serializado.id_item_serializado"))
    cantidad_actual: Mapped[int] = mapped_column(Integer, nullable=False)
    id_ubicacion: Mapped[int] = mapped_column(
        ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    estado_actual: Mapped[EstadoFuncionalEnum] = mapped_column(
        Enum(EstadoFuncionalEnum), nullable=False)
    fecha_ultima_actualizacion: Mapped[datetime] = mapped_column(
        DateTime, nullable=False)

    objeto: Mapped["Objeto"] = relationship(
        "Objeto", back_populates="inventarios")
    item_serializado: Mapped["ItemSerializado | None"] = relationship(
        "ItemSerializado")
    ubicacion: Mapped["Ubicacion"] = relationship(
        "Ubicacion", back_populates="inventarios")


class ObjetoAcumulable(Base):
    __tablename__ = "objeto_acumulable"

    __table_args__ = (
        CheckConstraint("cantidad > 0", name="CHK_cantidad_positiva"),
    )

    id_objeto_acumulable: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_objeto: Mapped[int] = mapped_column(
        ForeignKey("objeto.id_objeto"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    fecha_adquisicion: Mapped[date | None] = mapped_column(Date)
    forma_adquisicion: Mapped[str | None] = mapped_column(String(45))
    id_factura: Mapped[int | None] = mapped_column(
        ForeignKey("factura.id_factura"))
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now())

    objeto: Mapped["Objeto"] = relationship(
        "Objeto", back_populates="objetos_acumulables")
    factura: Mapped["Factura | None"] = relationship("Factura", foreign_keys=[id_factura])  # type: ignore[name-defined]  # noqa: F821


class TipoMovimiento(Base):
    __tablename__ = "tipo_movimiento"

    id_tipo_movimiento: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    movimientos: Mapped[list["Movimiento"]] = relationship(
        "Movimiento", back_populates="tipo_movimiento")


class Movimiento(Base):
    __tablename__ = "movimiento"

    id_movimiento: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    fecha_movimiento: Mapped[date] = mapped_column(Date, nullable=False)
    id_tipo_movimiento: Mapped[int] = mapped_column(
        ForeignKey("tipo_movimiento.id_tipo_movimiento"), nullable=False)

    tipo_movimiento: Mapped["TipoMovimiento"] = relationship(
        "TipoMovimiento", back_populates="movimientos")
    detalles: Mapped[list["DetalleMovimiento"]] = relationship(
        "DetalleMovimiento", back_populates="movimiento")


class DetalleMovimiento(Base):
    __tablename__ = "detalle_movimiento"

    __table_args__ = (
        CheckConstraint("cantidad_afectada >= 1",
                        name="CHK_detalle_movimiento_valor_mayor_1"),
    )

    id_detalle_movimiento: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    id_movimiento: Mapped[int] = mapped_column(
        ForeignKey("movimiento.id_movimiento"), nullable=False)
    id_objeto: Mapped[int] = mapped_column(
        ForeignKey("objeto.id_objeto"), nullable=False)
    id_item_serializado: Mapped[int | None] = mapped_column(
        ForeignKey("item_serializado.id_item_serializado"))
    id_inventario_origen: Mapped[int | None] = mapped_column(
        ForeignKey("inventario.id_inventario"))
    id_inventario_destino: Mapped[int | None] = mapped_column(
        ForeignKey("inventario.id_inventario"))
    id_ubicacion_origen: Mapped[int | None] = mapped_column(
        ForeignKey("ubicacion.id_ubicacion"))
    id_ubicacion_destino: Mapped[int] = mapped_column(
        ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    cantidad_afectada: Mapped[int] = mapped_column(Integer, nullable=False)
    observaciones: Mapped[str | None] = mapped_column(String(100))

    movimiento: Mapped["Movimiento"] = relationship(
        "Movimiento", back_populates="detalles")
    objeto: Mapped["Objeto"] = relationship("Objeto")
    item_serializado: Mapped["ItemSerializado | None"] = relationship(
        "ItemSerializado")
    inventario_origen: Mapped["Inventario | None"] = relationship(
        "Inventario", foreign_keys=[id_inventario_origen])
    inventario_destino: Mapped["Inventario | None"] = relationship(
        "Inventario", foreign_keys=[id_inventario_destino])
    ubicacion_origen: Mapped["Ubicacion | None"] = relationship(
        "Ubicacion", foreign_keys=[id_ubicacion_origen])
    ubicacion_destino: Mapped["Ubicacion"] = relationship(
        "Ubicacion", foreign_keys=[id_ubicacion_destino])
