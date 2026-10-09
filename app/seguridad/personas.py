"""Única lista de personas con cuenta en el Dashboard de Works.

Todas tienen las mismas reglas: no hay roles. La base de datos repite esta
lista en sus restricciones (migración 009); `test_int20_operador.py` revisa
que las dos sigan iguales.
"""

from __future__ import annotations

from typing import Literal, get_args

Persona = Literal["david", "grecia", "operador"]
PERSONAS: tuple[str, ...] = get_args(Persona)
NOMBRES_PERSONAS = "David, Grecia u Operador"
