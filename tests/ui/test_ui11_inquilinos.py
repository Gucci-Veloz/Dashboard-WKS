"""UI-11: detalle editable de inquilinos, contra la API real."""

import json
import urllib.request


def _get_json(url):
    with urllib.request.urlopen(url) as respuesta:
        return json.load(respuesta)


def test_editar_guardar_recargar_y_ver_el_valor_nuevo(servicio_url, page):
    inquilinos = _get_json(servicio_url + "/api/inquilinos")
    inquilino_id = inquilinos[0]["id"]

    page.goto(f"{servicio_url}/#inquilino-{inquilino_id}")
    page.wait_for_selector("#campo-contacto")

    page.locator("#campo-contacto").fill("contacto-prueba@works.local")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    page.locator("[data-confirmar-cambio]").click()
    page.wait_for_selector("[data-ventana-confirmacion]", state="detached")

    page.reload()
    page.wait_for_selector("#campo-contacto")
    assert page.locator("#campo-contacto").input_value() == "contacto-prueba@works.local"

    inquilino_actualizado = _get_json(f"{servicio_url}/api/inquilinos/{inquilino_id}")
    assert inquilino_actualizado["contacto"] == "contacto-prueba@works.local"


def test_guardar_deja_actividad_con_actor_dashboard(servicio_url, page):
    inquilinos = _get_json(servicio_url + "/api/inquilinos")
    inquilino_id = inquilinos[0]["id"]

    actividad_antes = _get_json(
        f"{servicio_url}/api/actividad?area=inquilinos"
    )["total"]

    page.goto(f"{servicio_url}/#inquilino-{inquilino_id}")
    page.wait_for_selector("#campo-titular")
    page.locator("#campo-titular").fill("Titular Sintético 07 (editado)")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    page.locator("[data-confirmar-cambio]").click()
    page.wait_for_selector("[data-ventana-confirmacion]", state="detached")

    actividad_despues = _get_json(f"{servicio_url}/api/actividad?area=inquilinos")
    assert actividad_despues["total"] == actividad_antes + 1
    assert actividad_despues["resultados"][0]["actor"] == "dashboard"
    assert actividad_despues["resultados"][0]["referencia"] == str(inquilino_id)
