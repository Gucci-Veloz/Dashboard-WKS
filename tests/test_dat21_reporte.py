from datetime import date

from fastapi.testclient import TestClient
from tests.test_dat09_oficinas import cliente


def _confirmar(cliente, ruta, datos):
    pendiente = cliente.post(ruta, json=datos)
    assert pendiente.status_code in {200, 201}
    confirmado = cliente.post(f"/api/cambios/{pendiente.json()['id']}/confirmar")
    assert confirmado.status_code == 200
    return pendiente.json()["id"], confirmado.json()["registro_id"]


def test_reporte_solo_muestra_confirmados_del_dia(cliente):
    from app.main import app

    confirmado_id, _ = _confirmar(cliente, "/api/inquilinos", {"titular": "Ana"})
    pendiente = cliente.post("/api/inquilinos", json={"titular": "Beto"})

    reporte = TestClient(app).get("/api/reporte", params={"fecha": date.today().isoformat()})

    assert reporte.status_code == 200
    assert [fila["id"] for fila in reporte.json()] == [confirmado_id]
    assert pendiente.json()["id"] not in [fila["id"] for fila in reporte.json()]
    assert reporte.json()[0]["concepto"] == "Alta de inquilino"


def test_reporte_respeta_el_dia_de_queretaro(cliente):
    from app.db.conexion import conectar_con_filas

    cambio_id, _ = _confirmar(cliente, "/api/oficinas", {"numero": "204"})
    conexion = conectar_con_filas()
    try:
        conexion.execute(
            "UPDATE cambios SET confirmado_en = '2026-09-27 05:30:00' WHERE id = ?", (cambio_id,)
        )
        conexion.commit()
    finally:
        conexion.close()

    respuesta = cliente.get("/api/reporte", params={"fecha": "2026-09-26"})
    siguiente = cliente.get("/api/reporte", params={"fecha": "2026-09-27"})

    assert [fila["id"] for fila in respuesta.json()] == [cambio_id]
    assert respuesta.json()[0]["fecha"] == "2026-09-26 23:30"
    assert siguiente.json() == []


def test_pago_muestra_estatus_como_concepto(cliente):
    _, inquilino_id = _confirmar(cliente, "/api/inquilinos", {"titular": "Lucía"})
    _, oficina_id = _confirmar(cliente, "/api/oficinas", {"numero": "205"})
    _, contrato_id = _confirmar(cliente, "/api/contratos", {"oficina_id": oficina_id, "inquilino_id": inquilino_id})
    pago_id, _ = _confirmar(cliente, "/api/pagos", {"contrato_id": contrato_id, "estatus_pago": "pagado"})

    reporte = cliente.get("/api/reporte", params={"fecha": date.today().isoformat()}).json()
    pago = next(fila for fila in reporte if fila["id"] == pago_id)

    assert pago["concepto"] == "Pagado"
    assert pago["inquilino"] == "Lucía"


def test_reporte_conserva_solicitante_y_ejecutor_de_vania(cliente, monkeypatch):
    from app.main import app
    from app.seguridad.actor import ActorActual, actor_actual

    app.dependency_overrides.clear()
    app.dependency_overrides[actor_actual] = lambda: ActorActual("vania", solicitante="grecia")
    try:
        cambio_id, _ = _confirmar(cliente, "/api/inquilinos", {"titular": "María"})
    finally:
        app.dependency_overrides.clear()

    reporte = cliente.get("/api/reporte", params={"fecha": date.today().isoformat()}).json()
    fila = next(fila for fila in reporte if fila["id"] == cambio_id)
    assert fila["solicitante"] == "grecia"
    assert fila["ejecutor"] == "vania"
