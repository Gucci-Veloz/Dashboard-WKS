from app.db.conexion import conectar

ACTORES = {"vania", "dashboard", "sistema"}
TIPOS = {"solicitada", "detectada", "automatica"}


def registrar(
    *,
    actor: str,
    tipo: str,
    accion: str,
    resumen: str,
    area: str | None = None,
    referencia: str | None = None,
    persona: str | None = None,
    origen_dato: str = "real",
) -> int:
    if actor not in ACTORES:
        raise ValueError(f"actor inválido: {actor!r}")
    if tipo not in TIPOS:
        raise ValueError(f"tipo inválido: {tipo!r}")

    conexion = conectar()
    try:
        cursor = conexion.execute(
            """
            INSERT INTO actividad (actor, persona, tipo, accion, area, referencia, resumen, origen_dato)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (actor, persona, tipo, accion, area, referencia, resumen, origen_dato),
        )
        conexion.commit()
        return cursor.lastrowid
    finally:
        conexion.close()
