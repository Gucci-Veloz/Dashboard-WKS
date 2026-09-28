"""Toda la redacción del estado de atención vive aquí.

Las frases son provisionales: el texto exacto sigue abierto (ver
contratos/LEEME.md). Cambiar el texto de una frase no debe requerir tocar
app/estado/reglas.py.
"""

MESES_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]

NUMEROS_EN_PALABRAS = {
    1: "una", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
    6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez",
}


def nombre_mes(numero_mes: int) -> str:
    return MESES_ES[numero_mes - 1]


def cantidad_en_palabras(cantidad: int) -> str:
    return NUMEROS_EN_PALABRAS.get(cantidad, str(cantidad))


def frase_conclusion_tranquilo() -> str:
    return "Todo está en orden en Works."


def frase_conclusion_atencion(cantidad: int) -> str:
    palabra = cantidad_en_palabras(cantidad)
    sustantivo = "cosa" if cantidad == 1 else "cosas"
    verbo = "requiere" if cantidad == 1 else "requieren"
    return f"Hay {palabra} {sustantivo} que {verbo} atención hoy."


def frase_contrato_por_vencer(numero_oficina: str, dias: int) -> str:
    return f"La oficina {numero_oficina} vence en {dias} días."


def por_que_importa_contrato_por_vencer() -> str:
    return (
        "El contrato entra en su ventana de renovación y todavía no hay "
        "respuesta de la persona inquilina."
    )


def frase_pago_pendiente(numero_oficina: str, numero_mes: int) -> str:
    return f"El pago de {nombre_mes(numero_mes)} de la oficina {numero_oficina} sigue pendiente."


def por_que_importa_pago_pendiente() -> str:
    return "Ya pasó la fecha esperada de pago y no hay registro de que se haya cubierto."


def frase_contacto_incompleto(titular: str) -> str:
    return f"El contacto de {titular} quedó incompleto."


def por_que_importa_contacto_incompleto() -> str:
    return "Falta un dato de contacto y eso impide avisarle si algo de su contrato cambia."


def indicador_oficinas() -> str:
    return "Oficinas · sin novedad"


def indicador_inquilinos(cantidad_incompletos: int) -> str:
    if cantidad_incompletos == 0:
        return "Inquilinos · sin novedad"
    sustantivo = "dato incompleto" if cantidad_incompletos == 1 else "datos incompletos"
    return f"Inquilinos · {cantidad_en_palabras(cantidad_incompletos)} {sustantivo}"


def indicador_contratos(cantidad_por_vencer: int) -> str:
    if cantidad_por_vencer == 0:
        return "Contratos · al día"
    sustantivo = "renovación cerca" if cantidad_por_vencer == 1 else "renovaciones cerca"
    return f"Contratos · {cantidad_en_palabras(cantidad_por_vencer)} {sustantivo}"


def indicador_pagos(cantidad_pendientes: int) -> str:
    if cantidad_pendientes == 0:
        return "Pagos · al día"
    sustantivo = "pendiente" if cantidad_pendientes == 1 else "pendientes"
    return f"Pagos · {cantidad_en_palabras(cantidad_pendientes)} {sustantivo}"
