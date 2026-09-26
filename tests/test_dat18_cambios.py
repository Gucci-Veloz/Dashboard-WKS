import pytest


@pytest.fixture()
def base(tmp_path, monkeypatch):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    from app.db.migrar import migrar

    migrar()
    from app.db.conexion import conectar

    conexion = conectar()
    conexion.execute(
        "INSERT INTO oficinas (numero, estatus, origen_dato) VALUES ('204', 'disponible', 'manual')"
    )
    conexion.commit()
    yield conexion
    conexion.close()


def test_pendiente_no_modifica_el_dato_oficial(base):
    from app.cambios import crear_pendiente

    cambio = crear_pendiente(
        area="oficinas",
        registro_id=1,
        operacion="modificacion",
        valores_nuevos={"estatus": "ocupada"},
        solicitante="david",
        ejecutor="david",
    )

    assert base.execute("SELECT estatus FROM oficinas WHERE id = 1").fetchone()[0] == "disponible"
    assert cambio["estado"] == "pendiente"


def test_confirmar_modifica_y_guarda_historial(base):
    from app.cambios import confirmar, crear_pendiente, historial

    cambio = crear_pendiente(
        area="oficinas",
        registro_id=1,
        operacion="modificacion",
        valores_nuevos={"estatus": "ocupada"},
        solicitante="grecia",
        ejecutor="vania",
    )
    confirmado = confirmar(cambio["id"], "grecia")

    assert confirmado["estado"] == "confirmado"
    assert base.execute("SELECT estatus FROM oficinas WHERE id = 1").fetchone()[0] == "ocupada"
    cambios = historial("oficinas", 1)
    assert cambios[0]["valores_anteriores"]["estatus"] == "disponible"
    assert cambios[0]["valores_nuevos"] == {"estatus": "ocupada"}


def test_pendiente_vencido_desaparece_y_no_se_confirma(base):
    from app.cambios import confirmar, crear_pendiente, pendientes

    cambio = crear_pendiente(
        area="oficinas",
        registro_id=1,
        operacion="modificacion",
        valores_nuevos={"estatus": "ocupada"},
        solicitante="david",
        ejecutor="david",
    )
    base.execute("UPDATE cambios SET vence_en = datetime('now', '-1 second') WHERE id = ?", (cambio["id"],))
    base.commit()

    with pytest.raises(ValueError, match="venció"):
        confirmar(cambio["id"], "david")
    assert pendientes("oficinas", 1) == []
    assert base.execute("SELECT COUNT(*) FROM cambios WHERE id = ?", (cambio["id"],)).fetchone()[0] == 0


def test_vania_no_puede_ser_solicitante(base):
    from app.cambios import crear_pendiente

    with pytest.raises(ValueError, match="David o Grecia"):
        crear_pendiente(
            area="oficinas",
            registro_id=1,
            operacion="modificacion",
            valores_nuevos={"estatus": "ocupada"},
            solicitante="vania",
            ejecutor="vania",
        )


def test_baja_confirmada_borra_y_deja_historial(base):
    from app.cambios import confirmar, crear_pendiente, historial

    cambio = crear_pendiente(
        area="oficinas",
        registro_id=1,
        operacion="baja",
        solicitante="david",
        ejecutor="vania",
    )
    confirmar(cambio["id"], "david")

    assert base.execute("SELECT * FROM oficinas WHERE id = 1").fetchone() is None
    cambios = historial("oficinas", 1)
    assert cambios[0]["operacion"] == "baja"
    assert cambios[0]["valores_anteriores"]["numero"] == "204"
