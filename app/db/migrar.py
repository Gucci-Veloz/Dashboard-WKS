import re
from pathlib import Path

from app.db.conexion import conectar

MIGRACIONES_DIR = Path(__file__).resolve().parent / "migraciones"
PATRON_NUMERO = re.compile(r"^(\d+)_")


def _crear_tabla_control(conexion):
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS migraciones_aplicadas (
            numero TEXT PRIMARY KEY,
            archivo TEXT NOT NULL,
            aplicada_en TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """
    )
    conexion.commit()


def _numeros_aplicados(conexion) -> set:
    filas = conexion.execute("SELECT numero FROM migraciones_aplicadas").fetchall()
    return {fila[0] for fila in filas}


def migrar() -> None:
    conexion = conectar()
    try:
        _crear_tabla_control(conexion)
        aplicadas = _numeros_aplicados(conexion)
        for archivo in sorted(MIGRACIONES_DIR.glob("*.sql")):
            coincidencia = PATRON_NUMERO.match(archivo.name)
            if not coincidencia:
                continue
            numero = coincidencia.group(1)
            if numero in aplicadas:
                continue
            conexion.executescript(archivo.read_text())
            conexion.execute(
                "INSERT INTO migraciones_aplicadas (numero, archivo) VALUES (?, ?)",
                (numero, archivo.name),
            )
            conexion.commit()
    finally:
        conexion.close()


if __name__ == "__main__":
    migrar()
    print("Migraciones aplicadas.")
