"""UI-19: aviso de posible duplicado (409) con tres opciones."""

import json
import urllib.request


def _get_json(url):
    with urllib.request.urlopen(url) as respuesta:
        return json.load(respuesta)


def _simular_409(page, oficina_id, duplicado_id, cuerpos):
    """Responde 409 salvo que la petición traiga crear_de_todos_modos."""
    def manejar(ruta):
        cuerpo = ruta.request.post_data_json
        cuerpos.append(cuerpo)
        if cuerpo.get("crear_de_todos_modos"):
            ruta.continue_()
            return
        ruta.fulfill(status=409, content_type="application/json", body=json.dumps({
            "mensaje": "Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?",
            "posible_duplicado": {"area": "oficinas", "id": duplicado_id, "resumen": "Oficina existente"},
        }))
    page.route(f"**/api/oficinas/{oficina_id}", lambda r: manejar(r) if r.request.method == "PUT" else r.continue_())


def _abrir_aviso(servicio_url, page, cuerpos):
    oficinas = _get_json(servicio_url + "/api/oficinas")
    oficina, otra = oficinas[3], oficinas[4]
    _simular_409(page, oficina["id"], otra["id"], cuerpos)
    page.goto(f"{servicio_url}/#oficina-{oficina['id']}")
    page.locator("#campo-piso").fill("Piso UI-19")
    page.locator("button[type=submit]").click()
    page.wait_for_selector("[data-ventana-duplicado]")
    return oficina, otra


def test_revisar_navega_al_registro_existente(servicio_url, page):
    cuerpos = []
    _, otra = _abrir_aviso(servicio_url, page, cuerpos)
    assert "Ya existe un registro similar" in page.locator("[data-ventana-duplicado]").inner_text()
    page.locator("[data-duplicado-revisar]").click()
    page.wait_for_function(f"location.hash === '#oficina-{otra['id']}'")
    assert page.locator("[data-ventana-duplicado]").count() == 0


def test_cancelar_cierra_sin_reintentar(servicio_url, page):
    cuerpos = []
    oficina, _ = _abrir_aviso(servicio_url, page, cuerpos)
    page.locator("[data-duplicado-cancelar]").click()
    assert page.locator("[data-ventana-duplicado]").count() == 0
    assert page.locator("[data-ventana-confirmacion]").count() == 0
    assert page.evaluate("location.hash") == f"#oficina-{oficina['id']}"
    assert len(cuerpos) == 1 and not cuerpos[0].get("crear_de_todos_modos")


def test_reemplazar_envia_put_al_registro_existente(servicio_url, page):
    cuerpos_reemplazo = []
    _, otra = _abrir_aviso(servicio_url, page, [])

    def capturar_reemplazo(ruta):
        cuerpos_reemplazo.append(ruta.request.post_data_json)
        ruta.continue_()

    page.route(f"**/api/oficinas/{otra['id']}", lambda r: capturar_reemplazo(r) if r.request.method == "PUT" else r.continue_())
    page.locator("[data-duplicado-forzar]").click()
    page.wait_for_selector("[data-ventana-confirmacion]")
    assert len(cuerpos_reemplazo) == 1
    assert not cuerpos_reemplazo[0].get("crear_de_todos_modos")
    assert cuerpos_reemplazo[0]["piso"] == "Piso UI-19"
