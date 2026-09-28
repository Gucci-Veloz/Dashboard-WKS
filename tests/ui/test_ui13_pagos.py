"""UI-13: detalle de pagos y registrar pago.

Una sola prueba: el escenario sintético con_atencion solo trae un
pago pendiente, y registrarlo no es reversible, así que dos pruebas
que registraran el mismo pago por separado chocarían entre sí en la
base compartida de la sesión.
"""

import json
import urllib.request


def _get_json(url):
    with urllib.request.urlopen(url) as respuesta:
        return json.load(respuesta)


def test_registrar_desde_el_asunto_y_desaparece_del_nivel_1(servicio_url, page):
    estado_antes = _get_json(servicio_url + "/api/estado")
    asuntos_pago_antes = [a for a in estado_antes["asuntos"] if a["area"] == "pagos"]
    assert len(asuntos_pago_antes) > 0, "se esperaba un asunto de pago pendiente"
    id_asunto_pago = asuntos_pago_antes[0]["id"]

    page.goto(servicio_url + "/")
    asunto_pago = page.locator('.nivel2__asunto[href^="#pago-"]').first
    asunto_pago.click()
    page.wait_for_selector("[data-accion-registrar-pago]")

    page.locator("#campo-forma_pago_registro").fill("transferencia")
    page.locator("[data-accion-registrar-pago] button[type=submit]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    page.locator("[data-confirmar-cambio]").click()
    page.wait_for_selector("[data-ventana-confirmacion]", state="detached")
    page.wait_for_selector("#campo-estatus_pago")

    # El estatus de la edición general se refleja de inmediato.
    assert page.locator("#campo-estatus_pago").input_value() == "pagado"

    page.locator(".navegacion__volver").click()
    page.wait_for_selector("[data-conclusion]")

    ids_asuntos_pantalla = page.locator(".nivel2__asunto").evaluate_all(
        "els => els.map(el => el.dataset.asuntoId)"
    )
    assert id_asunto_pago not in ids_asuntos_pantalla
