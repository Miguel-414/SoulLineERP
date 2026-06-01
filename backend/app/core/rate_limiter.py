"""
Configuración de Rate Limiting para la API.
Utiliza slowapi para proteger endpoints contra abuso.
"""

# from slowapi import Limiter
# from slowapi.util import get_remote_address

# limiter = Limiter(key_func=get_remote_address)

# Límites predefinidos
RATE_LIMITS = {
    "auth": "5/minute",              # Login: 5 intentos por minuto
    "default": "100/minute",         # General: 100 requests por minuto
    "search": "30/minute",           # Búsquedas: 30 por minuto
    "write": "50/minute",            # POST/PUT/DELETE: 50 por minuto
}
