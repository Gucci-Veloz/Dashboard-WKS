"""UI-21: base local del rediseño visual a 390 y 1280 px."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-21"


def _abrir_muestra(servicio_url, page, ancho, alto):
    solicitudes = []
    page.on("request", lambda solicitud: solicitudes.append(solicitud.url))
    page.set_viewport_size({"width": ancho, "height": alto})
    page.goto(f"{servicio_url}/muestras/componentes.html")
    page.wait_for_function("document.fonts.status === 'loaded'")
    return solicitudes


def test_superficie_plana_boton_elevado_y_campo_hundido(servicio_url, page):
    _abrir_muestra(servicio_url, page, 390, 844)
    superficie = page.locator(".muestra-estatica")
    boton = page.locator("#boton-muestra")
    campo = page.locator("#campo-muestra")
    assert superficie.evaluate("el => getComputedStyle(el).boxShadow") == "none"
    assert boton.evaluate("el => getComputedStyle(el).boxShadow") != "none"
    assert "inset" in campo.evaluate("el => getComputedStyle(el).boxShadow")


def test_presion_inter_y_sin_red_externa(servicio_url, page):
    solicitudes = _abrir_muestra(servicio_url, page, 390, 844)
    boton = page.locator("#boton-muestra")
    reposo = boton.evaluate("el => { const s = getComputedStyle(el); return [s.transform, s.boxShadow]; }")
    caja = boton.bounding_box()
    page.mouse.move(caja["x"] + caja["width"] / 2, caja["y"] + caja["height"] / 2)
    page.mouse.down()
    page.wait_for_timeout(110)
    presionado = boton.evaluate("el => { const s = getComputedStyle(el); return [s.transform, s.boxShadow]; }")
    page.mouse.up()
    assert reposo != presionado
    assert "Inter Variable" in page.locator("body").evaluate("el => getComputedStyle(el).fontFamily")
    assert page.evaluate("document.fonts.check('16px \\\"Inter Variable\\\"')")
    assert all(url.startswith(servicio_url) for url in solicitudes)


def test_refinamientos_de_enlace_deshabilitado_y_tabla(servicio_url, page):
    _abrir_muestra(servicio_url, page, 390, 844)
    enlace = page.locator(".c-enlace")
    deshabilitado = page.get_by_role("button", name="Deshabilitado")
    tabla = page.locator(".c-tabla-contenedor")
    etiqueta_overlay = page.locator(".c-overlay__etiqueta")

    assert enlace.evaluate("el => getComputedStyle(el).textDecorationLine") == "underline"
    assert deshabilitado.evaluate("el => getComputedStyle(el).borderTopColor") != "rgba(0, 0, 0, 0)"
    assert tabla.evaluate("el => getComputedStyle(el).overflowX") == "auto"
    assert etiqueta_overlay.evaluate("el => getComputedStyle(el).boxShadow") == "none"


def test_geometria_de_acciones_equivalentes_a_390px(servicio_url, page):
    _abrir_muestra(servicio_url, page, 390, 844)
    medidas = page.locator(".grupo-acciones .boton").evaluate_all(
        """botones => botones.map(boton => {
          const caja = boton.getBoundingClientRect();
          const icono = boton.querySelector('.accion__icono').getBoundingClientRect();
          const texto = boton.querySelector('.accion__texto').getBoundingClientRect();
          return { alto: caja.height, iconoX: icono.x, textoX: texto.x };
        })"""
    )
    assert max(medida["alto"] for medida in medidas) - min(
        medida["alto"] for medida in medidas
    ) <= 2
    assert max(medida["iconoX"] for medida in medidas) - min(
        medida["iconoX"] for medida in medidas
    ) <= 2
    assert max(medida["textoX"] for medida in medidas) - min(
        medida["textoX"] for medida in medidas
    ) <= 2
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")


def test_material_elevado_y_hundido_a_390px(servicio_url, page):
    _abrir_muestra(servicio_url, page, 390, 844)
    for boton in page.locator(".grupo-acciones .boton").all():
        estilo = boton.evaluate(
            """el => {
              const s = getComputedStyle(el);
              return { fondo: s.backgroundImage, borde: s.borderTopWidth, sombra: s.boxShadow };
            }"""
        )
        assert estilo["fondo"] == "none"
        assert estilo["borde"] == "0px"
        assert "-8px -8px" in estilo["sombra"] or "-5px -5px" in estilo["sombra"]
        assert "8px 8px" in estilo["sombra"] or "5px 5px" in estilo["sombra"]

    for selector in ("#campo-muestra", ".c-interruptor__pista", ".c-segmentos"):
        sombra = page.locator(selector).evaluate("el => getComputedStyle(el).boxShadow")
        assert sombra.count("inset") >= 2
        assert "-5px -5px" in sombra
        assert "5px 5px" in sombra


def test_no_desborda_y_guarda_capturas(servicio_url, page):
    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    _abrir_muestra(servicio_url, page, 390, 844)
    assert page.evaluate("document.documentElement.scrollWidth") <= 390
    page.screenshot(path=str(EVIDENCIA_DIR / "componentes-390.png"), full_page=True)
    tabla = page.locator(".c-tabla-contenedor")
    assert tabla.evaluate("el => { el.scrollLeft = 230; return el.scrollLeft; }") > 0
    assert page.evaluate("document.documentElement.scrollWidth") <= 390
    page.screenshot(path=str(EVIDENCIA_DIR / "tabla-desplazada-390.png"), full_page=True)
    _abrir_muestra(servicio_url, page, 1280, 800)
    page.screenshot(path=str(EVIDENCIA_DIR / "componentes-1280.png"), full_page=True)
    assert (EVIDENCIA_DIR / "componentes-390.png").exists()
    assert (EVIDENCIA_DIR / "tabla-desplazada-390.png").exists()
    assert (EVIDENCIA_DIR / "componentes-1280.png").exists()
