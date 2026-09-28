from tests.test_dat09_oficinas import cliente

def test_inquilino_se_confirma_antes_de_aparecer(cliente):
    creada = cliente.post("/api/inquilinos", json={"titular": "Titular Sintético 01"})
    assert creada.status_code == 201
    assert cliente.get("/api/inquilinos").json() == []
    confirmado = cliente.post(f"/api/cambios/{creada.json()['id']}/confirmar")
    assert confirmado.status_code == 200
    assert cliente.get(f"/api/inquilinos/{confirmado.json()['registro_id']}").status_code == 200

def test_inquilino_inexistente_da_mensaje_humano(cliente):
    respuesta = cliente.get("/api/inquilinos/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "No existe un inquilino con ese número de registro."
