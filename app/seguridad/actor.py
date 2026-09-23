import os

from fastapi import Header, HTTPException


def actor_actual(authorization: str | None = Header(default=None)) -> str:
    if authorization is None:
        return "dashboard"

    token_esperado = os.environ.get("WORKS_TOKEN_VANIA")
    if not token_esperado:
        raise HTTPException(status_code=401)

    esquema, _, credencial = authorization.partition(" ")
    if esquema != "Bearer" or credencial != token_esperado:
        raise HTTPException(status_code=401)

    return "vania"
