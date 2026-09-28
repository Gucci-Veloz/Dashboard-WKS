from fastapi import APIRouter

router = APIRouter()


@router.get("/api/salud")
def salud() -> dict:
    return {"ok": True}
