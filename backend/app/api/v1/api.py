from fastapi import APIRouter

from app.api.v1.endpoints import roles
from app.api.v1.endpoints import auth, facturas, objetos, personas, ubicaciones, movimientos

api_router = APIRouter()

api_router.include_router(
    auth.router,       prefix="/auth",       tags=["Autenticación"])
api_router.include_router(
    roles.router,      prefix="/roles",      tags=["Roles"])
api_router.include_router(
    personas.router,   prefix="/personas",   tags=["Personas"])
api_router.include_router(
    objetos.router,    prefix="/objetos",    tags=["Objetos"])
api_router.include_router(
    facturas.router,   prefix="/facturas",   tags=["Facturas"])
api_router.include_router(
    ubicaciones.router, prefix="/ubicaciones", tags=["Ubicaciones"])
api_router.include_router(
    movimientos.router, prefix="/movimientos", tags=["Movimientos"])
