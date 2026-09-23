from datetime import date

from app.fuentes.sintetica import ESCENARIOS, FuenteSintetica

FECHA_FIJA = date(2026, 9, 23)


def test_todo_es_sintetico():
    for escenario in ESCENARIOS:
        registros = FuenteSintetica(fecha_hoy=FECHA_FIJA).obtener_registros(escenario)
        for area, filas in registros.items():
            for fila in filas:
                assert fila["origen_dato"] == "sintetico", f"{area}: {fila}"


def test_conteos_esperados():
    for escenario in ESCENARIOS:
        registros = FuenteSintetica(fecha_hoy=FECHA_FIJA).obtener_registros(escenario)
        assert len(registros["oficinas"]) == 21
        assert len(registros["inquilinos"]) == 21
        assert len(registros["contratos"]) == 21
        assert len(registros["pagos"]) == 21


def test_titulares_contienen_sintetico():
    for escenario in ESCENARIOS:
        registros = FuenteSintetica(fecha_hoy=FECHA_FIJA).obtener_registros(escenario)
        for inquilino in registros["inquilinos"]:
            assert "Sintético" in inquilino["titular"]


def test_dos_corridas_dan_los_mismos_datos():
    for escenario in ESCENARIOS:
        primera = FuenteSintetica(fecha_hoy=FECHA_FIJA).obtener_registros(escenario)
        segunda = FuenteSintetica(fecha_hoy=FECHA_FIJA).obtener_registros(escenario)
        assert primera == segunda
