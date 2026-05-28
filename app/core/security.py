from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Recibe la contraseña en texto plano y retorna su hash."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña ingresada contra el hash guardado en la BD."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: Any) -> str:
    """
    Crea un JWT (JSON Web Token).

    El token contiene:
      - sub: el identificador del usuario (normalmente el nombre de usuario o id)
      - exp: la fecha/hora de expiración
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {"sub": str(subject), "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> str:
    """
    Decodifica el JWT y retorna el 'sub' (nombre de usuario).
    Retorna None si el token es inválido o expiró.
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return payload.get("sub")
    except JWTError:
        return None
