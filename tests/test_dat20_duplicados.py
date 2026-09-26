from tests.test_dat11_contratos import _confirmar, cliente


MENSAJE = "Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?"


def _debe_avisar(cliente, ruta, cuerpo, area):
    respuesta = cliente.post(ruta, json=cuerpo)
    assert respuesta.status_code == 409
    assert respuesta.json()["mensaje"] == MENSAJE
    assert respuesta.json()["posible_duplicado"]["area"] == area
    permitido = cliente.post(ruta, json={**cuerpo, "crear_de_todos_modos": True})
    assert permitido.status_code == 201
    assert "id" in permitido.json()


def test_oficina_duplicada_por_numero_y_sin_coincidencia_no_avisa(cliente):
    _confirmar(cliente, "/api/oficinas", {"numero": "204"})
    _debe_avisar(cliente, "/api/oficinas", {"numero": "204"}, "oficinas")
    assert cliente.post("/api/oficinas", json={"numero": "205"}).status_code == 201


def test_inquilino_duplicado_por_titular_normalizado_o_contacto(cliente):
    _confirmar(cliente, "/api/inquilinos", {"titular": "  José   Pérez ", "contacto": "+520000000001"})
    _debe_avisar(cliente, "/api/inquilinos", {"titular": "jose pÉrez"}, "inquilinos")
    _debe_avisar(cliente, "/api/inquilinos", {"titular": "Otra persona", "contacto": "+520000000001"}, "inquilinos")


def test_contrato_duplicado_por_intervalo_de_fechas(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "204"})
    inquilino_id = _confirmar(cliente, "/api/inquilinos", {"titular": "Titular"})
    _confirmar(cliente, "/api/contratos", {"oficina_id": oficina_id, "inquilino_id": inquilino_id, "inicio": "2026-01-01", "fin": "2026-06-30"})
    _debe_avisar(cliente, "/api/contratos", {"oficina_id": oficina_id, "inquilino_id": inquilino_id, "inicio": "2026-06-01", "fin": "2026-12-31"}, "contratos")


def test_pago_duplicado_por_contrato_mes_y_precio(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "204"})
    inquilino_id = _confirmar(cliente, "/api/inquilinos", {"titular": "Titular"})
    contrato_id = _confirmar(cliente, "/api/contratos", {"oficina_id": oficina_id, "inquilino_id": inquilino_id})
    _confirmar(cliente, "/api/pagos", {"contrato_id": contrato_id, "precio": 5000, "fecha_pago": "2026-09-01"})
    _debe_avisar(cliente, "/api/pagos", {"contrato_id": contrato_id, "precio": 5000, "fecha_pago": "2026-09-30"}, "pagos")
