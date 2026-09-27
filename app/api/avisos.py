from datetime import date, datetime, timezone
from hashlib import sha256
import json
import os
from secrets import compare_digest
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response
from pydantic import BaseModel, Field

from app.api.estado import _leer_datos, _origen_datos
from app.db.conexion import conectar_con_filas
from app.estado import redaccion
from app.estado.reglas import calcular_estado

router = APIRouter()
ZONA_LOCAL = ZoneInfo("America/Mexico_City")
Persona = Literal["david", "grecia"]
PERSONA_GENERAL = "__general__"


class PreferenciaAvisosEntrada(BaseModel):
    persona: Persona
    tipo_evento: str = Field(min_length=1, max_length=80)
    hasta: datetime | None = None


def _credencial_de_servicio(
    authorization: str | None = Header(default=None),
) -> str:
    token_esperado = os.environ.get("WORKS_TOKEN_VANIA")
    esquema, _, credencial = (authorization or "").partition(" ")
    if (
        not token_esperado
        or esquema.lower() != "bearer"
        or not compare_digest(credencial, token_esperado)
    ):
        raise HTTPException(status_code=401)
    return "vania"


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


def _normalizar_hasta(hasta: datetime | None) -> str | None:
    if hasta is None:
        return None
    if hasta.tzinfo is None:
        hasta = hasta.replace(tzinfo=ZONA_LOCAL)
    return hasta.astimezone(timezone.utc).isoformat()


def _normalizar_tipo(tipo_evento: str) -> str:
    tipo = tipo_evento.strip().lower()
    if not tipo:
        raise HTTPException(status_code=422, detail="tipo_evento no puede estar vacío")
    return tipo


def _esta_vigente(hasta: str | None, ahora: datetime) -> bool:
    if hasta is None:
        return True
    instante = datetime.fromisoformat(hasta)
    if instante.tzinfo is None:
        instante = instante.replace(tzinfo=ZONA_LOCAL)
    return instante.astimezone(timezone.utc) > ahora


def _purgar_preferencias_vencidas(conexion, ahora: datetime) -> None:
    filas = conexion.execute(
        "SELECT persona, tipo_evento, hasta FROM preferencias_avisos WHERE hasta IS NOT NULL"
    ).fetchall()
    for fila in filas:
        if not _esta_vigente(fila["hasta"], ahora):
            conexion.execute(
                "DELETE FROM preferencias_avisos WHERE persona = ? AND tipo_evento = ?",
                (fila["persona"], fila["tipo_evento"]),
            )


