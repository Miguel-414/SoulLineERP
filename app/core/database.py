from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.core.config import settings

# El engine es la conexion con la base de datos
# todo: averiguar que son las otras
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
