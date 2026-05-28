import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AccionAuditoriaEnum(str, enum.Enum):
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class Rol(Base):
    __tablename__ = "rol"

    id_rol: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(100), nullable=False)

    usuarios: Mapped[list["Usuario"]] = relationship("Usuario", back_populates="rol")
    permisos_rol: Mapped[list["PermisoRol"]] = relationship("PermisoRol", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_persona: Mapped[int] = mapped_column(ForeignKey("persona.id_persona"), nullable=False)
    nombre_usuario: Mapped[str] = mapped_column(String(45), unique=True, nullable=False)
    # Nunca guardes la contraseña aquí directamente — usa security.hash_password()
    contrasena: Mapped[str] = mapped_column(String(200), nullable=False)
    id_rol: Mapped[int] = mapped_column(ForeignKey("rol.id_rol"), nullable=False)

    persona: Mapped["Persona"] = relationship("Persona", back_populates="usuario")  # type: ignore[name-defined]  # noqa: F821
    rol: Mapped["Rol"] = relationship("Rol", back_populates="usuarios")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id_log: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_tabla: Mapped[str] = mapped_column(String(20), nullable=False)
    id_registro_afectado: Mapped[int] = mapped_column(Integer, nullable=False)
    accion: Mapped[AccionAuditoriaEnum] = mapped_column(Enum(AccionAuditoriaEnum), nullable=False)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id_usuario"), nullable=False)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    usuario: Mapped["Usuario"] = relationship("Usuario")


class Operacion(Base):
    __tablename__ = "operacion"

    id_operacion: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(45), nullable=False)


class Modulo(Base):
    __tablename__ = "modulo"

    id_modulo: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre_tabla: Mapped[str] = mapped_column(String(45), nullable=False)


class Permiso(Base):
    __tablename__ = "permiso"

    __table_args__ = (
        UniqueConstraint("id_modulo", "id_operacion", name="UK_modulo_operacion"),
    )

    id_permiso: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_modulo: Mapped[int] = mapped_column(ForeignKey("modulo.id_modulo"), nullable=False)
    id_operacion: Mapped[int] = mapped_column(ForeignKey("operacion.id_operacion"), nullable=False)

    modulo: Mapped["Modulo"] = relationship("Modulo")
    operacion: Mapped["Operacion"] = relationship("Operacion")


class PermisoRol(Base):
    __tablename__ = "permiso_rol"

    id_rol: Mapped[int] = mapped_column(ForeignKey("rol.id_rol"), primary_key=True)
    id_permiso: Mapped[int] = mapped_column(ForeignKey("permiso.id_permiso"), primary_key=True)

    rol: Mapped["Rol"] = relationship("Rol", back_populates="permisos_rol")
    permiso: Mapped["Permiso"] = relationship("Permiso")


# Importación diferida para cerrar la relación bidireccional con Persona
from app.models.personal import Persona  # noqa: E402, F401