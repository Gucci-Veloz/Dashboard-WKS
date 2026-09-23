"""UI-10: detalle editable de oficinas, contra la API real."""

import json
import urllib.request


def _get_json(url):
    with urllib.request.urlopen(url) as respuesta:
        return json.load(respuesta)


def test_editar_guardar_recargar_y_ver_el_valor_nuevo(servicio_url, page):
    oficinas = _get_json(servicio_url + "/api/oficinas")
    oficina_id = oficinas[0]["id"]

    page.goto(f"{servicio_url}/#oficina-{oficina_id}")
    page.wait_for_selector("#campo-piso")

    page.locator("#campo-piso").fill("Piso de prueba UI-10")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-confirmacion]")

    page.reload()
    page.wait_for_selector("#campo-piso")
    assert page.locator("#campo-piso").input_value() == "Piso de prueba UI-10"

    oficina_actualizada = _get_json(f"{servicio_url}/api/oficinas/{oficina_id}")
    assert oficina_actualizada["piso"] == "Piso de prueba UI-10"


def test_guardar_deja_actividad_con_actor_dashboard(servicio_url, page):
    oficinas = _get_json(servicio_url + "/api/oficinas")
    oficina_id = oficinas[0]["id"]

    actividad_antes = _get_json(
        f"{servicio_url}/api/actividad?area=oficinas"
    )["total"]

    page.goto(f"{servicio_url}/#oficina-{oficina_id}")
    page.wait_for_selector("#campo-estatus")
    page.locator("#campo-estatus").fill("disponible")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-confirmacion]")

    actividad_despues = _get_json(f"{servicio_url}/api/actividad?area=oficinas")
    assert actividad_despues["total"] == actividad_antes + 1
    assert actividad_despues["resultados"][0]["actor"] == "dashboard"
    assert actividad_despues["resultados"][0]["referencia"] == str(oficina_id)
