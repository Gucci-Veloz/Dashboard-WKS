from __future__ import annotations

import os

from fastapi import Cookie, Header, HTTPException, Request

from app.seguridad.sesion import NOMBRE_COOKIE, persona_de_sesion
from app.seguridad.vania import solicitante_con_sesion


class ActorActual(str):
    """Actor compatible con el rastro existente y con identidad de la persona."""

    def __new__(cls, ejecutor: str, solicitante: str | None = None):
        instancia = super().__new__(cls, ejecutor)
        instancia.ejecutor = ejecutor
        instancia.solicitante = solicitante
        instancia.persona = solicitante
        return instancia


def actor_actual(
    request: Request = None,
    authorization: str | None = Header(default=None),
    sesion: str | None = Cookie(default=None, alias=NOMBRE_COOKIE),
    numero_solicitante: str | None = Header(default=None, alias="X-Works-Solicitante"),
) -> ActorActual:
    """Identifica a Vania o a una persona con sesión vigente.

    La ruta directa sin Request se conserva para las pruebas históricas de INT-04;
    FastAPI siempre inyecta Request y por eso exige acceso en las rutas.
    """
    if request is not None:
        sesion = request.cookies.get(NOMBRE_COOKIE)
        numero_solicitante = request.headers.get("X-Works-Solicitante")

    if authorization is not None:
        token_esperado = os.environ.get("WORKS_TOKEN_VANIA")
        esquema, _, credencial = authorization.partition(" ")
        if not token_esperado or esquema != "Bearer" or credencial != token_esperado:
            raise HTTPException(status_code=401)
        if request is not None and request.method in {"POST", "PUT", "DELETE"} and request.url.path != "/api/acceso/enlace":
            solicitante = solicitante_con_sesion(numero_solicitante, sesion)
            return ActorActual("vania", solicitante=solicitante)
        return ActorActual("vania")

    if request is None:
        return ActorActual("dashboard")

    persona = persona_de_sesion(sesion)
    if persona is None:
        raise HTTPException(status_code=401, detail={"codigo": "sin_sesion"})
    return ActorActual("dashboard", solicitante=persona)
