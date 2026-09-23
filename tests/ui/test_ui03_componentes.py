"""UI-03: componentes neumórficos base.

La muestra carga, el botón presionado cambia un valor computado
distinto de box-shadow, el foco es visible, y el verificador de
contraste de UI-02 sigue en 0.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-03"


def test_muestra_carga(servicio_url, page):
    page.goto(servicio_url + "/muestras/componentes.html")
    assert page.title() == "Works · muestra de componentes"
    assert page.locator("#boton-muestra").is_visible()


def test_boton_presionado_cambia_borde_o_color(servicio_url, page):
    page.goto(servicio_url + "/muestras/componentes.html")
    boton = page.locator("#boton-muestra")

    estilo_reposo = boton.evaluate(
        "el => { const s = getComputedStyle(el); "
        "return {borderColor: s.borderColor, backgroundColor: s.backgroundColor}; }"
    )

    caja = boton.bounding_box()
    page.mouse.move(caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2)
    page.mouse.down()

    estilo_presionado = boton.evaluate(
        "el => { const s = getComputedStyle(el); "
        "return {borderColor: s.borderColor, backgroundColor: s.backgroundColor}; }"
    )
    page.mouse.up()

    assert estilo_reposo != estilo_presionado


def test_foco_es_visible(servicio_url, page):
    page.goto(servicio_url + "/muestras/componentes.html")
    campo = page.locator("#campo-muestra")
    campo.focus()

    outline = campo.evaluate("el => getComputedStyle(el).outlineStyle")
    assert outline != "none"


def test_capturas_390px(servicio_url, page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(servicio_url + "/muestras/componentes.html")

    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(EVIDENCIA_DIR / "componentes-390.png"), full_page=True)

    assert (EVIDENCIA_DIR / "componentes-390.png").exists()


def test_contraste_de_tokens_sigue_en_cero():
    resultado = subprocess.run(
        [sys.executable, "scripts/contraste.py", "web/estilos/tokens.css"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )
    assert resultado.returncode == 0, resultado.stdout
