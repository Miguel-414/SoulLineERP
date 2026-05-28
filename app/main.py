from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    # La documentación interactiva estará en /docs
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS: permite que un frontend (ej. React en localhost:3000) llame a la API.
# En producción cambia allow_origins a la URL real de tu frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar todas las rutas de la v1 bajo /api/v1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Health"])
def root():
    """Endpoint de salud — confirma que el servidor está corriendo."""
    return {"status": "ok", "proyecto": settings.PROJECT_NAME}
