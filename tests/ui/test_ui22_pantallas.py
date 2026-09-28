"""UI-22: entrada, tablero y áreas con la base visual de UI-21."""

from pathlib import Path

import pytest


BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-22"
VIEWPORT_MOVIL = {"width": 390, "height": 844}
VIEWPORT_ESCRITORIO = {"width": 1280, "height": 800}


def _abrir(page, url):
    page.set_viewport_size(VIEWPORT_MOVIL)
    page.goto(url)
    page.wait_for_function("document.fonts.status === 'loaded'")


def _sin_desborde(page):
    assert page.evaluate("document.documentElement.scrollWidth") <= page.viewport_size["width"]


def _capturar_responsiva(page, nombre, enfoque=None):
    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    for viewport in (VIEWPORT_MOVIL, VIEWPORT_ESCRITORIO):
        page.set_viewport_size(viewport)
        page.wait_for_function("document.fonts.status === 'loaded'")
        if enfoque:
            page.locator(enfoque).evaluate(
                "el => el.scrollIntoView({block: 'start'})"
            )
        ruta = EVIDENCIA_DIR / f"{nombre}-{viewport['width']}.png"
        page.screenshot(path=str(ruta), full_page=not enfoque)
        assert ruta.exists()


def test_s01_entrada_es_plana_y_el_estado_tiene_icono(servicio_url, page):
    _abrir(page, f"{servicio_url}/acceso/?token=no-existe")
    page.wait_for_selector(".acceso__mensaje-error")
    page.wait_for_selector(".acceso__icono--error svg")

    assert page.locator(".acceso__tarjeta").evaluate(
        "el => getComputedStyle(el).boxShadow"
    ) == "none"
    assert page.locator(".acceso__icono--error").is_visible()
    _sin_desborde(page)
    _capturar_responsiva(page, "entrada")


@pytest.mark.parametrize(
    ("escenario", "captura"),
    [
        ("tranquilo", "nivel1-tranquilo-390.png"),
        ("con_atencion", "nivel1-con_atencion-390.png"),
    ],
)
def test_s03_y_s04_estado_general_plano_con_iconos(
    servicio_url, page, escenario, captura
):
    _abrir(
        page,
        f"{servicio_url}/muestras/nivel1.html?escenario={escenario}",
    )
    page.wait_for_selector(".nivel1__icono svg")
    page.wait_for_selector(".indicadores__item svg")

    for selector in (".nivel1", "[data-bloque-informativo]"):
        assert page.locator(selector).evaluate(
            "el => getComputedStyle(el).boxShadow"
        ) == "none"
    assert page.locator("[data-icono-estado]").count() >= 5
    _sin_desborde(page)
    _capturar_responsiva(page, captura.removesuffix("-390.png"))


def test_s05_asuntos_tocables_con_estado_iconografico(servicio_url, page):
    _abrir(
        page,
        f"{servicio_url}/muestras/nivel1.html?escenario=con_atencion",
    )
    page.wait_for_selector(".nivel2__icono svg")

    asuntos = page.locator(".nivel2__asunto")
    assert asuntos.count() == 3
    assert asuntos.locator("[data-icono-estado='atencion'] svg").count() == 3
    for asunto in asuntos.all():
        assert asunto.evaluate("el => getComputedStyle(el).boxShadow") != "none"
    _sin_desborde(page)
    _capturar_responsiva(
        page,
        "nivel2-con_atencion",
        enfoque=".nivel2",
    )


def test_lista_contratos_distingue_atencion_y_normal(servicio_url, page):
    _abrir(page, f"{servicio_url}/#contratos")
    page.wait_for_selector("[data-contrato-id] svg")

    contratos = page.evaluate("fetch('/api/contratos').then(r => r.json())")
    contrato_atencion = next(
        contrato
        for contrato in contratos
        if contrato["alerta_renovacion"] == "cerca_de_vencer"
    )
    contrato_normal = next(
        contrato
        for contrato in contratos
        if contrato["alerta_renovacion"] == "normal"
    )

    renglon_atencion = page.locator(
        f"[data-contrato-id='{contrato_atencion['id']}']"
    )
    renglon_normal = page.locator(
        f"[data-contrato-id='{contrato_normal['id']}']"
    )
    assert "12 días" in renglon_atencion.inner_text()
    assert renglon_atencion.locator("[data-icono='circle-alert'] svg").count() == 1
    assert "c-indicador--atencion" in (renglon_atencion.get_attribute("class") or "")
    assert renglon_normal.locator("[data-icono='check'] svg").count() == 1
    assert "c-indicador--bien" in (renglon_normal.get_attribute("class") or "")

    iconos = page.locator("[data-contrato-id] [data-icono]").evaluate_all(
        "els => els.map(el => el.dataset.icono)"
    )
    assert len(set(iconos)) > 1


def test_entrada_a_areas_lista_y_ficha(servicio_url, page):
    _abrir(page, f"{servicio_url}/#detalle")
    page.wait_for_selector(".detalle-general__areas")
    assert page.locator(".detalle-general__areas a").count() == 5
    _sin_desborde(page)
    _capturar_responsiva(page, "areas")

    _abrir(page, f"{servicio_url}/#oficinas")
    page.wait_for_selector(".detalle-lista__enlace svg")
    primer_enlace = page.locator(".detalle-lista__enlace").first
    destino = primer_enlace.get_attribute("href")
    assert "c-tarjeta-tocable" in (primer_enlace.get_attribute("class") or "")
    _sin_desborde(page)
    _capturar_responsiva(page, "oficinas-lista")

    _abrir(page, f"{servicio_url}/{destino}")
    page.wait_for_selector("[data-titulo-detalle]")
    _sin_desborde(page)
    _capturar_responsiva(page, "oficina-ficha")
