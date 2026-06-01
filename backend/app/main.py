import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from slowapi import Limiter
# from slowapi.errors import RateLimitExceeded
# from slowapi.util import get_remote_address
# from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.api.v1.middlewares.logging_middleware import LoggingMiddleware
from app.core.config import settings
from app.core.database import SessionLocal
from app.core import seeder

# Configuración básica de logging — muestra INFO en consola con timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ── Rate Limiter ──────────────────────────────────────────────────────────
# limiter = Limiter(key_func=get_remote_address)


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

# ── Rate Limiter Exception Handler ────────────────────────────────────────
# todo trabajando en implementar el rate limiting para denegar ataques DDOS

# @app.exception_handler(RateLimitExceeded)
# async def rate_limit_handler(request, exc):
#     return JSONResponse(
#         status_code=429,
#         content={"detail": "Rate limit exceeded. Too many requests."}
#     )

# ── Middlewares ───────────────────────────────────────────────────────────────
# app.state.limiter = limiter
app.add_middleware(LoggingMiddleware)

# CORS configurado desde variables de entorno (producción debe restringir)
cors_origins = settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else [
    "http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
cors_credentials = settings.CORS_CREDENTIALS if hasattr(
    settings, 'CORS_CREDENTIALS') else True

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=cors_credentials,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# ── Rutas ─────────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
# @limiter.limit("100/minute")
def root(request):
    """Endpoint de salud — confirma que el servidor está corriendo."""
    return {"status": "ok", "proyecto": settings.PROJECT_NAME}
