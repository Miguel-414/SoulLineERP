from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Persona(Base):
    __tablename__ = "persona"

    id_persona: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    primer_nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    segundo_nombre: Mapped[str | None] = mapped_column(String(45))
    primer_apellido: Mapped[str] = mapped_column(String(45), nullable=False)
    segundo_apellido: Mapped[str | None] = mapped_column(String(45))
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    direccion: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    usuario: Mapped["Usuario | None"] = relationship("Usuario", back_populates="persona", uselist=False)  # type: ignore[name-defined]  # noqa: F821


class ResponsableObjeto(Base):
    __tablename__ = "responsable_objeto"

    id_responsable_objeto: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_inventario: Mapped[int] = mapped_column(ForeignKey("inventario.id_inventario"), nullable=False)
    id_persona: Mapped[int] = mapped_column(ForeignKey("persona.id_persona"), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date | None] = mapped_column(Date)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    persona: Mapped["Persona"] = relationship("Persona")


class ResponsableUbicacion(Base):
    __tablename__ = "responsable_ubicacion"

    id_responsable_ubicacion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_ubicacion: Mapped[int] = mapped_column(ForeignKey("ubicacion.id_ubicacion"), nullable=False)
    id_persona: Mapped[int] = mapped_column(ForeignKey("persona.id_persona"), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date | None] = mapped_column(Date)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    persona: Mapped["Persona"] = relationship("Persona")


# Importación diferida para evitar circular imports
from app.models.auth import Usuario  # noqa: E402, F401