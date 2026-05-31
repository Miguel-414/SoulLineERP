import pytest

factura_data = {}


def test_ciclo_proveedores(client, auth_headers):
    """Evalúa creación y lectura de Proveedores."""
    proveedor_payload = {
        "nit": "900123456-1",
        "razon_social": "Distribuciones Tecnológicas SAS",
        "telefono": "3224445566",
        "email": "contacto@distritech.com"
    }
    response = client.post("/api/v1/facturas/proveedores",
                           json=proveedor_payload, headers=auth_headers)
    assert response.status_code == 201
    factura_data["id_proveedor"] = response.json()["id_proveedor"]


def test_crear_factura(client, auth_headers):
    """Evalúa la inserción de una Factura asociada al proveedor previo."""
    assert "id_proveedor" in factura_data

    factura_payload = {
        "numero_factura": "FAC-2026-001",
        "fecha_emision": "2026-05-28T00:00:00",
        "valor_total": 4500000.00,
        "id_proveedor": factura_data["id_proveedor"]
    }
    response = client.post("/api/v1/facturas/",
                           json=factura_payload, headers=auth_headers)
    assert response.status_code == 201
