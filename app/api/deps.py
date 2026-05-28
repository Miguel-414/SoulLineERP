"""
Dependencias de FastAPI.

Una "dependencia" es una función que FastAPI ejecuta antes del endpoint
para preparar algo que el endpoint necesita: la sesión de BD, el usuario
autenticado, etc.

Uso en un endpoint:
    from app.api.deps import get_db, get_current_user

    @router.get("/algo")
    def mi_endpoint(
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user),
    ):
        ...
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.crud.crud_auth import get_usuario_by_nombre
from app.models.auth import Usuario

# OAuth2PasswordBearer indica a FastAPI dónde esperar el token.
# El cliente debe mandar: Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Usuario:
    """
    Decodifica el JWT del header Authorization y retorna el usuario activo.
    Si el token es inválido o el usuario no existe, lanza HTTP 401.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    nombre_usuario = decode_access_token(token)
    if not nombre_usuario:
        raise credentials_exception

    user = get_usuario_by_nombre(db, nombre_usuario)
    if not user:
        raise credentials_exception

    return user


# Re-exportar get_db para que los endpoints solo importen desde deps
__all__ = ["get_db", "get_current_user"]