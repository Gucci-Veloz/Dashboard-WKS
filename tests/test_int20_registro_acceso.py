"""El registro de accesos de Uvicorn no guarda teléfonos ni tokens de /api/acceso/.

Valores ficticios: ningún número ni token real.
"""

import logging
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

from uvicorn.logging import AccessFormatter

from app.seguridad.registro import FiltroAccesoSensible, ocultar_query

NUMERO_FICTICIO = "5210000000000"
TOKEN_FICTICIO = "tokenficticio123"
FORMATO = '%(client_addr)s - "%(request_line)s" %(status_code)s'


def _linea(ruta, metodo="POST", status=200):
    record = logging.LogRecord(
        "uvicorn.access", logging.INFO, __file__, 0,
        '%s - "%s %s HTTP/%s" %d', ("127.0.0.1:5000", metodo, ruta, "1.1", status), None,
    )
    assert FiltroAccesoSensible().filter(record)
    return AccessFormatter(FORMATO, use_colors=False).format(record)


def test_oculta_numero_whatsapp_y_conserva_metodo_ruta_y_status():
    linea = _linea(f"/api/acceso/enlace?numero_whatsapp={NUMERO_FICTICIO}")
    assert NUMERO_FICTICIO not in linea
    assert "POST /api/acceso/enlace?numero_whatsapp=*** HTTP/1.1" in linea
    assert linea.endswith("200 OK")


def test_oculta_token():
    linea = _linea(f"/api/acceso/entrar?token={TOKEN_FICTICIO}", metodo="GET", status=303)
    assert TOKEN_FICTICIO not in linea
    assert "GET /api/acceso/entrar?token=*** HTTP/1.1" in linea
    assert linea.endswith("303 See Other")


def test_otros_parametros_de_acceso_quedan_igual():
    assert ocultar_query("/api/acceso/entrar?token=x&modo=y") == "/api/acceso/entrar?token=***&modo=y"


def test_rutas_ajenas_a_acceso_no_cambian():
    for ruta in ("/api/estado", "/api/oficinas?token=visible", "/api/salud?numero_whatsapp=1"):
        assert ocultar_query(ruta) == ruta
        assert f"GET {ruta} HTTP/1.1" in _linea(ruta, metodo="GET")


def _puerto_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _pedir(url, metodo="GET"):
    try:
        urllib.request.urlopen(urllib.request.Request(url, method=metodo), timeout=5)
    except urllib.error.HTTPError:
        pass


def test_uvicorn_real_no_escribe_numero_ni_token(tmp_path):
    env = {**os.environ, "WORKS_DB": str(tmp_path / "works.db")}
    subprocess.run([sys.executable, "-m", "app.db.migrar"], env=env, check=True, capture_output=True)
    puerto = _puerto_libre()
    proceso = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(puerto)],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
    )
    base = f"http://127.0.0.1:{puerto}"
    try:
        for _ in range(100):
            try:
                urllib.request.urlopen(base + "/api/salud", timeout=1)
                break
            except OSError:
                time.sleep(0.1)
        _pedir(f"{base}/api/acceso/enlace?numero_whatsapp={NUMERO_FICTICIO}", metodo="POST")
        _pedir(f"{base}/api/acceso/entrar?token={TOKEN_FICTICIO}")
    finally:
        proceso.terminate()
        salida, _ = proceso.communicate(timeout=10)

    assert NUMERO_FICTICIO not in salida
    assert TOKEN_FICTICIO not in salida
    assert '"POST /api/acceso/enlace?numero_whatsapp=*** HTTP/1.1"' in salida
    assert '"GET /api/acceso/entrar?token=*** HTTP/1.1"' in salida
    assert '"GET /api/salud HTTP/1.1" 200' in salida
