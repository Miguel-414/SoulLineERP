"""
conftest.py — configuración y fixtures compartidos por todos los tests.

Estrategia de aislamiento:
  - Las tablas se crean UNA sola vez por sesión de pytest (scope="session").
  - El seeder también corre UNA sola vez: crea el superadmin.
  - Cada test individual obtiene su propia conexión. Los datos que el
    test crea se descartan al final mediante rollback (savepoint de SQLite).
  - Los datos del seeder quedan intactos entre tests porque se insertaron
    fuera del savepoint.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings
from app.core.database import get_db
from app.core import seeder
from app.main import app
from app.models.base import Base

TEST_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_test)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Crea tablas y ejecuta el seeder UNA vez para toda la sesión de tests."""
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        seeder.run(db)
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def db(setup_database) -> Session:
    """
    Fixture de BD por test: usa un savepoint de SQLite para poder hacer
    rollback al final del test sin afectar los datos del seeder.
    """
    connection = engine_test.connect()
    # Comenzar una transacción externa (el seeder ya hizo commit sobre ella)
    transaction = connection.begin()
    # Savepoint: los cambios del test se descartan aquí al final
    connection.begin_nested()

    session = TestingSessionLocal(bind=connection)

    # Cuando SQLAlchemy hace commit dentro del test, lo redirigimos
    # al savepoint para que no escape a la transacción externa.
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and not trans._parent.nested:
            connection.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db: Session, setup_database) -> TestClient:
    """TestClient con la BD de test inyectada."""
    def override_get_db():
        yield db

    # Evita que on_startup intente conectar a MySQL real
    import app.main as main_module
    original_startup = None

    app.dependency_overrides[get_db] = override_get_db

    # Reemplaza on_startup para usar la BD de test en lugar de MySQL
    from app.core import seeder as seeder_module
    original_run = seeder_module.run

    def _noop_run(_db):
        pass  # El seeder ya corrió en setup_database, no hace falta repetirlo

    seeder_module.run = _noop_run
    try:
        with TestClient(app, raise_server_exceptions=True) as c:
            yield c
    finally:
        seeder_module.run = original_run
        app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client: TestClient) -> dict:
    """Header Authorization listo para usar en peticiones autenticadas."""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": settings.MASTER_ADMIN_USERNAME,
            "password": settings.MASTER_ADMIN_PASSWORD,
        },
    )
    assert response.status_code == 200, f"Login falló: {response.text}"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
