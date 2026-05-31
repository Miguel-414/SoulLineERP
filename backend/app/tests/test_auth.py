"""
Tests del módulo de autenticación, usuarios y roles.

Convención de nombres:
    test_<qué_se_prueba>_<condición_o_resultado_esperado>

Cada función es independiente — el orden no importa.
"""

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


# ── Login ─────────────────────────────────────────────────────────────────────

def test_login_superadmin_exitoso(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": settings.MASTER_ADMIN_USERNAME,
            "password": settings.MASTER_ADMIN_PASSWORD,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_contrasena_incorrecta_retorna_401(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": settings.MASTER_ADMIN_USERNAME,
              "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_usuario_inexistente_retorna_401(client: TestClient):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "noexiste", "password": "noexiste"},
    )
    assert response.status_code == 401


# ── /me ───────────────────────────────────────────────────────────────────────

def test_get_me_retorna_datos_del_usuario_autenticado(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["nombre_usuario"] == settings.MASTER_ADMIN_USERNAME


def test_get_me_sin_token_retorna_401(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


# ── Roles ─────────────────────────────────────────────────────────────────────

def test_listar_roles_retorna_al_menos_superadmin(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/roles/", headers=auth_headers)
    assert response.status_code == 200
    nombres = [r["nombre"] for r in response.json()]
    assert "superadmin" in nombres


def test_crear_rol_nuevo(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/roles/",
        json={"nombre": "operario", "descripcion": "Usuario de operaciones"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["nombre"] == "operario"


def test_crear_rol_duplicado_retorna_400(client: TestClient, auth_headers: dict):
    payload = {"nombre": "rol_unico", "descripcion": "desc"}
    client.post("/api/v1/roles/", json=payload, headers=auth_headers)
    response = client.post(
        "/api/v1/roles/", json=payload, headers=auth_headers)
    assert response.status_code == 400


def test_eliminar_rol_superadmin_retorna_403(client: TestClient, auth_headers: dict):
    # Obtener el id del rol superadmin
    roles = client.get("/api/v1/roles/", headers=auth_headers).json()
    id_superadmin = next(r["id_rol"]
                         for r in roles if r["nombre"] == "superadmin")
    response = client.delete(
        f"/api/v1/roles/{id_superadmin}", headers=auth_headers)
    assert response.status_code == 403


# ── Registro de usuarios ──────────────────────────────────────────────────────

def _get_id_superadmin_rol(client: TestClient, headers: dict) -> int:
    roles = client.get("/api/v1/roles/", headers=headers).json()
    return next(r["id_rol"] for r in roles if r["nombre"] == "superadmin")


def test_register_usuario_exitoso(client: TestClient, auth_headers: dict):
    id_rol = _get_id_superadmin_rol(client, auth_headers)
    response = client.post(
        "/api/v1/auth/register",
        json={
            "persona": {
                "primer_nombre": "Ana",
                "primer_apellido": "López",
                "nombre": "Ana López",
                "email": "ana@test.com",
                "direccion": "Calle 1",
                "telefono": "3000000001",
            },
            "usuario": {
                "nombre_usuario": "alopez",
                "contrasena": "Pass1234!",
                "id_rol": id_rol,
            },
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["nombre_usuario"] == "alopez"
    # La contraseña nunca debe aparecer en la respuesta
    assert "contrasena" not in response.json()


def test_register_email_duplicado_retorna_400(client: TestClient, auth_headers: dict):
    id_rol = _get_id_superadmin_rol(client, auth_headers)
    payload = {
        "persona": {
            "primer_nombre": "Pedro",
            "primer_apellido": "Ríos",
            "nombre": "Pedro Ríos",
            "email": "pedro@test.com",
            "direccion": "Calle 2",
            "telefono": "3000000002",
        },
        "usuario": {"nombre_usuario": "prios", "contrasena": "Pass1234!", "id_rol": id_rol},
    }
    client.post("/api/v1/auth/register", json=payload, headers=auth_headers)
    # Segundo intento con el mismo email, distinto username
    payload["usuario"]["nombre_usuario"] = "prios2"
    response = client.post("/api/v1/auth/register",
                           json=payload, headers=auth_headers)
    assert response.status_code == 400


def test_register_rol_inexistente_retorna_400(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "persona": {
                "primer_nombre": "X",
                "primer_apellido": "Y",
                "nombre": "XY",
                "email": "xy@test.com",
                "direccion": "Dir",
                "telefono": "3000000099",
            },
            "usuario": {"nombre_usuario": "xy_user", "contrasena": "Pass1234!", "id_rol": 9999},
        },
        headers=auth_headers,
    )
    assert response.status_code == 400


def test_eliminar_superadmin_retorna_403(client: TestClient, auth_headers: dict):
    usuarios = client.get("/api/v1/auth/usuarios", headers=auth_headers).json()
    id_admin = next(
        u["id_usuario"] for u in usuarios
        if u["nombre_usuario"] == settings.MASTER_ADMIN_USERNAME
    )
    response = client.delete(
        f"/api/v1/auth/usuarios/{id_admin}", headers=auth_headers)
    assert response.status_code == 403


# ── Personas ──────────────────────────────────────────────────────────────────

def test_crear_persona_independiente(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/personas/",
        json={
            "primer_nombre": "Carlos",
            "primer_apellido": "Méndez",
            "nombre": "Carlos Méndez",
            "email": "carlos@test.com",
            "direccion": "Av. 5",
            "telefono": "3001111111",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["email"] == "carlos@test.com"


def test_obtener_persona_inexistente_retorna_404(client: TestClient, auth_headers: dict):
    response = client.get("/api/v1/personas/99999", headers=auth_headers)
    assert response.status_code == 404
