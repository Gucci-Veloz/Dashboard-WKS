from tests.test_dat09_oficinas import cliente

def _confirmar(cliente, ruta, cuerpo):
    pendiente = cliente.post(ruta, json=cuerpo)
    assert pendiente.status_code == 201
    respuesta = cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar")
    assert respuesta.status_code == 200
    return respuesta.json()["registro_id"]

def test_contrato_exige_referencias_oficiales_y_se_confirma(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "204"})
    inquilino_id = _confirmar(cliente, "/api/inquilinos", {"titular": "Titular Sintético 01"})
    pendiente = cliente.post("/api/contratos", json={"oficina_id": oficina_id, "inquilino_id": inquilino_id, "inicio": "2026-01-01"})
    assert pendiente.status_code == 201
    assert cliente.get("/api/contratos").json() == []
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200

def test_contrato_con_oficina_inexistente_falla_con_mensaje_humano(cliente):
    respuesta = cliente.post("/api/contratos", json={"oficina_id": 9999})
    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "La oficina indicada no existe."
