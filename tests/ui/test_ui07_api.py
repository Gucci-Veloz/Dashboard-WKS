"""UI-07: niveles 1 y 2 conectados a /api/estado."""

import json
import os
import socket
import sys
import threading
import time
import urllib.request
from pathlib import Path

import pytest
import uvicorn

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def test_pantalla_muestra_los_mismos_asuntos_que_la_api(servicio_url, page):
    with urllib.request.urlopen(servicio_url + "/api/estado") as respuesta:
        estado_api = json.load(respuesta)

    asuntos_api = sorted(estado_api["asuntos"], key=lambda a: a["orden"])
    assert len(asuntos_api) > 0, "se esperaba el escenario con_atencion cargado"

    page.goto(servicio_url + "/")
    page.wait_for_selector(".nivel2__asunto")

    ids_pantalla = page.locator(".nivel2__asunto").evaluate_all(
        "els => els.map(el => el.dataset.asuntoId)"
    )
    frases_pantalla = page.locator(".nivel2__frase").evaluate_all(
        "els => els.map(el => el.textContent)"
    )

    assert ids_pantalla == [a["id"] for a in asuntos_api]
    assert frases_pantalla == [a["frase"] for a in asuntos_api]


def test_conclusion_coincide_con_la_api(servicio_url, page):
    with urllib.request.urlopen(servicio_url + "/api/estado") as respuesta:
        estado_api = json.load(respuesta)

    page.goto(servicio_url + "/")
    page.wait_for_selector("[data-conclusion]")

    texto_conclusion = page.locator("[data-conclusion]").inner_text()
    assert texto_conclusion == estado_api["conclusion"]["frase"]


@pytest.fixture
def servicio_con_api_caida(tmp_path):
    """Levanta una instancia aparte con una base SIN migrar, para que
    GET /api/estado responda con error y se pueda comprobar que la
    pantalla, servida por los mismos archivos estáticos, no se cae."""
    valor_anterior = os.environ.get("WORKS_DB")
    os.environ["WORKS_DB"] = str(tmp_path / "works-sin-migrar.db")

    for modulo in list(sys.modules):
        if modulo == "app" or modulo.startswith("app."):
            del sys.modules[modulo]
    from app.main import app

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        puerto = s.getsockname()[1]

    config = uvicorn.Config(app, host="127.0.0.1", port=puerto, log_level="warning")
    servidor = uvicorn.Server(config)
    hilo = threading.Thread(target=servidor.run, daemon=True)
    hilo.start()
    for _ in range(100):
        if servidor.started:
            break
        time.sleep(0.05)

    yield f"http://127.0.0.1:{puerto}"

    servidor.should_exit = True
    hilo.join(timeout=5)
    if valor_anterior is None:
        os.environ.pop("WORKS_DB", None)
    else:
        os.environ["WORKS_DB"] = valor_anterior


def test_servicio_caido_muestra_mensaje_humano(servicio_con_api_caida, page):
    page.goto(servicio_con_api_caida + "/")
    page.wait_for_selector("[data-error-estado]")

    texto = page.locator("[data-error-estado]").inner_text()
    assert texto.strip() != ""
    # Mensaje en palabras normales, no una pantalla técnica.
    assert "Traceback" not in texto
    assert "Error" not in texto
    assert page.locator("[data-conclusion]").count() == 0
