from tests.test_dat11_contratos import _confirmar, cliente

def test_put_solo_cambia_al_confirmar_y_se_lista_pendiente(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "204", "estatus": "libre"})
    pendiente = cliente.put(f"/api/oficinas/{oficina_id}", json={"numero": "204", "estatus": "ocupada", "observaciones": "Cambio acordado"})
    assert pendiente.status_code == 200
    assert cliente.get(f"/api/oficinas/{oficina_id}").json()["estatus"] == "libre"
    cambios = cliente.get("/api/cambios", params={"area": "oficinas", "registro_id": oficina_id}).json()
    assert [cambio["id"] for cambio in cambios] == [pendiente.json()["id"]]
    assert cambios[0]["observaciones"] == "Cambio acordado"
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200
    assert cliente.get(f"/api/oficinas/{oficina_id}").json()["estatus"] == "ocupada"

def test_registrar_pago_solo_quita_asunto_al_confirmar(cliente):
    from app.fuentes.cargar import cargar
    cargar("sintetica", escenario="con_atencion")
    antes = cliente.get("/api/estado").json()
    pendiente = cliente.post("/api/pagos/registrar", json={"contrato_id": 8, "forma_pago": "transferencia"})
    assert pendiente.status_code == 200
    durante = cliente.get("/api/estado").json()
    assert durante["conclusion"]["cantidad"] == antes["conclusion"]["cantidad"]
    assert durante["asuntos"] == antes["asuntos"]
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200
    despues = cliente.get("/api/estado").json()
    assert despues["conclusion"]["cantidad"] == antes["conclusion"]["cantidad"] - 1

def test_baja_tambien_espera_confirmacion(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "301"})
    pendiente = cliente.delete(f"/api/oficinas/{oficina_id}")
    assert pendiente.status_code == 200
    assert cliente.get(f"/api/oficinas/{oficina_id}").status_code == 200
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200
    assert cliente.get(f"/api/oficinas/{oficina_id}").status_code == 404
