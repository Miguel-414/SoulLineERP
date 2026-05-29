"""
Seeder — inicialización automática de datos base.

Se ejecuta una sola vez al arrancar la aplicación.
Si los datos ya existen, no hace nada (es idempotente).

Crea en orden:
  1. Rol 'superadmin'
  2. Persona placeholder para el admin maestro
  3. Usuario administrador maestro

El usuario maestro NO puede ser eliminado ni degradado por ningún
endpoint; esa protección está en crud_auth.py y en deps.py.
"""

import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import hash_password
from app.models.auth import Rol, Usuario
from app.models.personal import Persona

logger = logging.getLogger(__name__)

# Nombre del rol protegido. Nunca cambiar este valor en producción
# sin una migración planificada.
SUPERADMIN_ROL = "superadmin"


def run(db: Session) -> None:
    """Punto de entrada del seeder. Llamado desde main.py al iniciar."""
    _seed_rol_superadmin(db)
    _seed_usuario_maestro(db)


# ── helpers privados ──────────────────────────────────────────────────────────

def _seed_rol_superadmin(db: Session) -> Rol:
    rol = db.query(Rol).filter(Rol.nombre == SUPERADMIN_ROL).first()
    if not rol:
        rol = Rol(
            nombre=SUPERADMIN_ROL,
            descripcion="Administrador maestro del sistema. Acceso total.",
        )
        db.add(rol)
        db.commit()
        db.refresh(rol)
        logger.info("Seeder: rol '%s' creado (id=%d)",
                    SUPERADMIN_ROL, rol.id_rol)
    return rol


def _seed_usuario_maestro(db: Session) -> None:
    existe = (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == settings.MASTER_ADMIN_USERNAME)
        .first()
    )
    if existe:
        return  # Ya está creado, nada que hacer

    rol = db.query(Rol).filter(Rol.nombre == SUPERADMIN_ROL).first()
    if not rol:
        logger.error(
            "Seeder: no se encontró el rol superadmin. Abortando seed de usuario.")
        return

    persona = Persona(
        primer_nombre="Administrador",
        primer_apellido="Maestro",
        nombre=settings.MASTER_ADMIN_USERNAME,
        email=settings.MASTER_ADMIN_EMAIL,
        direccion="Sistema",
        telefono="0000000000",
    )
    db.add(persona)
    db.flush()  # Necesitamos el id_persona antes del commit

    usuario = Usuario(
        nombre_usuario=settings.MASTER_ADMIN_USERNAME,
        contrasena=hash_password(settings.MASTER_ADMIN_PASSWORD),
        id_rol=rol.id_rol,
        id_persona=persona.id_persona,
    )
    db.add(usuario)
    db.commit()
    logger.info(
        "Seeder: usuario maestro '%s' creado. "
        "CAMBIA LA CONTRASEÑA en .env antes de ir a producción.",
        settings.MASTER_ADMIN_USERNAME,
    )
