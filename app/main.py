import importlib
import pkgutil
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import api

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(title="Works")

for _, module_name, _ in pkgutil.iter_modules(api.__path__):
    modulo = importlib.import_module(f"app.api.{module_name}")
    router = getattr(modulo, "router", None)
    if router is not None:
        app.include_router(router)

if WEB_DIR.exists():
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
