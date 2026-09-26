from tests.test_dat11_contratos import _confirmar, cliente


def test_descartar_quita_el_pendiente_sin_cambiar_el_registro(cliente):
    oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "204", "estatus": "libre"})
    pendiente = cliente.put(f"/api/oficinas/{oficina_id}", json={"estatus": "ocupada"})

    respuesta = cliente.post(f"/api/cambios/{pendiente.json()['id']}/descartar")

    assert respuesta.status_code == 200
    assert respuesta.json()["id"] == pendiente.json()["id"]
    assert cliente.get(f"/api/oficinas/{oficina_id}").json()["estatus"] == "libre"
    assert cliente.get("/api/cambios", params={"area": "oficinas", "registro_id": oficina_id}).json() == []
    actividad = cliente.get("/api/actividad").json()["resultados"]
    assert actividad[0]["accion"] == "descartar_modificacion_oficinas"


def test_descartar_un_cambio_confirmado_da_400(cliente):
    pendiente = cliente.post("/api/oficinas", json={"numero": "204"})
    assert cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar").status_code == 200

    respuesta = cliente.post(f"/api/cambios/{pendiente.json()['id']}/descartar")

    assert respuesta.status_code == 400
    assert respuesta.json()["detail"] == "No existe un cambio pendiente con ese número."
