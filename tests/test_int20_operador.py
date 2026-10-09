"""Tercera persona `operador`: mismas reglas que David y Grecia, sin privilegios."""

import shutil
import sqlite3

import pytest
from fastapi.testclient import TestClient

from app.db import migrar as modulo_migrar
from app.db.conexion import conectar
from app.db.migrar import migrar
from app.main import app
from app.seguridad.admin import desactivar_cuenta
from app.seguridad.personas import PERSONAS


CREDENCIAL = {"Authorization": "Bearer token-de-prueba"}
DAVID = "+520000000001"
GRECIA = "+520000000002"
# Número falso; el real del operador nunca entra al repositorio.
OPERADOR = "5210000000005"


def _clientes(monkeypatch, tmp_path):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "token-de-prueba")
    monkeypatch.setenv("WORKS_WHATSAPP_DAVID", DAVID)
    monkeypatch.setenv("WORKS_WHATSAPP_GRECIA", GRECIA)
    monkeypatch.setenv("WORKS_WHATSAPP_OPERADOR", OPERADOR)
    migrar()
    cliente_usuario = TestClient(app, base_url="https://testserver")
    cliente_vania = TestClient(app, base_url="https://testserver")
    # El conftest abre una sesión de Grecia al crear cada cliente; aquí cada
    # prueba decide qué sesiones existen.
    conexion = conectar()
    try:
        conexion.execute("DELETE FROM sesiones")
        conexion.commit()
    finally:
        conexion.close()
    cliente_usuario.cookies.clear()
    cliente_vania.cookies.clear()
    return cliente_usuario, cliente_vania


def _entrar(cliente, numero):
    enlace = cliente.post(
        "/api/acceso/enlace", params={"numero_whatsapp": numero}, headers=CREDENCIAL
    )
    assert enlace.status_code == 200
    token = enlace.json()["enlace"].split("token=", 1)[1]
    entrada = cliente.get("/api/acceso/entrar", params={"token": token})
    assert entrada.status_code == 200
    return entrada.json()


def _como(numero):
    return {**CREDENCIAL, "X-Works-Solicitante": numero}


def _proponer(cliente_vania, numero, oficina="204"):
    respuesta = cliente_vania.post(
        "/api/oficinas", json={"numero": oficina}, headers=_como(numero)
    )
    assert respuesta.status_code == 201
    return respuesta.json()["id"]


def test_operador_pide_link_entra_propone_y_confirma_su_propio_cambio(monkeypatch, tmp_path):
    cliente_operador, cliente_vania = _clientes(monkeypatch, tmp_path)

    assert _entrar(cliente_operador, OPERADOR)["persona"] == "operador"
    assert cliente_operador.get("/api/estado").status_code == 200

    cambio_id = _proponer(cliente_vania, OPERADOR)
    pendiente = cliente_vania.get("/api/cambios", headers=CREDENCIAL).json()[0]
    assert pendiente["solicitante"] == "operador"
    assert pendiente["ejecutor"] == "vania"

    confirmacion = cliente_vania.post(
        f"/api/cambios/{cambio_id}/confirmar", headers=_como(OPERADOR)
    )
    assert confirmacion.status_code == 200
    oficinas = cliente_vania.get("/api/oficinas", headers=CREDENCIAL).json()
    assert [oficina["numero"] for oficina in oficinas] == ["204"]


