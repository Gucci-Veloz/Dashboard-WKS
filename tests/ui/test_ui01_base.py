"""UI-01: la página base carga sin errores de consola en ambos
viewports y no produce scroll horizontal a 390px."""


def test_pagina_base_carga_sin_errores(servicio_url, pagina_con_viewport, viewport):
    errores_consola = []
    pagina_con_viewport.on(
        "console",
        lambda msg: errores_consola.append(msg.text) if msg.type == "error" else None,
    )
    pagina_con_viewport.on("pageerror", lambda exc: errores_consola.append(str(exc)))

    pagina_con_viewport.goto(servicio_url + "/")

    assert pagina_con_viewport.title() == "Works"
    assert errores_consola == []

    if viewport["width"] == 390:
        ancho_documento = pagina_con_viewport.evaluate(
            "document.documentElement.scrollWidth"
        )
        assert ancho_documento <= viewport["width"]
