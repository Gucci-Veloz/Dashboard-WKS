import json
import re
from datetime import date
from pathlib import Path

from app.estado.reglas import calcular_estado
from app.fuentes.sintetica import FuenteSintetica

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "contratos" / "estado.schema.json"
FECHA_FIJA = date(2026, 9, 23)


def _validar_contra_esquema(instancia, esquema):
    tipo = esquema.get("type")

    if "enum" in esquema:
        assert instancia in esquema["enum"], f"{instancia!r} no está en {esquema['enum']}"

    if tipo == "object":
        assert isinstance(instancia, dict)
        for campo in esquema.get("required", []):
            assert campo in instancia, f"falta el campo requerido {campo!r}"
        propiedades = esquema.get("properties", {})
        if esquema.get("additionalProperties") is False:
            extra = set(instancia) - set(propiedades)
            assert not extra, f"propiedades no permitidas: {extra}"
        for clave, subesquema in propiedades.items():
            if clave in instancia:
                _validar_contra_esquema(instancia[clave], subesquema)
    elif tipo == "array":
        assert isinstance(instancia, list)
        for elemento in instancia:
            _validar_contra_esquema(elemento, esquema["items"])
    elif tipo == "string":
        assert isinstance(instancia, str)
        assert len(instancia) >= esquema.get("minLength", 0)
    elif tipo == "integer":
        assert isinstance(instancia, int)
        assert instancia >= esquema.get("minimum", instancia)


def _cargar_datos(escenario):
    return FuenteSintetica(fecha_hoy=FECHA_FIJA).obtener_registros(escenario)


def test_tranquilo_sin_asuntos():
    estado = calcular_estado(_cargar_datos("tranquilo"), FECHA_FIJA, "sintetico")
    assert estado["conclusion"]["tipo"] == "tranquilo"
    assert estado["asuntos"] == []


def test_con_atencion_reproduce_los_tres_asuntos_en_el_mismo_orden():
    datos = _cargar_datos("con_atencion")
    primera = calcular_estado(datos, FECHA_FIJA, "sintetico")
    segunda = calcular_estado(datos, FECHA_FIJA, "sintetico")

    assert primera == segunda
    assert primera["conclusion"]["tipo"] == "atencion"
    assert [a["area"] for a in primera["asuntos"]] == ["contratos", "pagos", "inquilinos"]
    assert [a["orden"] for a in primera["asuntos"]] == [0, 1, 2]


def test_ninguna_frase_tiene_fecha_cruda():
    estado = calcular_estado(_cargar_datos("con_atencion"), FECHA_FIJA, "sintetico")
    patron_fecha = re.compile(r"\d{2}/\d{2}/\d{4}")
    assert not patron_fecha.search(estado["conclusion"]["frase"])
    for asunto in estado["asuntos"]:
        assert not patron_fecha.search(asunto["frase"])
        assert not patron_fecha.search(asunto["por_que_importa"])
    for indicador in estado["indicadores"]:
        assert not patron_fecha.search(indicador["frase_corta"])


def test_la_salida_valida_contra_el_esquema():
    esquema = json.loads(SCHEMA_PATH.read_text())
    for escenario in ("tranquilo", "con_atencion"):
        estado = calcular_estado(_cargar_datos(escenario), FECHA_FIJA, "sintetico")
        _validar_contra_esquema(estado, esquema)
