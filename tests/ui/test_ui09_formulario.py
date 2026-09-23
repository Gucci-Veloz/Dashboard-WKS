"""UI-09: formulario y confirmación de guardado, contra un servicio
simulado dentro de la prueba (query string ?resultado=exito|error de
la muestra, sin backend real)."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-09"


def test_guardar_con_exito_muestra_confirmacion(servicio_url, page):
    page.goto(servicio_url + "/muestras/formulario.html?resultado=exito")
    page.wait_for_selector("#campo-titular")

    page.locator("#campo-titular").fill("Titular Sintético 07 editado")
    page.locator("button[type=submit]").click()

    page.wait_for_selector("[data-confirmacion]")
    assert page.locator("[data-confirmacion]").is_visible()
    assert page.locator("#campo-titular").input_value() == (
        "Titular Sintético 07 editado (actualizado)"
    )


def test_error_muestra_mensaje_y_conserva_lo_escrito(servicio_url, page):
    page.goto(servicio_url + "/muestras/formulario.html?resultado=error")
    page.wait_for_selector("#campo-titular")

    page.locator("#campo-titular").fill("Un valor que la persona escribió")
    page.locator("button[type=submit]").click()

    page.wait_for_selector("[data-error-guardar]:not([hidden])")
    mensaje = page.locator("[data-error-guardar]").inner_text()
    assert mensaje.strip() != ""

    assert page.locator("#campo-titular").input_value() == (
        "Un valor que la persona escribió"
    )
    assert page.locator("[data-confirmacion]").count() == 0


def test_capturas_390px(servicio_url, page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(servicio_url + "/muestras/formulario.html?resultado=exito")
    page.wait_for_selector("#campo-titular")

    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    ruta = EVIDENCIA_DIR / "formulario-390.png"
    page.screenshot(path=str(ruta), full_page=True)
    assert ruta.exists()
