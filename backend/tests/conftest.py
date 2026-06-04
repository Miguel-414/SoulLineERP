"""
conftest.py — Configuración global de fixtures para Pytest.

Usa SQLite en memoria para que las pruebas no necesiten una base de
datos MySQL real. FastAPI TestClient permite lanzar peticiones HTTP
sin levantar un servidor Uvicorn.
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ── Parchear init_database y seeder ANTES de importar app ────────────────────
# database.py llama a init_database() al importarse (nivel de módulo),
# lo que intenta conectar a MySQL. Lo silenciamos para tests.
with patch("sqlalchemy_utils.database_exists", return_value=True), \
        patch("app.core.database.script_sql"), \
        patch("app.core.seeder.run"):
    from app.main import app as fastapi_app

from app.api.deps import get_db
from app.models.base import Base
# Importar TODOS los modelos para que SQLAlchemy resuelva todas las FK
import app.models.auth      # noqa: F401
import app.models.personal  # noqa: F401
import app.models.inventario  # noqa: F401
import app.models.financiero  # noqa: F401

from sqlalchemy.pool import StaticPool

# ── Motor SQLite en memoria ───────────────────────────────────────────────────
# StaticPool garantiza que todas las conexiones compartan exactamente
# la misma BD en memoria — imprescindible para tests con FastAPI TestClient.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# ── Fixtures de sesión y cliente ──────────────────────────────────────────────

@pytest.fixture(scope="function")
def db():
    """
    Crea todas las tablas antes de cada test y las elimina al terminar.
    Garantiza que cada prueba empiece con una BD limpia.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    TestClient de FastAPI con la dependencia get_db sustituida por la
    sesión SQLite en memoria.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    fastapi_app.dependency_overrides[get_db] = override_get_db
    # Silenciar el seeder del lifespan (requiere MySQL real)
    with patch("app.core.seeder.run"):
        with TestClient(fastapi_app) as c:
            yield c
    fastapi_app.dependency_overrides.clear()


# ── Fixtures de datos base ────────────────────────────────────────────────────

@pytest.fixture()
def rol_admin(db):
    """Crea y retorna un Rol 'admin' en la BD de prueba."""
    from app.models.auth import Rol
    rol = Rol(nombre="admin", descripcion="Administrador del sistema")
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


@pytest.fixture()
def usuario_base(db, rol_admin):
    """
    Crea una Persona + Usuario con contraseña hasheada listos para
    ser usados en pruebas que requieran autenticación.
    """
    from app.models.personal import Persona
    from app.models.auth import Usuario
    from app.core.security import hash_password

    persona = Persona(
        primer_nombre="Test",
        primer_apellido="User",
        nombre="Test User",
        email="testuser@example.com",
        direccion="Calle Falsa 123",
        telefono="3000000000",
    )
    db.add(persona)
    db.flush()

    usuario = Usuario(
        nombre_usuario="testuser",
        contrasena=hash_password("testpass123"),
        id_rol=rol_admin.id_rol,
        id_persona=persona.id_persona,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@pytest.fixture()
def auth_headers(client, usuario_base):
    """
    Realiza el login y retorna el header Authorization listo para
    usarse en peticiones protegidas.
    """
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser",
            "password": "testpass123",
            "grant_type": "password",
        },
    )
    assert response.status_code == 200, (
        f"Login falló en fixture auth_headers: {response.json()}"
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def tipo_activo_base(client, auth_headers):
    """Crea un TipoActivo de prueba y lo retorna."""
    response = client.post(
        "/api/v1/objetos/tipos-activo",
        json={"nombre": "Electrónico", "descripcion": "Equipos electrónicos"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture()
def objeto_base(client, auth_headers, tipo_activo_base):
    """Crea un Objeto de prueba (tipo 'unico') y lo retorna."""
    response = client.post(
        "/api/v1/objetos/",
        json={
            "tipo_objeto": "unico",
            "nombre": "Laptop Dell",
            "descripcion": "Laptop de prueba",
            "marca": "Dell",
            "modelo": "Inspiron 15",
            "id_tipo_activo": tipo_activo_base["id_tipo_activo"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()
