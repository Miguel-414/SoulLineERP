import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.api.v1.middlewares.logging_middleware import LoggingMiddleware
from app.core.config import settings
from app.core.database import SessionLocal
from app.core import seeder

# TODO Queda pendiente implementar la logica para el manejo de objetos acumulables
# todo Los models para la logica de acumulables
# ? falta: implementar en capa crud y en capa de endpoints

# Configuración básica de logging — muestra INFO en consola con timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# ── Eventos de ciclo de vida ──────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se ejecuta una sola vez cuando arranca el servidor.
    Corre el seeder para garantizar que el admin maestro exista.
    """
    db = SessionLocal()
    try:
        seeder.run(db)
    finally:
        db.close()

    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ── Middlewares ───────────────────────────────────────────────────────────────
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Rutas ─────────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
def root():
    """Endpoint de salud — confirma que el servidor está corriendo."""
    return {"status": "ok", "proyecto": settings.PROJECT_NAME}
