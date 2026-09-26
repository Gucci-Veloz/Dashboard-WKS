from fastapi import APIRouter, Query

from app.db.conexion import conectar_con_filas

router = APIRouter()


@router.get("/api/actividad")
def listar_actividad(
    actor: str | None = None,
    area: str | None = None,
    pagina: int = Query(default=1, ge=1),
    tamano_pagina: int = Query(default=20, ge=1, le=100),
) -> dict:
    condiciones = []
    parametros: list = []
    if actor:
        condiciones.append("actor = ?")
        parametros.append(actor)
    if area:
        condiciones.append("area = ?")
        parametros.append(area)
    where = f"WHERE {' AND '.join(condiciones)}" if condiciones else ""

    conexion = conectar_con_filas()
    try:
        total = conexion.execute(
            f"SELECT COUNT(*) FROM actividad {where}", parametros
        ).fetchone()[0]
        desplazamiento = (pagina - 1) * tamano_pagina
        filas = conexion.execute(
            f"SELECT * FROM actividad {where} ORDER BY momento DESC, id DESC LIMIT ? OFFSET ?",
            (*parametros, tamano_pagina, desplazamiento),
        ).fetchall()
    finally:
        conexion.close()

    return {
        "total": total,
        "pagina": pagina,
        "tamano_pagina": tamano_pagina,
        "resultados": [dict(fila) for fila in filas],
    }
