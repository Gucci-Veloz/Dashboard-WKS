import sys
from datetime import date, datetime, timedelta, timezone

import pytest
from fastapi.testclient import TestClient


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


@pytest.fixture()
def cliente(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "secreto-largo")
    _app_fresco()

    from app.db.migrar import migrar

    migrar()

    from app.fuentes.cargar import cargar

    cargar("sintetica", escenario="con_atencion")

    from app.main import app

    return TestClient(app)


CREDENCIAL = {"Authorization": "Bearer secreto-largo"}
RUTA_PREFERENCIAS = "/api/vania/preferencias-avisos"
RUTA_AVISOS = "/api/vania/avisos?persona=grecia"


def _guardar_preferencia(cliente, hasta):
    return cliente.patch(
        RUTA_PREFERENCIAS,
        headers=CREDENCIAL,
        json={"persona": "grecia", "tipo_evento": "contratos", "hasta": hasta},
    )


def test_silenciar_contratos_vence_y_se_puede_quitar_sin_ocultarlos_del_estado(cliente):
    estado_antes = cliente.get("/api/estado").json()
    assert any(asunto["area"] == "contratos" for asunto in estado_antes["asuntos"])

    futuro = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    respuesta = _guardar_preferencia(cliente, futuro)
    assert respuesta.status_code == 200

    preferencias = cliente.get(
        RUTA_PREFERENCIAS,
        params={"persona": "grecia"},
        headers=CREDENCIAL,
    )
    assert preferencias.status_code == 200
    assert preferencias.json()["preferencias"] == [
        {"persona": "grecia", "tipo_evento": "contratos", "hasta": futuro}
    ]

    aviso_silenciado = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert aviso_silenciado.status_code == 200
    assert aviso_silenciado.json()["cantidad"] == 2
    assert all(
        asunto["area"] != "contratos"
        for asunto in aviso_silenciado.json()["asuntos"]
    )
    assert cliente.get("/api/estado").json()["asuntos"] == estado_antes["asuntos"]

    pasado = (datetime.now(timezone.utc) - timedelta(seconds=1)).isoformat()
    assert _guardar_preferencia(cliente, pasado).status_code == 200
    aviso_tras_vencer = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert aviso_tras_vencer.status_code == 200
    assert [asunto["area"] for asunto in aviso_tras_vencer.json()["asuntos"]] == [
        "contratos"
    ]

    assert _guardar_preferencia(cliente, None).status_code == 200
    assert cliente.get(RUTA_AVISOS, headers=CREDENCIAL).status_code == 204
    quitada = cliente.patch(
        RUTA_PREFERENCIAS + "/quitar",
        params={"persona": "grecia", "tipo_evento": "contratos"},
        headers=CREDENCIAL,
    )
    assert quitada.status_code == 204
    aviso_tras_quitar = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert aviso_tras_quitar.status_code == 200
    assert [asunto["area"] for asunto in aviso_tras_quitar.json()["asuntos"]] == [
        "contratos"
    ]


def test_un_asunto_no_se_repite_hasta_que_cambia_o_se_reabre(cliente):
    primer_aviso = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert primer_aviso.status_code == 200
    assert primer_aviso.json()["cantidad"] == 3
    assert cliente.get(RUTA_AVISOS, headers=CREDENCIAL).status_code == 204

    from app.db.conexion import conectar

    conexion = conectar()
    try:
        nueva_fecha = (date.today() + timedelta(days=5)).isoformat()
        conexion.execute("UPDATE contratos SET fin = ? WHERE id = 4", (nueva_fecha,))
        conexion.commit()
    finally:
        conexion.close()

    aviso_cambiado = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert aviso_cambiado.status_code == 200
    assert [asunto["id"] for asunto in aviso_cambiado.json()["asuntos"]] == ["contrato-4"]

    conexion = conectar()
    try:
        fecha_lejana = (date.today() + timedelta(days=200)).isoformat()
        conexion.execute("UPDATE contratos SET fin = ? WHERE id = 4", (fecha_lejana,))
        conexion.commit()
    finally:
        conexion.close()
    assert cliente.get(RUTA_AVISOS, headers=CREDENCIAL).status_code == 204

    conexion = conectar()
    try:
        conexion.execute("UPDATE contratos SET fin = ? WHERE id = 4", (nueva_fecha,))
        conexion.commit()
    finally:
        conexion.close()
    aviso_reabierto = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert aviso_reabierto.status_code == 200
    assert [asunto["id"] for asunto in aviso_reabierto.json()["asuntos"]] == ["contrato-4"]


def test_contrato_no_se_repite_al_dia_siguiente_por_tener_un_dia_menos(
    cliente, monkeypatch
):
    from app.api import avisos
    from app.db.conexion import conectar

    hoy = date(2030, 1, 10)

    class FechaControlada(date):
        fecha_actual = hoy

        @classmethod
        def today(cls):
            return cls.fecha_actual

    conexion = conectar()
    try:
        conexion.execute(
            "UPDATE contratos SET fin = ? WHERE id = 4",
            ((hoy + timedelta(days=12)).isoformat(),),
        )
        conexion.commit()
    finally:
        conexion.close()

    monkeypatch.setattr(avisos, "date", FechaControlada)
    primer_aviso = cliente.get(RUTA_AVISOS, headers=CREDENCIAL)
    assert primer_aviso.status_code == 200
    contrato = next(
        asunto
        for asunto in primer_aviso.json()["asuntos"]
        if asunto["id"] == "contrato-4"
    )
    assert contrato["frase"] == "La oficina 104 vence en 12 días."

    FechaControlada.fecha_actual = hoy + timedelta(days=1)
    assert cliente.get(RUTA_AVISOS, headers=CREDENCIAL).status_code == 204


@pytest.mark.parametrize(
    ("metodo", "ruta", "kwargs"),
    [
        ("get", "/api/vania/avisos?persona=grecia", {}),
        ("get", RUTA_PREFERENCIAS, {}),
        (
            "patch",
            RUTA_PREFERENCIAS,
            {"json": {"persona": "grecia", "tipo_evento": "contratos", "hasta": None}},
        ),
        (
            "patch",
            RUTA_PREFERENCIAS + "/quitar",
            {"params": {"persona": "grecia", "tipo_evento": "contratos"}},
        ),
    ],
)
def test_sin_credencial_devuelve_401(cliente, metodo, ruta, kwargs):
    respuesta = getattr(cliente, metodo)(ruta, **kwargs)
    assert respuesta.status_code == 401
