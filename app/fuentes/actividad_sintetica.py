"""Movimientos de ejemplo del rastro de Vania (ver PLAN.md, INT-03).

Asume que ya se cargó `app.fuentes.sintetica` con el escenario
`con_atencion` (DAT-06): las referencias apuntan a los registros que ese
escenario deja en `contratos`, `pagos` e `inquilinos`.
"""

from app.actividad.registrar import registrar

MOVIMIENTOS = (
    {
        "tipo": "solicitada",
        "accion": "registrar_pago",
        "area": "pagos",
        "referencia": "pago-1",
        "resumen": "Vania registró el pago de la oficina 101.",
    },
    {
        "tipo": "solicitada",
        "accion": "actualizar_dato",
        "area": "inquilinos",
        "referencia": "inquilino-1",
        "resumen": "Vania actualizó el contacto de Titular Sintético 01.",
    },
    {
        "tipo": "detectada",
        "accion": "contrato_por_vencer",
        "area": "contratos",
        "referencia": "contrato-4",
        "resumen": "Vania detectó que el contrato de la oficina 104 vence en 12 días.",
    },
    {
        "tipo": "detectada",
        "accion": "contacto_incompleto",
        "area": "inquilinos",
        "referencia": "inquilino-9",
        "resumen": "Vania encontró que el contacto de Titular Sintético 09 necesita revisión.",
    },
)


def cargar_actividad_sintetica() -> None:
    for movimiento in MOVIMIENTOS:
        registrar(
            actor="vania",
            origen_dato="sintetico",
            **movimiento,
        )


if __name__ == "__main__":
    cargar_actividad_sintetica()
    print("Actividad sintética de Vania cargada.")
