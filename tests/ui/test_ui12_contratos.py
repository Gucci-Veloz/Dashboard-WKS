"""UI-12: detalle editable de contratos, contra la API real."""

import json
import urllib.request
from datetime import date, timedelta


def _get_json(url):
    with urllib.request.urlopen(url) as respuesta:
        return json.load(respuesta)


def test_editar_guardar_recargar_y_ver_el_valor_nuevo(servicio_url, page):
    contratos = _get_json(servicio_url + "/api/contratos")
    contrato_id = contratos[0]["id"]

    page.goto(f"{servicio_url}/#contrato-{contrato_id}")
    page.wait_for_selector("#campo-alerta_renovacion")

    page.locator("#campo-alerta_renovacion").fill("alerta de prueba UI-12")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-confirmacion]")

    page.reload()
    page.wait_for_selector("#campo-alerta_renovacion")
    assert page.locator("#campo-alerta_renovacion").input_value() == "alerta de prueba UI-12"

    contrato_actualizado = _get_json(f"{servicio_url}/api/contratos/{contrato_id}")
    assert contrato_actualizado["alerta_renovacion"] == "alerta de prueba UI-12"


def test_fecha_se_muestra_en_forma_humana(servicio_url, page):
    contratos = _get_json(servicio_url + "/api/contratos")
    contrato_id = contratos[0]["id"]

    nueva_fecha_fin = (date.today() + timedelta(days=12)).isoformat()

    page.goto(f"{servicio_url}/#contrato-{contrato_id}")
    page.wait_for_selector("#campo-fin")
    page.locator("#campo-fin").fill(nueva_fecha_fin)
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-confirmacion]")

    texto_vencimiento = page.locator("[data-vencimiento]").inner_text()
    assert "12 días" in texto_vencimiento
    assert nueva_fecha_fin not in texto_vencimiento


def test_guardar_deja_actividad_con_actor_dashboard(servicio_url, page):
    contratos = _get_json(servicio_url + "/api/contratos")
    contrato_id = contratos[0]["id"]

    actividad_antes = _get_json(
        f"{servicio_url}/api/actividad?area=contratos"
    )["total"]

    page.goto(f"{servicio_url}/#contrato-{contrato_id}")
    page.wait_for_selector("#campo-inicio")
    page.locator("#campo-inicio").fill(date.today().isoformat())
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-confirmacion]")

    actividad_despues = _get_json(f"{servicio_url}/api/actividad?area=contratos")
    assert actividad_despues["total"] == actividad_antes + 1
    assert actividad_despues["resultados"][0]["actor"] == "dashboard"
    assert actividad_despues["resultados"][0]["referencia"] == str(contrato_id)
