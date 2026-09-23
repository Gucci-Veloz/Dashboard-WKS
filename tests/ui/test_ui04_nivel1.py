"""UI-04: nivel 1 con conclusión humana, con los ejemplos del
contrato, en ambos viewports."""

from pathlib import Path

import pytest

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "UI-04"

ESCENARIOS = ["tranquilo", "con_atencion"]


@pytest.mark.parametrize("escenario", ESCENARIOS)
def test_conclusion_tiene_la_mayor_jerarquia(servicio_url, pagina_con_viewport, escenario):
    pagina_con_viewport.goto(f"{servicio_url}/muestras/nivel1.html?escenario={escenario}")
    pagina_con_viewport.wait_for_selector("[data-conclusion]")

    resultado = pagina_con_viewport.evaluate(
        """(selectorConclusion) => {
            const conclusion = document.querySelector(selectorConclusion);
            const tamanoConclusion = parseFloat(getComputedStyle(conclusion).fontSize);
            const todos = document.querySelectorAll('body *');
            let mayor = 0;
            for (const el of todos) {
                if (el.textContent.trim() === '') continue;
                const tamano = parseFloat(getComputedStyle(el).fontSize);
                if (tamano > mayor) mayor = tamano;
            }
            return { tamanoConclusion, mayor };
        }""",
        "[data-conclusion]",
    )
    assert resultado["tamanoConclusion"] == resultado["mayor"]


def test_tranquilo_no_muestra_ninguna_lista_de_asuntos(servicio_url, page):
    # El nivel 1 en sí no agrega listas (eso es nivel 2, UI-05). Los
    # indicadores de UI-06 son una lista aparte y sí se muestran
    # siempre; aquí solo se comprueba que no aparezca ningún asunto.
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario=tranquilo")
    page.wait_for_selector("[data-conclusion]")
    assert page.locator(".nivel2__asunto").count() == 0


@pytest.mark.parametrize("escenario", ESCENARIOS)
def test_sin_porcentaje_ni_dinero(servicio_url, page, escenario):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario={escenario}")
    page.wait_for_selector("[data-conclusion]")
    texto = page.locator(".nivel1").inner_text()
    assert "%" not in texto
    assert "$" not in texto


@pytest.mark.parametrize("escenario", ESCENARIOS)
def test_aviso_de_datos_sinteticos_presente(servicio_url, page, escenario):
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario={escenario}")
    page.wait_for_selector("[data-conclusion]")
    assert page.locator("[data-aviso-datos-sinteticos]").is_visible()


@pytest.mark.parametrize("escenario", ESCENARIOS)
def test_capturas_390px(servicio_url, page, escenario):
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{servicio_url}/muestras/nivel1.html?escenario={escenario}")
    page.wait_for_selector("[data-conclusion]")

    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    ruta = EVIDENCIA_DIR / f"nivel1-{escenario}-390.png"
    page.screenshot(path=str(ruta), full_page=True)
    assert ruta.exists()
