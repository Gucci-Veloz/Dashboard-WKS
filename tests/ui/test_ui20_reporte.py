"""UI-20: reporte del día desde el detalle, en vista de teléfono."""

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def _fecha_queretaro():
    return datetime.now(ZoneInfo("America/Mexico_City")).date().isoformat()


def test_reporte_abre_hoy_muestra_columnas_y_no_contamina_nivel1(servicio_url, page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{servicio_url}/#detalle")
    page.locator("[data-abrir-reporte]").click()
    page.wait_for_selector("[data-fecha-reporte]")

    assert page.locator("[data-fecha-reporte]").input_value() == _fecha_queretaro()

    page.goto(f"{servicio_url}/")
    page.wait_for_selector(".nivel1")
    assert page.locator(".nivel1 table").count() == 0


def test_cambiar_fecha_consulta_el_dia_elegido_y_la_tabla_tiene_siete_columnas(servicio_url, page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{servicio_url}/#reporte")
    page.wait_for_selector("[data-fecha-reporte]")
    fecha_pasada = "2000-01-01"
    with page.expect_response(lambda respuesta: f"/api/reporte?fecha={fecha_pasada}" in respuesta.url):
        page.locator("[data-fecha-reporte]").fill(fecha_pasada)
        page.locator("[data-fecha-reporte]").dispatch_event("change")
    page.wait_for_selector("[data-reporte-vacio]")
    assert page.locator("[data-fecha-reporte]").input_value() == fecha_pasada

    page.goto(f"{servicio_url}/#reporte")
    page.wait_for_selector("[data-fecha-reporte]")
    encabezados = page.locator("[data-tabla-reporte] th")
    if encabezados.count() == 0:
        page.evaluate("""async () => {
          const pendiente = await fetch('/api/inquilinos', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({titular: 'Reporte UI-20'})
          });
          const cambio = await pendiente.json();
          await fetch(`/api/cambios/${cambio.id}/confirmar`, {method: 'POST'});
        }""")
        page.reload()
        page.wait_for_selector("[data-tabla-reporte]")
        encabezados = page.locator("[data-tabla-reporte] th")
    assert encabezados.all_inner_texts() == [
        "ID", "Fecha", "Inquilino", "Concepto", "Observaciones", "Solicitante", "Ejecutor"
    ]
    Path("evidencia/UI-20").mkdir(parents=True, exist_ok=True)
    page.screenshot(path="evidencia/UI-20/reporte-390.png", full_page=True)