def test_operador_no_confirma_ni_descarta_un_cambio_de_david(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes(monkeypatch, tmp_path)
    _entrar(cliente_usuario, DAVID)
    cambio_de_david = _proponer(cliente_vania, DAVID)
    _entrar(cliente_usuario, OPERADOR)

    for accion in ("confirmar", "descartar"):
        respuesta = cliente_vania.post(
            f"/api/cambios/{cambio_de_david}/{accion}", headers=_como(OPERADOR)
        )
        assert respuesta.status_code == 400
        assert "Solo la persona" in respuesta.json()["detail"]

    assert cliente_vania.get("/api/oficinas", headers=CREDENCIAL).json() == []
    pendiente = cliente_vania.get("/api/cambios", headers=CREDENCIAL).json()[0]
    assert pendiente["estado"] == "pendiente"


def test_david_y_grecia_no_confirman_un_cambio_del_operador(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes(monkeypatch, tmp_path)
    _entrar(cliente_usuario, OPERADOR)
    cambio_del_operador = _proponer(cliente_vania, OPERADOR)
    _entrar(cliente_usuario, DAVID)
    _entrar(cliente_usuario, GRECIA)

    for numero in (DAVID, GRECIA):
        respuesta = cliente_vania.post(
            f"/api/cambios/{cambio_del_operador}/confirmar", headers=_como(numero)
        )
        assert respuesta.status_code == 400
    assert cliente_vania.get("/api/oficinas", headers=CREDENCIAL).json() == []


def test_operador_sin_sesion_o_con_cuenta_apagada_no_escribe(monkeypatch, tmp_path):
    cliente_usuario, cliente_vania = _clientes(monkeypatch, tmp_path)
    sin_sesion = cliente_vania.post(
        "/api/oficinas", json={"numero": "204"}, headers=_como(OPERADOR)
    )
    assert sin_sesion.status_code == 401

    _entrar(cliente_usuario, OPERADOR)
    desactivar_cuenta("operador")
    apagada = cliente_vania.post(
        "/api/oficinas", json={"numero": "204"}, headers=_como(OPERADOR)
    )
    assert apagada.status_code == 401
    enlace = cliente_vania.post(
        "/api/acceso/enlace", params={"numero_whatsapp": OPERADOR}, headers=CREDENCIAL
    )
    assert enlace.status_code == 403


def test_cada_quien_cambia_solo_sus_propios_avisos(monkeypatch, tmp_path):
    _, cliente_vania = _clientes(monkeypatch, tmp_path)
    ruta = "/api/vania/preferencias-avisos"

    propia = cliente_vania.patch(
        ruta, json={"tipo_evento": "contratos"}, headers=_como(OPERADOR)
    )
    assert propia.status_code == 200
    assert propia.json()["persona"] == "operador"

    ajena = cliente_vania.patch(
        ruta, json={"persona": "grecia", "tipo_evento": "pagos"}, headers=_como(OPERADOR)
    )
    assert ajena.status_code == 403
    quitar_ajena = cliente_vania.patch(
        ruta + "/quitar",
        params={"persona": "david", "tipo_evento": "contratos"},
        headers=_como(OPERADOR),
    )
    assert quitar_ajena.status_code == 403
    sin_remitente = cliente_vania.patch(
        ruta, json={"persona": "operador", "tipo_evento": "pagos"}, headers=CREDENCIAL
    )
    assert sin_remitente.status_code == 403

    mias = cliente_vania.get(ruta, headers=_como(OPERADOR)).json()["preferencias"]
    assert [(p["persona"], p["tipo_evento"]) for p in mias] == [("operador", "contratos")]
    assert cliente_vania.get(
        ruta, params={"persona": "grecia"}, headers=_como(OPERADOR)
    ).status_code == 403

    guardadas = cliente_vania.get(ruta, headers=CREDENCIAL).json()["preferencias"]
    assert [(p["persona"], p["tipo_evento"]) for p in guardadas] == [
        ("operador", "contratos")
    ]


def test_migracion_009_conserva_los_datos_existentes(monkeypatch, tmp_path):
    base = tmp_path / "works.db"
    monkeypatch.setenv("WORKS_DB", str(base))
    anteriores = tmp_path / "migraciones_hasta_008"
    anteriores.mkdir()
    for archivo in sorted(modulo_migrar.MIGRACIONES_DIR.glob("*.sql")):
        if archivo.name < "009":
            shutil.copy(archivo, anteriores / archivo.name)
    monkeypatch.setattr(modulo_migrar, "MIGRACIONES_DIR", anteriores)
    migrar()

    conexion = sqlite3.connect(base)
    conexion.executescript(
        """
        UPDATE cuentas SET activa = 0 WHERE persona = 'david';
        INSERT INTO enlaces_acceso (persona, token_hash, creado_en, vence_en)
            VALUES ('grecia', 'h-enlace', '2026-10-01T09:00', '2026-10-01T09:10');
        INSERT INTO sesiones (persona, token_hash, creado_en, vence_en)
            VALUES ('grecia', 'h-sesion', '2026-10-01T09:01', '2026-10-01T18:00');
        INSERT INTO cambios (id, vence_en, estado, area, operacion, valores_anteriores,
                             valores_nuevos, observaciones, solicitante, ejecutor)
            VALUES (1, '2026-10-02', 'confirmado', 'oficinas', 'alta', '{}',
                    '{"numero": "101"}', 'nota', 'grecia', 'vania'),
                   (7, '2026-10-02', 'pendiente', 'pagos', 'modificacion', '{}',
                    '{}', NULL, 'david', 'david');
        DELETE FROM cambios WHERE id = 7;
        INSERT INTO preferencias_avisos (persona, tipo_evento, hasta, creado_en, actualizado_en)
            VALUES ('david', 'pagos', NULL, '2026-10-01', '2026-10-01');
        """
    )
    conexion.commit()
    conexion.close()

    monkeypatch.undo()
    monkeypatch.setenv("WORKS_DB", str(base))
    migrar()

    conexion = sqlite3.connect(base)
    try:
        assert conexion.execute(
            "SELECT persona, activa FROM cuentas ORDER BY persona"
        ).fetchall() == [("david", 0), ("grecia", 1), ("operador", 1)]
        assert conexion.execute("SELECT persona, token_hash FROM enlaces_acceso").fetchall() == [
            ("grecia", "h-enlace")
        ]
        assert conexion.execute("SELECT persona, token_hash FROM sesiones").fetchall() == [
            ("grecia", "h-sesion")
        ]
        assert conexion.execute(
            "SELECT id, estado, valores_nuevos, observaciones, solicitante, ejecutor FROM cambios"
        ).fetchall() == [(1, "confirmado", '{"numero": "101"}', "nota", "grecia", "vania")]
        assert conexion.execute(
            "SELECT persona, tipo_evento FROM preferencias_avisos"
        ).fetchall() == [("david", "pagos")]
        assert conexion.execute("PRAGMA foreign_key_check").fetchall() == []
        assert conexion.execute("PRAGMA integrity_check").fetchone() == ("ok",)
        # El siguiente cambio no reutiliza el número 7 que ya se había usado.
        conexion.execute(
            "INSERT INTO cambios (vence_en, estado, area, operacion, valores_anteriores,"
            " valores_nuevos, solicitante, ejecutor)"
            " VALUES ('2026-10-09', 'pendiente', 'oficinas', 'alta', '{}', '{}', 'operador', 'vania')"
        )
        assert conexion.execute("SELECT max(id) FROM cambios").fetchone() == (8,)
        assert conexion.execute(
            "SELECT 1 FROM sqlite_master WHERE name = 'cambios_pendientes_por_registro'"
        ).fetchone() == (1,)
    finally:
        conexion.close()


def test_la_base_acepta_exactamente_las_personas_del_codigo(monkeypatch, tmp_path):
    monkeypatch.setenv("WORKS_DB", str(tmp_path / "works.db"))
    migrar()
    conexion = sqlite3.connect(tmp_path / "works.db")
    try:
        assert [fila[0] for fila in conexion.execute(
            "SELECT persona FROM cuentas ORDER BY persona"
        )] == sorted(PERSONAS)
        for persona in PERSONAS:
            conexion.execute(
                "INSERT INTO preferencias_avisos VALUES (?, 'pagos', NULL, 'x', 'x')", (persona,)
            )
            conexion.execute(
                "INSERT INTO cambios (vence_en, estado, area, operacion, valores_anteriores,"
                " valores_nuevos, solicitante, ejecutor)"
                " VALUES ('x', 'pendiente', 'pagos', 'alta', '{}', '{}', ?, ?)",
                (persona, persona),
            )
        for intruso in ("vania", "admin"):
            with pytest.raises(sqlite3.IntegrityError):
                conexion.execute("INSERT INTO cuentas (persona) VALUES (?)", (intruso,))
            with pytest.raises(sqlite3.IntegrityError):
                conexion.execute(
                    "INSERT INTO preferencias_avisos VALUES (?, 'otro', NULL, 'x', 'x')",
                    (intruso,),
                )
    finally:
        conexion.close()
