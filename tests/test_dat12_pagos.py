from tests.test_dat11_contratos import _confirmar, cliente

def _contrato(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "204"})
    inquilino_id = _confirmar(cliente, "/api/inquilinos", {"titular": "Titular Sintético 01"})
    return _confirmar(cliente, "/api/contratos", {"oficina_id": oficina_id, "inquilino_id": inquilino_id})

def test_pago_se_confirma_antes_de_aparecer(cliente):
    contrato_id = _contrato(cliente)
    pendiente = cliente.post("/api/pagos", json={"contrato_id": contrato_id, "precio": 5000})
    assert pendiente.status_code == 201
    assert cliente.get("/api/pagos").json() == []
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200

def test_registrar_pago_deja_pendiente_hasta_confirmarlo(cliente):
    contrato_id = _contrato(cliente)
    pago_id = _confirmar(cliente, "/api/pagos", {"contrato_id": contrato_id, "estatus_pago": "pendiente"})
    pendiente = cliente.post("/api/pagos/registrar", json={"contrato_id": contrato_id, "forma_pago": "transferencia"})
    assert pendiente.status_code == 200
    assert cliente.get(f"/api/pagos/{pago_id}").json()["estatus_pago"] == "pendiente"
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200
    assert cliente.get(f"/api/pagos/{pago_id}").json()["estatus_pago"] == "pagado"
