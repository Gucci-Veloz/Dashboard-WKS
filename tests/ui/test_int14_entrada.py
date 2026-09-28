"""INT-14: entrada desde un enlace de Vania en teléfono."""

from pathlib import Path

from app.seguridad.sesion import crear_enlace
from playwright.sync_api import expect

BASE_DIR = Path(__file__).resolve().parent.parent.parent
EVIDENCIA_DIR = BASE_DIR / "evidencia" / "INT-14"
MENSAJE_ENLACE_INVALIDO = "Este enlace ya no sirve. Pídele a Vania uno nuevo."


def test_enlace_valido_termina_en_nivel_1(servicio_url, page):
    page.set_viewport_size({"width": 390, "height": 844})
    page.context.clear_cookies()
    token = crear_enlace("grecia")["token"]

    page.goto(f"{servicio_url}/acceso/?token={token}")
    page.wait_for_url(f"{servicio_url}/")
    page.wait_for_selector("[data-conclusion]")

    EVIDENCIA_DIR.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(EVIDENCIA_DIR / "entrada-390.png"), full_page=True)
    assert (EVIDENCIA_DIR / "entrada-390.png").exists()


def test_enlace_vencido_muestra_que_hacer(servicio_url, page):
    page.goto(f"{servicio_url}/acceso/?token=no-existe")
    mensaje = page.locator("[data-acceso-mensaje]")
    expect(mensaje).to_have_text(MENSAJE_ENLACE_INVALIDO)
    assert mensaje.inner_text() == MENSAJE_ENLACE_INVALIDO
