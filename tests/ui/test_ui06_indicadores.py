"""UI-06: indicadores textuales sin KPI dominante."""


def test_indicadores_menores_que_la_conclusion(servicio_url, page):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=con_atencion")
    page.wait_for_selector(".indicadores__item")

    resultado = page.evaluate(
        """() => {
            const conclusion = document.querySelector('[data-conclusion]');
            const tamanoConclusion = parseFloat(getComputedStyle(conclusion).fontSize);
            const indicadores = document.querySelectorAll('.indicadores__item');
            const tamanos = [...indicadores].map(
                el => parseFloat(getComputedStyle(el).fontSize)
            );
            return { tamanoConclusion, tamanos };
        }"""
    )
    assert len(resultado["tamanos"]) == 4
    for tamano in resultado["tamanos"]:
        assert tamano < resultado["tamanoConclusion"]


def test_ningun_indicador_domina(servicio_url, page):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=con_atencion")
    page.wait_for_selector(".indicadores__item")

    estilos = page.locator(".indicadores__item").evaluate_all(
        """els => els.map(el => {
            const s = getComputedStyle(el);
            return `${s.fontSize}|${s.fontWeight}|${s.color}`;
        })"""
    )
    assert len(set(estilos)) == 1
