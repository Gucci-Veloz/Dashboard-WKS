"""UI-23: formulario, reporte, confirmación, duplicado y pendientes."""

import hashlib
import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-23"
MOVIL = {"width": 390, "height": 844}
ESCRITORIO = {"width": 1280, "height": 800}


def _abrir(page, url, viewport=MOVIL):
    page.set_viewport_size(viewport)
    page.goto(url)
    page.wait_for_function("document.fonts.status === 'loaded'")


def _capturar(page, nombre, viewport, full_page=True):
    page.set_viewport_size(viewport)
    page.wait_for_function("document.fonts.status === 'loaded'")
    ruta = EVIDENCIA_DIR / f"{nombre}-{viewport['width']}.png"
    page.screenshot(path=str(ruta), full_page=full_page)
    assert ruta.exists()


def _sin_desborde(page, ancho):
    assert page.evaluate("document.documentElement.scrollWidth") <= ancho


def test_s06_formulario_hundido_y_responsivo(servicio_url, page):
    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    _abrir(page, f"{servicio_url}/muestras/formulario.html")

    campos = page.locator(".campo-texto__control")
    assert campos.count() == 4
    for campo in campos.all():
        assert "inset" in campo.evaluate("el => getComputedStyle(el).boxShadow")
    _sin_desborde(page, 390)
    _capturar(page, "formulario", MOVIL)

    _capturar(page, "formulario", ESCRITORIO)
    assert page.locator(".formulario").evaluate(
        "el => Math.round(el.getBoundingClientRect().width)"
    ) == 680
    _sin_desborde(page, 1280)


def test_s07_reporte_contiene_su_desplazamiento(servicio_url, page):
    filas = [
        {
            "id": 2301,
            "fecha": "2026-09-27T10:15:00-06:00",
            "inquilino": "Titular Sintético 07",
            "concepto": "Cambio de contacto",
            "observaciones": "Verificación visual UI-23",
            "solicitante": "grecia",
            "ejecutor": "vania",
        }
    ]
    page.route(
        "**/api/reporte?**",
        lambda ruta: ruta.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(filas),
        ),
    )
    _abrir(page, f"{servicio_url}/#reporte")
    page.wait_for_selector("[data-tabla-reporte]")

    fecha = page.locator("[data-fecha-reporte]")
    tabla = page.locator(".reporte__tabla")
    assert "inset" in fecha.evaluate("el => getComputedStyle(el).boxShadow")
    assert tabla.evaluate("el => getComputedStyle(el).overflowX") == "auto"
    assert tabla.evaluate("el => el.scrollWidth > el.clientWidth")
    assert tabla.evaluate("el => { el.scrollLeft = 240; return el.scrollLeft; }") > 0
    _sin_desborde(page, 390)
    _capturar(page, "reporte", MOVIL)

    _capturar(page, "reporte", ESCRITORIO)
    _sin_desborde(page, 1280)


def test_confirmacion_y_duplicado_son_hojas_inferiores(servicio_url, page):
    _abrir(page, f"{servicio_url}/muestras/formulario.html")
    page.evaluate(
        """async () => {
          const { abrirConfirmacion } = await import('/componentes/confirmacion.js');
          abrirConfirmacion({ cambio: { id: 2302, solicitante: 'grecia' } });
        }"""
    )
    page.wait_for_selector("[data-icono-estado='info'] svg")
    page.wait_for_function(
        "document.getAnimations().every(animacion => animacion.playState === 'finished')"
    )
    contenido = page.locator(".ventana-confirmacion__contenido")
    caja = contenido.bounding_box()
    assert abs(caja["y"] + caja["height"] - MOVIL["height"]) <= 2
    assert "c-modal" in (contenido.get_attribute("class") or "")
    _capturar(page, "confirmacion", MOVIL, full_page=False)

    _capturar(page, "confirmacion", ESCRITORIO, full_page=False)
    caja = contenido.bounding_box()
    assert caja["y"] > 0
    assert caja["y"] + caja["height"] < ESCRITORIO["height"]

    page.locator("[data-ventana-confirmacion]").evaluate("el => el.remove()")
    page.evaluate(
        """async () => {
          const { abrirDuplicado } = await import('/componentes/duplicado.js');
          abrirDuplicado({
            error: {
              message: 'Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?',
              duplicado: {
                area: 'oficinas',
                id: 2303,
                resumen: 'Oficina sintética 2303'
              }
            }
          });
        }"""
    )
    page.wait_for_selector("[data-icono-estado='circle-alert'] svg")
    page.wait_for_function(
        "document.getAnimations().every(animacion => animacion.playState === 'finished')"
    )
    _capturar(page, "duplicado", MOVIL, full_page=False)
    caja = contenido.bounding_box()
    assert abs(caja["y"] + caja["height"] - MOVIL["height"]) <= 2

    _capturar(page, "duplicado", ESCRITORIO, full_page=False)
    caja = contenido.bounding_box()
    assert caja["y"] > 0
    assert caja["y"] + caja["height"] < ESCRITORIO["height"]


def test_cambio_pendiente_es_plano_y_su_icono_es_real(servicio_url, page):
    cambios = [
        {
            "id": 2304,
            "area": "oficinas",
            "registro_id": 101,
            "estado": "pendiente",
            "solicitante": "grecia",
        }
    ]
    page.route(
        "**/api/cambios?**",
        lambda ruta: ruta.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(cambios),
        ),
    )
    _abrir(page, f"{servicio_url}/muestras/formulario.html")
    page.evaluate(
        """async () => {
          const app = document.querySelector('#app');
          app.innerHTML = '<h1>Oficina 101</h1><div data-pendientes></div>';
          const { mostrarPendientes } = await import('/componentes/confirmacion.js');
          await mostrarPendientes({
            contenedor: document.querySelector('[data-pendientes]'),
            area: 'oficinas',
            registroId: 101
          });
        }"""
    )
    page.wait_for_selector("[data-cambio-pendiente] [data-icono-estado='circle-alert'] svg")

    pendiente = page.locator("[data-cambio-pendiente]")
    assert pendiente.evaluate("el => getComputedStyle(el).boxShadow") == "none"
    assert "c-indicador--atencion" in (
        pendiente.locator(".cambio-pendiente__estado").get_attribute("class") or ""
    )
    _sin_desborde(page, 390)
    _capturar(page, "pendientes", MOVIL)
    _capturar(page, "pendientes", ESCRITORIO)


def test_capturas_ui23_existen_y_son_todas_distintas():
    nombres = ("formulario", "reporte", "confirmacion", "duplicado", "pendientes")
    rutas = [
        EVIDENCIA_DIR / f"{nombre}-{ancho}.png"
        for nombre in nombres
        for ancho in (390, 1280)
    ]
    assert all(ruta.exists() for ruta in rutas)
    hashes = [hashlib.sha256(ruta.read_bytes()).hexdigest() for ruta in rutas]
    assert len(set(hashes)) == len(rutas)
