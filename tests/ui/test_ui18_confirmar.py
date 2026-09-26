"""UI-18: pre-registro, ventana de confirmación y pendientes compartidos."""

import json
import urllib.request


def _get_json(url):
    with urllib.request.urlopen(url) as respuesta:
        return json.load(respuesta)


def test_si_confirma_y_aplica_el_cambio(servicio_url, page):
    oficina = _get_json(servicio_url + "/api/oficinas")[0]
    page.goto(f"{servicio_url}/#oficina-{oficina['id']}")
    page.locator("#campo-piso").fill("Piso confirmado UI-18")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    assert "Grecia, ¿deseas confirmar el cambio?" in page.locator("[data-ventana-confirmacion]").inner_text()
    page.locator("[data-confirmar-cambio]").click()
    page.wait_for_selector("#campo-piso")
    assert page.locator("#campo-piso").input_value() == "Piso confirmado UI-18"


def test_no_deja_pendiente_al_recargar_y_permite_descartar(servicio_url, page):
    oficina = _get_json(servicio_url + "/api/oficinas")[1]
    valor_anterior = oficina["estatus"]
    page.goto(f"{servicio_url}/#oficina-{oficina['id']}")
    page.locator("#campo-estatus").fill("pendiente UI-18")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    page.locator("[data-no-confirmar-cambio]").click()
    page.wait_for_selector("[data-cambio-pendiente]")
    page.reload(wait_until="commit")
    page.wait_for_selector("[data-cambio-pendiente]")
    assert _get_json(f"{servicio_url}/api/oficinas/{oficina['id']}")["estatus"] == valor_anterior
    page.locator("[data-cambio-pendiente]", has_text="Cambio pendiente de confirmar").get_by_text("Descartar").click()
    page.wait_for_timeout(100)
    assert page.locator("[data-cambio-pendiente]").count() == 0


def test_borrar_pide_confirmacion(servicio_url, page):
    oficina = _get_json(servicio_url + "/api/oficinas")[2]
    page.goto(f"{servicio_url}/#oficina-{oficina['id']}")
    page.locator("[data-eliminar-registro]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    assert page.locator("[data-ventana-confirmacion]").get_by_text("Sí").is_visible()
