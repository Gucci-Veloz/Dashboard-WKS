import sys


def _app_fresco():
    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]


def test_migrar_dos_veces_no_duplica_control(tmp_path, monkeypatch):
    base_temporal = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base_temporal))
    _app_fresco()

    from app.db.migrar import migrar
    from app.db.conexion import conectar

    migrar()
    migrar()

    conexion = conectar()
    try:
        numeros = [
            fila[0]
            for fila in conexion.execute(
                "SELECT numero FROM migraciones_aplicadas ORDER BY numero"
            ).fetchall()
        ]
    finally:
        conexion.close()

    assert numeros == sorted(set(numeros))
    assert "000" in numeros
