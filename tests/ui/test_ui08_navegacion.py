"""UI-08: navegación al detalle bajo demanda."""


def test_al_cargar_no_hay_detalle_visible(servicio_url, page):
    page.goto(servicio_url + "/")
    page.wait_for_selector("[data-conclusion]")

    assert page.locator("table").count() == 0
    assert page.locator(".navegacion__volver").count() == 0
    assert page.locator("h2", has_text="Detalle").count() == 0


def test_tocar_un_asunto_cambia_la_ruta_a_su_registro(servicio_url, page):
    page.goto(servicio_url + "/")
    page.wait_for_selector(".nivel2__asunto")

    primer_asunto = page.locator(".nivel2__asunto").first
    referencia_esperada = primer_asunto.get_attribute("href")

    primer_asunto.click()
    page.wait_for_selector(".navegacion__volver")

    assert page.evaluate("window.location.hash") == referencia_esperada
    assert page.locator("table").count() == 0


def test_volver_regresa_al_nivel_1(servicio_url, page):
    page.goto(servicio_url + "/")
    page.wait_for_selector(".nivel2__asunto")

    page.locator(".nivel2__asunto").first.click()
    page.wait_for_selector(".navegacion__volver")

    page.locator(".navegacion__volver").click()
    page.wait_for_selector("[data-conclusion]")

    assert page.evaluate("window.location.hash") in ("", "#")
    assert page.locator(".navegacion__volver").count() == 0
