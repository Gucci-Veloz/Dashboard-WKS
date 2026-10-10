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


def _hash(page):
    return page.evaluate("window.location.hash")


def test_volver_desde_ficha_regresa_a_la_lista_del_detalle(servicio_url, page):
    page.goto(servicio_url + "/#detalle")
    page.locator('.detalle-general__areas a[href="#oficinas"]').click()
    page.wait_for_selector(".detalle-lista__enlace")
    page.locator(".detalle-lista__enlace").first.click()
    page.wait_for_selector("form")

    page.locator(".navegacion__volver").click()
    page.wait_for_selector(".detalle-lista__enlace")
    assert _hash(page) == "#oficinas"

    # Un nivel más: de la lista regresa al Detalle, y de ahí a Inicio.
    page.locator(".navegacion__volver").click()
    page.wait_for_selector(".detalle-general__areas")
    assert _hash(page) == "#detalle"
    page.locator(".navegacion__volver").click()
    page.wait_for_selector("[data-conclusion]")
    assert _hash(page) in ("", "#")


def test_volver_desde_reporte_regresa_al_detalle(servicio_url, page):
    page.goto(servicio_url + "/#detalle")
    page.locator("[data-abrir-reporte]").click()
    page.wait_for_selector("[data-fecha-reporte]")

    page.locator(".navegacion__volver").click()
    page.wait_for_selector(".detalle-general__areas")
    assert _hash(page) == "#detalle"


def test_volver_en_ficha_abierta_directo_va_a_inicio(servicio_url, page):
    page.goto(servicio_url + "/#oficinas")
    page.wait_for_selector(".detalle-lista__enlace")
    ficha = page.locator(".detalle-lista__enlace").first.get_attribute("href")

    page.goto(servicio_url + "/")
    page.goto(servicio_url + "/" + ficha)
    page.reload()
    page.wait_for_selector(".navegacion__volver")

    page.locator(".navegacion__volver").click()
    page.wait_for_selector("[data-conclusion]")
    assert _hash(page) in ("", "#")
