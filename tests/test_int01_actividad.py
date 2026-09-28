import sys

import pytest


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


@pytest.fixture()
def base(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    _app_fresco()

    from app.db.migrar import migrar

    migrar()
    return base_temporal


def test_registrar_y_leer(base):
    from app.actividad.registrar import registrar
    from app.db.conexion import conectar

    id_fila = registrar(
        actor="dashboard",
        tipo="solicitada",
        accion="confirmar_pago",
        resumen="Se confirmó el pago de la oficina 204.",
        area="pagos",
        referencia="pago-12",
        origen_dato="sintetico",
    )

    conexion = conectar()
    try:
        conexion.row_factory = None
        fila = conexion.execute(
            "SELECT actor, persona, tipo, accion, area, referencia, resumen, origen_dato "
            "FROM actividad WHERE id = ?",
            (id_fila,),
        ).fetchone()
    finally:
        conexion.close()

    assert fila == (
        "dashboard",
        None,
        "solicitada",
        "confirmar_pago",
        "pagos",
        "pago-12",
        "Se confirmó el pago de la oficina 204.",
        "sintetico",
    )


def test_actor_invalido_falla(base):
    from app.actividad.registrar import registrar

    with pytest.raises(ValueError):
        registrar(actor="tercero", tipo="solicitada", accion="x", resumen="x")


def test_tipo_invalido_falla(base):
    from app.actividad.registrar import registrar

    with pytest.raises(ValueError):
        registrar(actor="vania", tipo="inventado", accion="x", resumen="x")
