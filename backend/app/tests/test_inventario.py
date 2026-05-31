"""
Tests del módulo de inventario: tipo_activo, objetos, ubicaciones.
"""

from fastapi.testclient import TestClient


# ── Helpers ───────────────────────────────────────────────────────────────────

def _crear_tipo_activo(client: TestClient, headers: dict, nombre: str = "Equipos de cómputo") -> dict:
    r = client.post(
        "/api/v1/objetos/tipos-activo",
        json={"nombre": nombre, "descripcion": "Equipos TI"},
        headers=headers,
    )
    assert r.status_code == 201, r.text
    return r.json()


def _crear_objeto(client: TestClient, headers: dict, id_tipo: int) -> dict:
    r = client.post(
        "/api/v1/objetos/",
        json={
            "tipo_objeto": "unico",
            "nombre": "Laptop Dell",
            "descripcion": "Laptop de desarrollo",
            "marca": "Dell",
            "modelo": "XPS 15",
            "id_tipo_activo": id_tipo,
        },
        headers=headers,
    )
    assert r.status_code == 201, r.text
    return r.json()


# ── TipoActivo ────────────────────────────────────────────────────────────────

def test_crear_tipo_activo(client: TestClient, auth_headers: dict):
    ta = _crear_tipo_activo(client, auth_headers)
    assert ta["nombre"] == "Equipos de cómputo"
    assert "id_tipo_activo" in ta


def test_listar_tipos_activo(client: TestClient, auth_headers: dict):
    _crear_tipo_activo(client, auth_headers, nombre="Mobiliario")
    response = client.get("/api/v1/objetos/tipos-activo", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_actualizar_tipo_activo(client: TestClient, auth_headers: dict):
    ta = _crear_tipo_activo(client, auth_headers, nombre="Original")
    response = client.patch(
        f"/api/v1/objetos/tipos-activo/{ta['id_tipo_activo']}",
        json={"nombre": "Actualizado"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["nombre"] == "Actualizado"


def test_eliminar_tipo_activo(client: TestClient, auth_headers: dict):
    ta = _crear_tipo_activo(client, auth_headers, nombre="Para borrar")
    response = client.delete(
        f"/api/v1/objetos/tipos-activo/{ta['id_tipo_activo']}",
        headers=auth_headers,
    )
    assert response.status_code == 204


def test_obtener_tipo_activo_inexistente_retorna_404(client: TestClient, auth_headers: dict):
    response = client.get(
        "/api/v1/objetos/tipos-activo/99999", headers=auth_headers)
    assert response.status_code == 404


# ── Objetos ───────────────────────────────────────────────────────────────────

def test_crear_objeto(client: TestClient, auth_headers: dict):
    ta = _crear_tipo_activo(client, auth_headers, nombre="TI")
    obj = _crear_objeto(client, auth_headers, ta["id_tipo_activo"])
    assert obj["nombre"] == "Laptop Dell"
    assert obj["marca"] == "Dell"


def test_crear_objeto_tipo_invalido_retorna_422(client: TestClient, auth_headers: dict):
    """tipo_objeto solo acepta 'acumulable' o 'unico'."""
    ta = _crear_tipo_activo(client, auth_headers, nombre="TI2")
    response = client.post(
        "/api/v1/objetos/",
        json={
            "tipo_objeto": "invalido",
            "nombre": "Test",
            "descripcion": "Desc",
            "id_tipo_activo": ta["id_tipo_activo"],
        },
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_actualizar_objeto_parcial(client: TestClient, auth_headers: dict):
    ta = _crear_tipo_activo(client, auth_headers, nombre="TI3")
    obj = _crear_objeto(client, auth_headers, ta["id_tipo_activo"])
    response = client.patch(
        f"/api/v1/objetos/{obj['id_objeto']}",
        json={"marca": "Apple"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["marca"] == "Apple"
    # El nombre no cambió
    assert response.json()["nombre"] == "Laptop Dell"


# ── Ubicaciones ───────────────────────────────────────────────────────────────

def test_crear_ubicacion_raiz(client: TestClient, auth_headers: dict):
    response = client.post(
        "/api/v1/ubicaciones/",
        json={"nombre": "Sede Principal", "descripcion": "Oficina central"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    assert response.json()["id_zona_padre"] is None


def test_crear_ubicacion_hija(client: TestClient, auth_headers: dict):
    padre = client.post(
        "/api/v1/ubicaciones/",
        json={"nombre": "Edificio A"},
        headers=auth_headers,
    ).json()

    hija = client.post(
        "/api/v1/ubicaciones/",
        json={"nombre": "Piso 2", "id_zona_padre": padre["id_ubicacion"]},
        headers=auth_headers,
    ).json()

    assert hija["id_zona_padre"] == padre["id_ubicacion"]


def test_endpoint_sin_autenticacion_retorna_401(client: TestClient):
    """Garantiza que ningún endpoint de datos sea accesible sin token."""
    endpoints = [
        ("GET", "/api/v1/objetos/"),
        ("GET", "/api/v1/ubicaciones/"),
        ("GET", "/api/v1/roles/"),
        ("GET", "/api/v1/personas/"),
        ("GET", "/api/v1/facturas/proveedores"),
    ]
    for method, url in endpoints:
        response = client.request(method, url)
        assert response.status_code == 401, f"{method} {url} debería requerir auth"
