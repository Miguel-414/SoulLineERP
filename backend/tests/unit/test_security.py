"""
tests/unit/test_security.py
Pruebas unitarias para app.core.security.

Validan la lógica de negocio pura (hash, verificación, JWT) sin
necesitar base de datos ni servidor HTTP.
"""

import time
import pytest
from unittest.mock import patch

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)


# ═══════════════════════════════════════════════════════════════════
# hash_password
# ═══════════════════════════════════════════════════════════════════

class TestHashPassword:
    """Pruebas para hash_password."""

    def test_retorna_string(self):
        """hash_password debe retornar un string."""
        resultado = hash_password("miContraseña123")
        assert isinstance(resultado, str)

    def test_hash_no_es_igual_al_texto_plano(self):
        """El hash nunca debe ser igual a la contraseña original."""
        plain = "secreto"
        assert hash_password(plain) != plain

    def test_dos_hashes_del_mismo_texto_son_distintos(self):
        """bcrypt genera un salt aleatorio: dos hashes del mismo texto difieren."""
        plain = "mismaContraseña"
        hash1 = hash_password(plain)
        hash2 = hash_password(plain)
        assert hash1 != hash2

    def test_hash_contrasena_vacia(self):
        """Una contraseña vacía también debe generar un hash válido."""
        resultado = hash_password("")
        assert isinstance(resultado, str)
        assert len(resultado) > 0

    def test_hash_contrasena_larga(self):
        """Contraseñas muy largas deben ser manejadas sin error."""
        larga = "a" * 200
        resultado = hash_password(larga)
        assert isinstance(resultado, str)


# ═══════════════════════════════════════════════════════════════════
# verify_password
# ═══════════════════════════════════════════════════════════════════

class TestVerifyPassword:
    """Pruebas para verify_password."""

    def test_contrasena_correcta_retorna_true(self):
        """verify_password debe retornar True cuando la contraseña coincide."""
        plain = "correcta123"
        hashed = hash_password(plain)
        assert verify_password(plain, hashed) is True

    def test_contrasena_incorrecta_retorna_false(self):
        """verify_password debe retornar False cuando la contraseña no coincide."""
        hashed = hash_password("original")
        assert verify_password("incorrecta", hashed) is False

    def test_cadena_vacia_vs_hash_de_cadena_vacia(self):
        """Cadena vacía debe verificar correctamente contra su propio hash."""
        hashed = hash_password("")
        assert verify_password("", hashed) is True

    def test_contrasena_con_espacios(self):
        """Contraseñas con espacios deben ser tratadas exactamente."""
        plain = "con espacios "
        hashed = hash_password(plain)
        assert verify_password(plain, hashed) is True
        assert verify_password("con espacios", hashed) is False

    def test_es_case_sensitive(self):
        """La verificación debe ser sensible a mayúsculas/minúsculas."""
        plain = "MiPass"
        hashed = hash_password(plain)
        assert verify_password("mipass", hashed) is False
        assert verify_password("MIPASS", hashed) is False
        assert verify_password("MiPass", hashed) is True

    def test_hash_invalido_lanza_excepcion(self):
        """
        Un hash malformado (sin prefijo bcrypt válido) hace que passlib lance
        UnknownHashError en lugar de retornar False.

        COMPORTAMIENTO ACTUAL: verify_password no captura esta excepción.
        Es recomendable envolver pwd_context.verify en un try/except en
        security.py para que retorne False en lugar de propagar el error.
        """
        from passlib.exc import UnknownHashError
        with pytest.raises(UnknownHashError):
            verify_password("cualquier", "hash_invalido_no_bcrypt")


# ═══════════════════════════════════════════════════════════════════
# create_access_token
# ═══════════════════════════════════════════════════════════════════

class TestCreateAccessToken:
    """Pruebas para create_access_token."""

    def test_retorna_string(self):
        """create_access_token debe retornar un string."""
        token = create_access_token("usuario1")
        assert isinstance(token, str)

    def test_token_tiene_tres_partes_jwt(self):
        """Un JWT válido tiene exactamente tres segmentos separados por '.'."""
        token = create_access_token("usuario1")
        partes = token.split(".")
        assert len(partes) == 3

    def test_distintos_sujetos_generan_distintos_tokens(self):
        """Sujetos diferentes deben producir tokens diferentes."""
        token_a = create_access_token("usuarioA")
        token_b = create_access_token("usuarioB")
        assert token_a != token_b

    def test_mismo_sujeto_dos_momentos_distintos(self):
        """El mismo sujeto en dos instantes puede generar tokens distintos (exp diferente)."""
        token1 = create_access_token("usuario1")
        time.sleep(1)
        token2 = create_access_token("usuario1")
        # No es garantía que sean distintos (depende del reloj), pero sí deben ser válidos
        assert decode_access_token(
            token1) == decode_access_token(token2) == "usuario1"

    def test_sujeto_numerico(self):
        """El sujeto puede ser un entero (se convierte a string internamente)."""
        token = create_access_token(42)
        assert decode_access_token(token) == "42"

    def test_sujeto_con_caracteres_especiales(self):
        """El sujeto puede contener caracteres especiales."""
        token = create_access_token("user@dominio.com")
        assert decode_access_token(token) == "user@dominio.com"


# ═══════════════════════════════════════════════════════════════════
# decode_access_token
# ═══════════════════════════════════════════════════════════════════

class TestDecodeAccessToken:
    """Pruebas para decode_access_token."""

    def test_decodifica_sujeto_correctamente(self):
        """decode_access_token debe retornar el mismo sujeto que se usó al crear."""
        sujeto = "miguel"
        token = create_access_token(sujeto)
        assert decode_access_token(token) == sujeto

    def test_token_invalido_retorna_none(self):
        """Un token aleatorio inválido debe retornar None."""
        assert decode_access_token("token.invalido.aqui") is None

    def test_token_vacio_retorna_none(self):
        """Una cadena vacía debe retornar None."""
        assert decode_access_token("") is None

    def test_token_manipulado_retorna_none(self):
        """Un token con la firma alterada debe retornar None."""
        token = create_access_token("usuario")
        partes = token.split(".")
        # Modificar la firma (tercera parte)
        token_manipulado = f"{partes[0]}.{partes[1]}.firmaFalsa"
        assert decode_access_token(token_manipulado) is None

    def test_token_expirado_retorna_none(self):
        """Un token con expiración en el pasado debe retornar None."""
        from datetime import datetime, timedelta, timezone
        from jose import jwt
        from app.core.config import settings

        payload = {
            "sub": "usuario_expirado",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=5),
        }
        token_expirado = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        assert decode_access_token(token_expirado) is None

    def test_token_firmado_con_clave_incorrecta_retorna_none(self):
        """Un token firmado con otra clave secreta debe retornar None."""
        from datetime import datetime, timedelta, timezone
        from jose import jwt
        from app.core.config import settings

        payload = {
            "sub": "usuario",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
        }
        token_malo = jwt.encode(
            payload, "clave_incorrecta", algorithm=settings.ALGORITHM)
        assert decode_access_token(token_malo) is None

    def test_ciclo_completo_crear_y_decodificar(self):
        """Ciclo de ida y vuelta: crear token → decodificar → obtener sujeto original."""
        sujeto = "ciclo_completo"
        token = create_access_token(sujeto)
        resultado = decode_access_token(token)
        assert resultado == sujeto
