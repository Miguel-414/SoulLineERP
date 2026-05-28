"""
Middleware de logging.

Registra cada petición HTTP con:
  - Método y ruta
  - Código de respuesta
  - Tiempo de procesamiento en milisegundos

Ejemplo de salida en consola:
  INFO  POST /api/v1/auth/login → 200  (45ms)
  INFO  GET  /api/v1/objetos/   → 401  (3ms)

Para activarlo, añadir en main.py:
    from app.api.v1.middlewares.logging_middleware import LoggingMiddleware
    app.add_middleware(LoggingMiddleware)
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("api.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "%-6s %-45s → %d  (%.0fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response
