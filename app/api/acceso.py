from __future__ import annotations

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response

from app.main import app
from app.seguridad.actor import actor_actual
from app.seguridad.sesion import (
    NOMBRE_COOKIE,
    consumir_enlace,
    crear_enlace,
    persona_de_sesion,
    persona_por_whatsapp,
)

router = APIRouter()

RUTAS_ENTRADA = {"/api/acceso/enlace", "/api/acceso/entrar"}


@app.middleware("http")
async def exigir_acceso(request: Request, call_next):
    if not request.url.path.startswith("/api/") or request.url.path in {"/api/salud", *RUTAS_ENTRADA}:
        return await call_next(request)
    autorizacion = request.headers.get("Authorization")
    if autorizacion:
        try:
            actor_actual(request=request, authorization=autorizacion)
        except HTTPException as error:
            return Response(status_code=error.status_code, content='{"codigo":"sin_sesion"}', media_type="application/json")
    elif persona_de_sesion(request.cookies.get(NOMBRE_COOKIE)) is None:
        return Response(status_code=401, content='{"codigo":"sin_sesion"}', media_type="application/json")
    return await call_next(request)


@router.post("/api/acceso/enlace")
def pedir_enlace(
    numero_whatsapp: str,
    actor=Depends(actor_actual),
) -> dict:
    if actor != "vania":
        raise HTTPException(status_code=401)
    persona = persona_por_whatsapp(numero_whatsapp)
    if persona is None:
        raise HTTPException(status_code=403)
    enlace = crear_enlace(persona)
    return {
        "enlace": f"/acceso/?token={enlace['token']}",
        "vence_en": enlace["vence_en"],
    }


@router.get("/api/acceso/entrar")
def entrar(token: str, response: Response) -> dict:
    resultado = consumir_enlace(token)
    response.set_cookie(
        key=NOMBRE_COOKIE,
        value=resultado["token"],
        secure=True,
        httponly=True,
        samesite="strict",
        expires=resultado["vence_en"],
    )
    return {"persona": resultado["persona"], "vence_en": resultado["vence_en"]}
