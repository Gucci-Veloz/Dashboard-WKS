import pytest
from fastapi import HTTPException

from app.seguridad.actor import actor_actual


def test_sin_credencial_devuelve_dashboard(monkeypatch):
    monkeypatch.delenv("WORKS_TOKEN_VANIA", raising=False)
    assert actor_actual(authorization=None) == "dashboard"


def test_credencial_valida_devuelve_vania(monkeypatch):
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "secreto-largo")
    assert actor_actual(authorization="Bearer secreto-largo") == "vania"


def test_credencial_invalida_falla(monkeypatch):
    monkeypatch.setenv("WORKS_TOKEN_VANIA", "secreto-largo")
    with pytest.raises(HTTPException) as excinfo:
        actor_actual(authorization="Bearer incorrecta")
    assert excinfo.value.status_code == 401


def test_sin_variable_definida_con_credencial_falla(monkeypatch):
    monkeypatch.delenv("WORKS_TOKEN_VANIA", raising=False)
    with pytest.raises(HTTPException) as excinfo:
        actor_actual(authorization="Bearer cualquiera")
    assert excinfo.value.status_code == 401
