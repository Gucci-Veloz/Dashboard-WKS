import sys
from contextvars import ContextVar
from pathlib import Path
from sqlite3 import OperationalError

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


_sesion_de_prueba_activa = ContextVar("sesion_de_prueba_activa", default=True)
_iniciar_cliente = TestClient.__init__


def _iniciar_cliente_con_sesion(self, app, *args, **kwargs):
    _iniciar_cliente(self, app, *args, **kwargs)
    if not _sesion_de_prueba_activa.get() or getattr(app, "title", None) != "Works":
        return

    from app.seguridad.sesion import NOMBRE_COOKIE, consumir_enlace, crear_enlace

    try:
        enlace = crear_enlace("grecia")
        resultado = consumir_enlace(enlace["token"])
    except OperationalError:
        return
    self.cookies.set(NOMBRE_COOKIE, resultado["token"])


TestClient.__init__ = _iniciar_cliente_con_sesion


@pytest.fixture(autouse=True)
def sesion_de_prueba(request, tmp_path, monkeypatch):
    """Las pruebas históricas entran como Grecia sin alterar la regla 401."""
    if request.node.path.name == "test_dat01_salud.py":
        monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
        from app.db.migrar import migrar

        migrar()
    activa = request.node.path.name != "test_int13_acceso.py"
    contexto = _sesion_de_prueba_activa.set(activa)
    yield
    _sesion_de_prueba_activa.reset(contexto)
