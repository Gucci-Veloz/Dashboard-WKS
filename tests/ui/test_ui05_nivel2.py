"""UI-05: nivel 2 con asuntos en lenguaje humano."""

import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-05"

FECHA_DD_MM_AAAA = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")


def test_orden_en_pantalla_coincide_con_el_contrato(servicio_url, page):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=con_atencion")
    page.wait_for_selector(".nivel2")

    ordenes = page.locator(".nivel2__asunto").evaluate_all(
        "els => els.map(el => el.dataset.orden)"
    )
    assert ordenes == ["0", "1", "2"]

    ids = page.locator(".nivel2__asunto").evaluate_all(
        "els => els.map(el => el.dataset.asuntoId)"
    )
    assert ids == ["asunto-001", "asunto-002", "asunto-003"]


def test_tranquilo_no_renderiza_ningun_asunto(servicio_url, page):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=tranquilo")
    page.wait_for_selector("[data-conclusion]")
    assert page.locator(".nivel2__asunto").count() == 0
    # La lista de asuntos (.nivel2) no existe; los indicadores de
    # UI-06 son una lista aparte y sí se muestran siempre.
    assert page.locator("ul.nivel2").count() == 0


def test_ninguna_frase_tiene_fecha_cruda(servicio_url, page):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=con_atencion")
    page.wait_for_selector(".nivel2")

    textos = page.locator(".nivel2__asunto").evaluate_all(
        "els => els.map(el => el.textContent)"
    )
    for texto in textos:
        assert FECHA_DD_MM_AAAA.search(texto) is None


def test_capturas_390px(servicio_url, page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=con_atencion")
    page.wait_for_selector(".nivel2")

    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    ruta = EVIDENCIA_DIR / "nivel2-con_atencion-390.png"
    page.screenshot(path=str(ruta), full_page=True)
    assert ruta.exists()
