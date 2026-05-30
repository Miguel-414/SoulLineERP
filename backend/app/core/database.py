from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import database_exists, create_database
from typing import Generator

from app.core.config import settings

# Logica para poder verificar la existencia de la base de datos
import os
import re
from sqlalchemy import inspect


def script_sql(engine):
    ruta_sql = os.path.join(os.path.dirname(__file__),
                            "scripts", "control_inventario.sql")

    if not os.path.exists(ruta_sql):
        return

    try:
        with open(ruta_sql, "r", encoding="utf-8") as f:
            contenido_sql = f.read()

        # Quitar referencias absolutas `CONTROL_INVENTARIO`.
        contenido_procesado = re.sub(
            r"`CONTROL_INVENTARIO`\.|CONTROL_INVENTARIO\.",
            "",
            contenido_sql,
            flags=re.IGNORECASE
        )

        # Eliminar comandos que no voy a usar
        lineas = contenido_procesado.splitlines()
        lineas_limpias = []
        for linea in lineas:
            linea_strip = linea.strip()
            if (
                linea_strip.startswith("--")
                or "CREATE SCHEMA" in linea_strip.upper()
                or "USE " in linea_strip.upper()
                or "=@OLD_" in linea_strip
                or "SET SQL_MODE=" in linea_strip
            ):
                continue
            lineas_limpias.append(linea)

        # unir todo el script limpio
        script_final = "\n".join(lineas_limpias)
        with engine.begin() as conn:
            conn.execute(text(script_final))

    except Exception as e:
        raise e


def init_database():
    try:
        # me aprovecho de sqlalchemy para crear la base de datos de una vez
        if not database_exists(settings.DATABASE_URL):
            create_database(settings.DATABASE_URL)

        url_conexion = settings.DATABASE_URL
        if "?" not in url_conexion:
            url_conexion += "?client_flag=65536"
        else:
            url_conexion += "&client_flag=65536"

        temp_engine = create_engine(url_conexion)
        inspector = inspect(temp_engine)
        tablas_existentes = inspector.get_table_names()

        # necesito verificar que la base de datos tenga tablas
        if not tablas_existentes:
            script_sql(temp_engine)

        temp_engine.dispose()
    except Exception as e:
        print("Error al crear base de datos:", e)


init_database()

# El engine es la conexion con la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Fabrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI. Abre una sesión de base de datos,
    la entrega al endpoint, y la cierra cuando el request termina.

    Uso en un endpoint:
        def mi_endpoint(db: Session = Depends(get_db)):
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
