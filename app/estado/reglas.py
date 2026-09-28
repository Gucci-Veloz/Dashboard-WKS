"""Motor del estado de atención: módulo puro (D-3, alternativa A).

No depende de la base de datos ni del servicio web. Recibe los datos ya
leídos y devuelve un estado conforme a contratos/estado.schema.json.
Ninguna regla produce un asunto si no hay un hecho concreto que lo sostenga.
"""

from datetime import date
from pathlib import Path
from typing import Optional

from app.estado import redaccion

UMBRALES_PATH = Path(__file__).resolve().parent / "umbrales.toml"


def _leer_umbrales(ruta: Path) -> dict:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:  # pragma: no cover - solo en Python 3.10
        tomllib = None

    texto = ruta.read_text(encoding="utf-8")
    if tomllib is not None:
        return tomllib.loads(texto)

    # Analizador mínimo para pares "clave = numero", suficiente mientras
    # umbrales.toml solo tenga asignaciones simples (sin tablas ni listas).
    umbrales = {}
    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, _, valor = linea.partition("=")
        clave = clave.strip()
        valor = valor.split("#", 1)[0].strip()
        try:
            umbrales[clave] = int(valor)
        except ValueError:
            umbrales[clave] = float(valor)
    return umbrales


def _cargar_umbrales() -> dict:
    return _leer_umbrales(UMBRALES_PATH)


def _fecha(valor: str) -> date:
    return date.fromisoformat(valor)


def _asuntos_contratos_por_vencer(contratos, oficinas_por_id, fecha_hoy, dias_alerta):
    asuntos = []
    for contrato in contratos:
        fin = _fecha(contrato["fin"])
        dias = (fin - fecha_hoy).days
        if dias < 0 or dias > dias_alerta:
            continue
        oficina = oficinas_por_id.get(contrato["oficina_id"])
        numero_oficina = oficina["numero"] if oficina else "?"
        asuntos.append(
            {
                "id": f"contrato-{contrato['id']}",
                "area": "contratos",
                "frase": redaccion.frase_contrato_por_vencer(numero_oficina, dias),
                "por_que_importa": redaccion.por_que_importa_contrato_por_vencer(),
                "referencia": {"tipo": "contrato", "id": str(contrato["id"])},
                "_orden_secundario": contrato["id"],
            }
        )
    asuntos.sort(key=lambda a: a["_orden_secundario"])
    return asuntos


def _asuntos_pagos_pendientes(pagos, contratos_por_id, oficinas_por_id, fecha_hoy):
    asuntos = []
    for pago in pagos:
        if pago["estatus_pago"] != "pendiente":
            continue
        contrato = contratos_por_id.get(pago["contrato_id"])
        oficina = oficinas_por_id.get(contrato["oficina_id"]) if contrato else None
        numero_oficina = oficina["numero"] if oficina else "?"
        asuntos.append(
            {
                "id": f"pago-{pago['id']}",
                "area": "pagos",
                "frase": redaccion.frase_pago_pendiente(numero_oficina, fecha_hoy.month),
                "por_que_importa": redaccion.por_que_importa_pago_pendiente(),
                "referencia": {"tipo": "pago", "id": str(pago["id"])},
                "_orden_secundario": pago["id"],
            }
        )
    asuntos.sort(key=lambda a: a["_orden_secundario"])
    return asuntos


def _asuntos_contactos_incompletos(inquilinos):
    asuntos = []
    for inquilino in inquilinos:
        contacto = (inquilino.get("contacto") or "").strip()
        if contacto:
            continue
        asuntos.append(
            {
                "id": f"inquilino-{inquilino['id']}",
                "area": "inquilinos",
                "frase": redaccion.frase_contacto_incompleto(inquilino["titular"]),
                "por_que_importa": redaccion.por_que_importa_contacto_incompleto(),
                "referencia": {"tipo": "inquilino", "id": str(inquilino["id"])},
                "_orden_secundario": inquilino["id"],
            }
        )
    asuntos.sort(key=lambda a: a["_orden_secundario"])
    return asuntos


def _indicadores(datos, asuntos_contratos, asuntos_pagos, asuntos_inquilinos):
    return [
        {"area": "oficinas", "frase_corta": redaccion.indicador_oficinas()},
        {
            "area": "inquilinos",
            "frase_corta": redaccion.indicador_inquilinos(len(asuntos_inquilinos)),
        },
        {
            "area": "contratos",
            "frase_corta": redaccion.indicador_contratos(len(asuntos_contratos)),
        },
        {"area": "pagos", "frase_corta": redaccion.indicador_pagos(len(asuntos_pagos))},
    ]


def calcular_estado(
    datos: dict,
    fecha_hoy: date,
    origen_datos: str,
    generado_en: Optional[str] = None,
    umbrales: Optional[dict] = None,
) -> dict:
    umbrales = umbrales if umbrales is not None else _cargar_umbrales()
    dias_alerta = umbrales["dias_alerta_renovacion"]

    oficinas_por_id = {of["id"]: of for of in datos.get("oficinas", [])}
    contratos_por_id = {c["id"]: c for c in datos.get("contratos", [])}

    asuntos_contratos = _asuntos_contratos_por_vencer(
        datos.get("contratos", []), oficinas_por_id, fecha_hoy, dias_alerta
    )
    asuntos_pagos = _asuntos_pagos_pendientes(
        datos.get("pagos", []), contratos_por_id, oficinas_por_id, fecha_hoy
    )
    asuntos_inquilinos = _asuntos_contactos_incompletos(datos.get("inquilinos", []))

    # Orden determinista: contratos, luego pagos, luego inquilinos
    # (mismo orden que contratos/ejemplos/estado-atencion.json).
    asuntos = asuntos_contratos + asuntos_pagos + asuntos_inquilinos
    for indice, asunto in enumerate(asuntos):
        asunto["orden"] = indice
        del asunto["_orden_secundario"]

    cantidad = len(asuntos)
    if cantidad == 0:
        conclusion = {
            "tipo": "tranquilo",
            "frase": redaccion.frase_conclusion_tranquilo(),
            "cantidad": 0,
        }
    else:
        conclusion = {
            "tipo": "atencion",
            "frase": redaccion.frase_conclusion_atencion(cantidad),
            "cantidad": cantidad,
        }

    return {
        "conclusion": conclusion,
        "asuntos": asuntos,
        "indicadores": _indicadores(datos, asuntos_contratos, asuntos_pagos, asuntos_inquilinos),
        "origen_datos": origen_datos,
        "generado_en": generado_en or fecha_hoy.isoformat() + "T00:00:00",
    }
