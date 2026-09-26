from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.actividad.registrar import registrar
from app.db.conexion import conectar_con_filas
from app.seguridad.actor import actor_actual

router = APIRouter()

MENSAJE_NO_EXISTE = "No existe un pago con ese número de registro."
MENSAJE_CONTRATO_INEXISTENTE = "El contrato indicado no existe."
MENSAJE_SIN_PAGO_PENDIENTE = "No hay un pago pendiente para ese contrato."


class PagoEntrada(BaseModel):
    contrato_id: Optional[int] = None
    precio: Optional[float] = None
    deposito_garantia: Optional[float] = None
    fecha_pago: Optional[str] = None
    forma_pago: Optional[str] = None
    estatus_pago: Optional[str] = None
    extras: Optional[str] = None


class RegistrarPagoEntrada(BaseModel):
    contrato_id: int
    periodo: Optional[str] = None
    forma_pago: str


def _obtener(conexion, pago_id: int):
    fila = conexion.execute("SELECT * FROM pagos WHERE id = ?", (pago_id,)).fetchone()
    if fila is None:
        raise HTTPException(status_code=404, detail=MENSAJE_NO_EXISTE)
    return dict(fila)


def _validar_contrato(conexion, entrada: PagoEntrada) -> None:
    if entrada.contrato_id is not None:
        existe = conexion.execute(
            "SELECT 1 FROM contratos WHERE id = ?", (entrada.contrato_id,)
        ).fetchone()
        if existe is None:
            raise HTTPException(status_code=400, detail=MENSAJE_CONTRATO_INEXISTENTE)


def _numero_oficina_de_contrato(conexion, contrato_id: int) -> str:
    fila = conexion.execute(
        """
        SELECT oficinas.numero AS numero
        FROM contratos
        JOIN oficinas ON oficinas.id = contratos.oficina_id
        WHERE contratos.id = ?
        """,
        (contrato_id,),
    ).fetchone()
    return fila["numero"] if fila else "?"


@router.get("/api/pagos")
def listar_pagos() -> list:
    conexion = conectar_con_filas()
    try:
        filas = conexion.execute("SELECT * FROM pagos ORDER BY id").fetchall()
        return [dict(fila) for fila in filas]
    finally:
        conexion.close()


@router.get("/api/pagos/{pago_id}")
def ver_pago(pago_id: int) -> dict:
    conexion = conectar_con_filas()
    try:
        return _obtener(conexion, pago_id)
    finally:
        conexion.close()


@router.post("/api/pagos", status_code=201)
def crear_pago(entrada: PagoEntrada, actor: str = Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _validar_contrato(conexion, entrada)
        cursor = conexion.execute(
            """
            INSERT INTO pagos
                (contrato_id, precio, deposito_garantia, fecha_pago, forma_pago, estatus_pago,
                 origen_dato, extras)
            VALUES (?, ?, ?, ?, ?, ?, 'manual', ?)
            """,
            (
                entrada.contrato_id,
                entrada.precio,
                entrada.deposito_garantia,
                entrada.fecha_pago,
                entrada.forma_pago,
                entrada.estatus_pago or "pendiente",
                entrada.extras,
            ),
        )
        conexion.commit()
        pago_id = cursor.lastrowid
        pago = _obtener(conexion, pago_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="crear_pago",
        area="pagos",
        referencia=str(pago_id),
        resumen=f"Se creó el pago {pago_id}.",
        origen_dato="real",
    )
    return pago


@router.put("/api/pagos/{pago_id}")
def editar_pago(pago_id: int, entrada: PagoEntrada, actor: str = Depends(actor_actual)) -> dict:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, pago_id)
        _validar_contrato(conexion, entrada)
        conexion.execute(
            """
            UPDATE pagos
            SET contrato_id = ?, precio = ?, deposito_garantia = ?, fecha_pago = ?,
                forma_pago = ?, estatus_pago = ?, extras = ?, actualizado_en = datetime('now')
            WHERE id = ?
            """,
            (
                entrada.contrato_id,
                entrada.precio,
                entrada.deposito_garantia,
                entrada.fecha_pago,
                entrada.forma_pago,
                entrada.estatus_pago,
                entrada.extras,
                pago_id,
            ),
        )
        conexion.commit()
        pago = _obtener(conexion, pago_id)
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="editar_pago",
        area="pagos",
        referencia=str(pago_id),
        resumen=f"Se editó el pago {pago_id}.",
        origen_dato="real",
    )
    return pago


@router.delete("/api/pagos/{pago_id}", status_code=204)
def eliminar_pago(pago_id: int, actor: str = Depends(actor_actual)) -> None:
    conexion = conectar_con_filas()
    try:
        _obtener(conexion, pago_id)
        conexion.execute("DELETE FROM pagos WHERE id = ?", (pago_id,))
        conexion.commit()
    finally:
        conexion.close()

    registrar(
        actor=actor,
        tipo="solicitada",
        accion="eliminar_pago",
        area="pagos",
        referencia=str(pago_id),
        resumen=f"Se eliminó el pago {pago_id}.",
        origen_dato="real",
    )


@router.post("/api/pagos/registrar")
def registrar_pago(entrada: RegistrarPagoEntrada, actor: str = Depends(actor_actual)) -> dict:
    """Marca como pagado el pago pendiente de un contrato. Es la operación que
    usan tanto el Dashboard como Vania (por ejemplo: "Vania, registra que la
    oficina 204 pagó septiembre por transferencia")."""
    conexion = conectar_con_filas()
    try:
        fila = conexion.execute(
            """
            SELECT * FROM pagos
            WHERE contrato_id = ? AND estatus_pago = 'pendiente'
            ORDER BY id LIMIT 1
            """,
            (entrada.contrato_id,),
        ).fetchone()
        if fila is None:
            raise HTTPException(status_code=404, detail=MENSAJE_SIN_PAGO_PENDIENTE)

        pago_id = fila["id"]
        conexion.execute(
            """
            UPDATE pagos
            SET estatus_pago = 'pagado', forma_pago = ?, fecha_pago = ?,
                actualizado_en = datetime('now')
            WHERE id = ?
            """,
            (entrada.forma_pago, date.today().isoformat(), pago_id),
        )
        conexion.commit()
        pago = _obtener(conexion, pago_id)
        numero_oficina = _numero_oficina_de_contrato(conexion, entrada.contrato_id)
    finally:
        conexion.close()

    periodo = entrada.periodo or "el periodo indicado"
    registrar(
        actor=actor,
        tipo="solicitada",
        accion="registrar_pago",
        area="pagos",
        referencia=str(pago_id),
        resumen=(
            f"Se registró el pago de {periodo} de la oficina {numero_oficina} "
            f"por {entrada.forma_pago}."
        ),
        origen_dato="real",
    )
    return pago
