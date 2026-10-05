# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es

Dashboard de Works (oficinas, inquilinos, contratos, pagos) para David y Grecia. **Vania** (asistente por WhatsApp, vía Hermes) lee el mismo estado y propone cambios por la misma API: "un solo cerebro, dos superficies". Hoy corre con **datos sintéticos**; el Excel real de Works todavía no existe. Código, comentarios, nombres y mensajes van en español.

## Comandos

```bash
# Instalación local
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m playwright install chromium

# Base local (var/works.db por defecto, o la ruta en WORKS_DB)
.venv/bin/python -m app.db.migrar
.venv/bin/python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion
.venv/bin/uvicorn app.main:app --reload

# Pruebas
.venv/bin/python -m pytest -q                                   # todo (API + UI con Playwright)
.venv/bin/python -m pytest -q tests/test_dat07_estado.py        # un archivo
.venv/bin/python -m pytest -q tests/test_dat07_estado.py -k nombre   # una prueba
.venv/bin/python -m pytest -q --ignore=tests/ui                 # sin navegador

# Contraste WCAG de los tokens de color (también lo corre test_ui03)
python scripts/contraste.py web/estilos/tokens.css

# Despliegue (ver docs/despliegue-docker.md)
docker compose up -d --build     # host 127.0.0.1:8010 -> contenedor 8000
```

No hay linter configurado. **Nunca uses `docker compose down -v`**: borra el volumen `works_datos` con la base y `works_cuentas.json`.

## Arquitectura

**Servidor (`app/`)** — FastAPI + SQLite, sin ORM (`sqlite3` con `row_factory = Row`, `PRAGMA foreign_keys = ON`).
- `app/main.py` registra automáticamente todo módulo de `app/api/` que exponga `router`; agregar una ruta nueva = crear el módulo, sin tocar `main.py`. También sirve `web/` como estáticos en `/`.
- `app/db/migrar.py` aplica `app/db/migraciones/NNN_*.sql` en orden y anota cada una en `migraciones_aplicadas`. Las migraciones son de solo avance: para cambiar el esquema se crea un archivo con número nuevo, nunca se edita uno aplicado. El contenedor corre `migrar` en cada arranque.
- `app/fuentes/`: `FuenteDatos` (`base.py`) es el contrato de cualquier fuente; `cargar.py` resuelve por convención `app.fuentes.<nombre>` → clase `Fuente<Nombre>` y recarga las cuatro áreas en una sola transacción (borra en orden inverso por las llaves foráneas). El Excel real entrará como otra fuente (`excel.py`).
- `app/estado/reglas.py` es un **módulo puro** (no toca base ni web): recibe los datos ya leídos y devuelve el estado conforme a `contratos/estado.schema.json`. Umbrales en `umbrales.toml`; toda la redacción de frases vive solo en `redaccion.py`. Ninguna regla genera un asunto sin un hecho concreto que lo sostenga. `/api/estado` (`app/api/estado.py`) solo lee y delega.
- `app/cambios/servicio.py`: las escrituras de las áreas **no se aplican directo**. Se crean como cambio `pendiente` (con vencimiento) y solo David o Grecia los confirman o descartan; al confirmar se aplican y queda historial. `duplicados.py` detecta cambios repetidos; `reporte.py` arma el reporte del día desde la tabla `cambios`. `app/actividad/registrar.py` deja el rastro de quién hizo qué.
- `app/seguridad/`:
  - `sesion.py`: entrada sin contraseña. Vania pide un enlace de un solo uso (10 min); al consumirlo se crea una sesión server-side (cookie `works_sesion`, solo se guarda el hash) que vence a las 18:00 o, si se entra después, a las 23:59 (America/Mexico_City). Los teléfonos de david/grecia vienen de `works_cuentas.json` (junto a la base, o `WORKS_CUENTAS_CONFIG`) o de `WORKS_WHATSAPP_*`.
  - `actor.py` (`actor_actual`, usado como `Depends`): Vania se identifica con `Authorization: Bearer $WORKS_TOKEN_VANIA`; en POST/PUT/DELETE además debe mandar `X-Works-Solicitante` y esa persona necesita **su propia sesión vigente** (`vania.py`), si no 401/403. Sin Bearer, se exige la cookie de sesión. El `ActorActual` distingue `ejecutor` (vania/dashboard) de `solicitante` (david/grecia).
- `app/api/avisos.py`: preferencias de avisos para Vania (silenciar asuntos) y avisos nuevos; cada asunto se avisa una sola vez (huella por asunto).

**Pantallas (`web/`)** — HTML/CSS/JS sin framework ni build, módulos ES con rutas absolutas. `app.js` es el punto de entrada; `datos/estado.js` llama a `/api/estado`. Navegación por hash en `navegacion/rutas.js`: las pantallas de detalle se cargan por convención desde `web/detalle/<area>.js` (cada una exporta `renderDetalle(contenedor, id)`), así que agregar un área no requiere editar `rutas.js`. Colores como tokens en `estilos/tokens.css`, con pares de contraste declarados en comentarios `/* par: --a sobre --b N */` que valida `scripts/contraste.py`. Inter y los íconos Lucide están incluidos localmente; `web/muestras/` son páginas de muestra usadas por las pruebas de UI.

**Contrato con Vania** — `contratos/estado.schema.json` (forma del estado compartido; las frases de los ejemplos son ilustrativas, no copiar) y `docs/contrato-vania.md` (rutas, encabezados, reglas). Reglas del esquema: `conclusion` sin `%` ni `$`, ningún indicador es "principal", fechas redactadas como persona ("vence en 12 días"), nunca `dd/mm/aaaa`.

## Pruebas

- Los archivos se nombran por el identificador de tarea del plan (`test_datNN_*`, `test_intNN_*`, `test_uiNN_*`).
- `tests/conftest.py` parchea `TestClient.__init__` para que cada cliente de la app entre ya con sesión de Grecia; `test_int13_acceso.py` es la excepción (prueba la regla 401 sin sesión). Las pruebas usan bases temporales vía `WORKS_DB` en `tmp_path`.
- `tests/ui/conftest.py` levanta uvicorn en un **puerto libre aleatorio** con una base temporal migrada y cargada con `sintetica/con_atencion`, e inyecta la cookie de sesión en Playwright. Las pruebas de UI corren en viewport móvil (390×844) y escritorio (1280×800).

## Repositorio

- `main` es la rama pública (GitHub, por defecto). La documentación de construcción (planes, decisiones, `Father.md`) vive en la rama local `master`, en el worktree `Works_construccion/`, y no se sube a GitHub.
- `.env`, `var/`, `datos_reales/` y `evidencia/` están en `.gitignore`; nunca se versionan.