def _huella_asunto(asunto: dict) -> str:
    contenido = {clave: valor for clave, valor in asunto.items() if clave != "orden"}
    serializado = json.dumps(contenido, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return sha256(serializado.encode("utf-8")).hexdigest()


def _asuntos_nuevos(conexion, asuntos: list[dict], persona: str, ahora: datetime) -> list[dict]:
    ids_actuales = {asunto["id"] for asunto in asuntos}
    emitidos = conexion.execute(
        "SELECT asunto_id, huella FROM avisos_emitidos WHERE persona = ?",
        (persona,),
    ).fetchall()
    for fila in emitidos:
        if fila["asunto_id"] not in ids_actuales:
            conexion.execute(
                "DELETE FROM avisos_emitidos WHERE persona = ? AND asunto_id = ?",
                (persona, fila["asunto_id"]),
            )

    huellas_emitidas = {fila["asunto_id"]: fila["huella"] for fila in emitidos}
    nuevos = []
    instante = ahora.isoformat()
    for asunto in asuntos:
        huella = _huella_asunto(asunto)
        if huellas_emitidas.get(asunto["id"]) == huella:
            continue
        nuevos.append(asunto)
        conexion.execute(
            """
            INSERT INTO avisos_emitidos
                (persona, asunto_id, tipo_evento, huella, avisado_en)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(persona, asunto_id) DO UPDATE SET
                tipo_evento = excluded.tipo_evento,
                huella = excluded.huella,
                avisado_en = excluded.avisado_en
            """,
            (persona, asunto["id"], asunto["area"], huella, instante),
        )
    return nuevos


@router.patch("/api/vania/preferencias-avisos")
def guardar_preferencia(
    preferencia: PreferenciaAvisosEntrada,
    _: str = Depends(_credencial_de_servicio),
):
    ahora = _ahora_utc()
    tipo_evento = _normalizar_tipo(preferencia.tipo_evento)
    hasta = _normalizar_hasta(preferencia.hasta)
    conexion = conectar_con_filas()
    try:
        conexion.execute(
            """
            INSERT INTO preferencias_avisos
                (persona, tipo_evento, hasta, creado_en, actualizado_en)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(persona, tipo_evento) DO UPDATE SET
                hasta = excluded.hasta,
                actualizado_en = excluded.actualizado_en
            """,
            (preferencia.persona, tipo_evento, hasta, ahora.isoformat(), ahora.isoformat()),
        )
        # Al terminar el silencio, el asunto debe poder avisarse otra vez aunque
        # se hubiera emitido antes de crear la preferencia.
        conexion.execute(
            "DELETE FROM avisos_emitidos WHERE persona = ? AND tipo_evento = ?",
            (preferencia.persona, tipo_evento),
        )
        conexion.commit()
    finally:
        conexion.close()
    return {
        "persona": preferencia.persona,
        "tipo_evento": tipo_evento,
        "hasta": hasta,
    }


@router.get("/api/vania/preferencias-avisos")
def consultar_preferencias(
    persona: Persona | None = Query(default=None),
    _: str = Depends(_credencial_de_servicio),
):
    ahora = _ahora_utc()
    conexion = conectar_con_filas()
    try:
        _purgar_preferencias_vencidas(conexion, ahora)
        if persona is None:
            filas = conexion.execute(
                "SELECT persona, tipo_evento, hasta FROM preferencias_avisos "
                "ORDER BY persona, tipo_evento"
            ).fetchall()
        else:
            filas = conexion.execute(
                "SELECT persona, tipo_evento, hasta FROM preferencias_avisos "
                "WHERE persona = ? ORDER BY tipo_evento",
                (persona,),
            ).fetchall()
        conexion.commit()
        return {"preferencias": [dict(fila) for fila in filas]}
    finally:
        conexion.close()


@router.patch("/api/vania/preferencias-avisos/quitar", status_code=204)
def quitar_preferencia(
    persona: Persona,
    tipo_evento: str = Query(min_length=1, max_length=80),
    _: str = Depends(_credencial_de_servicio),
):
    tipo = _normalizar_tipo(tipo_evento)
    conexion = conectar_con_filas()
    try:
        conexion.execute(
            "DELETE FROM preferencias_avisos WHERE persona = ? AND tipo_evento = ?",
            (persona, tipo),
        )
        conexion.execute(
            "DELETE FROM avisos_emitidos WHERE persona = ? AND tipo_evento = ?",
            (persona, tipo),
        )
        conexion.commit()
    finally:
        conexion.close()
    return Response(status_code=204)


@router.get("/api/vania/avisos")
def avisos_agrupados(
    persona: Persona | None = Query(default=None),
    _: str = Depends(_credencial_de_servicio),
):
    ahora = _ahora_utc()
    conexion = conectar_con_filas()
    try:
        datos, origenes = _leer_datos(conexion)
        estado = calcular_estado(
            datos,
            date.today(),
            _origen_datos(origenes),
            generado_en=datetime.now().isoformat(),
        )

        _purgar_preferencias_vencidas(conexion, ahora)
        tipos_silenciados = set()
        if persona is not None:
            filas = conexion.execute(
                "SELECT tipo_evento, hasta FROM preferencias_avisos WHERE persona = ?",
                (persona,),
            ).fetchall()
            tipos_silenciados = {
                fila["tipo_evento"]
                for fila in filas
                if _esta_vigente(fila["hasta"], ahora)
            }

        asuntos_visibles = [
            asunto
            for asunto in estado["asuntos"]
            if asunto["area"] not in tipos_silenciados
        ]
        asuntos = _asuntos_nuevos(
            conexion,
            asuntos_visibles,
            persona or PERSONA_GENERAL,
            ahora,
        )
        conexion.commit()
    finally:
        conexion.close()

    if not asuntos:
        return Response(status_code=204)

    frases = [asunto["frase"] for asunto in asuntos]
    mensaje = redaccion.frase_conclusion_atencion(len(asuntos)) + " " + " ".join(frases)

    return {
        "mensaje": mensaje,
        "cantidad": len(asuntos),
        "asuntos": asuntos,
    }
