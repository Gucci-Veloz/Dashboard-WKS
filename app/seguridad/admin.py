"""Administración técnica local de las cuentas de Works."""

from __future__ import annotations

import argparse
import json
from datetime import datetime

from app.db.conexion import conectar
from app.seguridad.sesion import ZONA_HORARIA, ruta_telefonos

PERSONAS = {"david", "grecia"}


def _validar_persona(persona: str) -> None:
    if persona not in PERSONAS:
        raise ValueError("La cuenta debe ser david o grecia.")


def _guardar_telefono(persona: str, numero_whatsapp: str) -> None:
    ruta = ruta_telefonos()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    telefonos: dict[str, str] = {}
    if ruta.is_file():
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if isinstance(datos, dict):
            telefonos = {clave: valor for clave, valor in datos.items() if isinstance(valor, str)}
    telefonos[persona] = numero_whatsapp
    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(telefonos, archivo, ensure_ascii=False, indent=2)
        archivo.write("\n")


def crear_cuenta(persona: str, numero_whatsapp: str) -> None:
    """Activa una cuenta del Dashboard y registra su teléfono localmente."""
    _validar_persona(persona)
    conexion = conectar()
    try:
        conexion.execute(
            "INSERT INTO cuentas (persona, activa) VALUES (?, 1) "
            "ON CONFLICT(persona) DO UPDATE SET activa = 1",
            (persona,),
        )
        conexion.commit()
    finally:
        conexion.close()
    _guardar_telefono(persona, numero_whatsapp)


def desactivar_cuenta(persona: str) -> None:
    _validar_persona(persona)
    conexion = conectar()
    try:
        conexion.execute("UPDATE cuentas SET activa = 0 WHERE persona = ?", (persona,))
        conexion.commit()
    finally:
        conexion.close()


def revocar_sesiones(persona: str) -> None:
    _validar_persona(persona)
    conexion = conectar()
    try:
        conexion.execute(
            "UPDATE sesiones SET revocada_en = ? WHERE persona = ? AND revocada_en IS NULL",
            (datetime.now(ZONA_HORARIA).isoformat(), persona),
        )
        conexion.commit()
    finally:
        conexion.close()


def listar_cuentas() -> list[dict[str, object]]:
    conexion = conectar()
    try:
        filas = conexion.execute("SELECT persona, activa FROM cuentas ORDER BY persona").fetchall()
    finally:
        conexion.close()
    telefonos = {}
    ruta = ruta_telefonos()
    if ruta.is_file():
        with ruta.open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if isinstance(datos, dict):
            telefonos = datos
    return [
        {"persona": fila["persona"], "activa": bool(fila["activa"]), "numero_whatsapp": telefonos.get(fila["persona"])}
        for fila in filas
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Administración técnica local de Works")
    acciones = parser.add_subparsers(dest="accion", required=True)
    crear = acciones.add_parser("crear")
    crear.add_argument("persona", choices=sorted(PERSONAS))
    crear.add_argument("numero_whatsapp")
    for accion in ("desactivar", "revocar-sesiones"):
        subcomando = acciones.add_parser(accion)
        subcomando.add_argument("persona", choices=sorted(PERSONAS))
    acciones.add_parser("listar")
    argumentos = parser.parse_args()
    if argumentos.accion == "crear":
        crear_cuenta(argumentos.persona, argumentos.numero_whatsapp)
    elif argumentos.accion == "desactivar":
        desactivar_cuenta(argumentos.persona)
    elif argumentos.accion == "revocar-sesiones":
        revocar_sesiones(argumentos.persona)
    else:
        print(json.dumps(listar_cuentas(), ensure_ascii=False))


if __name__ == "__main__":
    main()
