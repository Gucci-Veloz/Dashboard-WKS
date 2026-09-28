# Dashboard de Works

Tablero web para **David y Grecia** que muestra cómo está Works (oficinas,
inquilinos, contratos y pagos) y qué requiere atención hoy.

**Vania**, la asistente por WhatsApp, lee el mismo estado y registra cambios a
través de la API del tablero. Un solo cerebro, dos superficies: lo que ve el
tablero y lo que dice Vania salen de la misma base.

> **Estado:** construido y probado (150 pruebas automáticas pasan). Por ahora
> corre con **datos sintéticos**; el Excel real de Works todavía no existe.

## Qué hace

- **Tablero principal:** el estado de cada área con semáforo (verde, ámbar, rojo)
  y lo que pide atención.
- **Detalle por área:** oficinas, inquilinos, contratos y pagos.
- **Cambios pendientes:** lo que Vania propone no se aplica solo. David o Grecia
  lo confirman o lo descartan desde el tablero, y el sistema detecta duplicados.
- **Reporte del día:** qué cambió y quién lo hizo.
- **Entrada sin contraseña:** Vania manda por WhatsApp un enlace de un solo uso
  que dura 10 minutos. La sesión dura hasta las 18:00 o, si se entra después,
  hasta las 23:59 (hora de la Ciudad de México).
- **Avisos para Vania:** qué asuntos avisar y cuáles silenciar; cada asunto se
  avisa una sola vez.

## Tecnología

- **Servidor:** Python 3.10+ con FastAPI y Uvicorn.
- **Base de datos:** SQLite, con migraciones que se aplican solas al arrancar.
- **Pantallas:** HTML, CSS y JavaScript sin framework; la tipografía Inter y los
  íconos Lucide van incluidos en el proyecto.
- **Pruebas:** pytest y Playwright.
- **Despliegue:** un solo contenedor con Docker Compose.

## Estructura

| Carpeta | Qué contiene |
|---|---|
| `app/` | El servidor: API, base de datos, reglas del semáforo, fuentes de datos y seguridad. |
| `web/` | Las pantallas del tablero. |
| `contratos/` | El esquema JSON del estado y ejemplos. |
| `docs/` | La guía de despliegue y el contrato con Vania. |
| `datos_sinteticos/` | Notas sobre los datos de prueba. |
| `scripts/` | Utilidades (revisión de contraste de colores). |
| `tests/` | Pruebas de API y de pantallas. |

## Ponerlo en marcha en el servidor (Docker)

```bash
git clone https://github.com/Gucci-Veloz/Dashboard-WKS.git
cd Dashboard-WKS
cp .env.example .env          # llena WORKS_TOKEN_VANIA
docker compose up -d --build
curl http://127.0.0.1:8000/api/salud   # {"ok":true}
```

El puerto `8000` solo escucha dentro del servidor. La dirección pública y el
**https (obligatorio: sin él no se guarda la sesión)** los pone el proxy del
servidor, que reenvía a `127.0.0.1:8000`.

Cuentas, carga de datos, actualización y respaldos:
**[docs/despliegue-docker.md](docs/despliegue-docker.md)**.

> **Nunca uses `docker compose down -v`:** borra el volumen con la base de datos.

## Correrlo en tu computadora

```bash
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m playwright install chromium

.venv/bin/python -m app.db.migrar
.venv/bin/python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion
.venv/bin/uvicorn app.main:app --reload
```

Pruebas:

```bash
.venv/bin/python -m pytest -q
```

## Configuración

| Variable | Para qué sirve |
|---|---|
| `WORKS_TOKEN_VANIA` | Contraseña con la que Vania se identifica ante la API. **Obligatoria.** |
| `WORKS_DB` | Ruta del archivo de la base de datos. |
| `WORKS_CUENTAS_CONFIG` | Ruta del archivo con los teléfonos de David y Grecia. |
| `WORKS_WHATSAPP_DAVID`, `WORKS_WHATSAPP_GRECIA` | Opcionales; es mejor registrar los teléfonos con el comando de la guía. |

El archivo `.env` nunca se sube al repositorio.

## Para quien integra a Vania

La API vive bajo `/api/…`. Vania manda `Authorization: Bearer <WORKS_TOKEN_VANIA>`
en cada llamada y, para crear, modificar, borrar o confirmar,
`X-Works-Solicitante: <número de WhatsApp>` de quien lo pidió.

Rutas, reglas y ejemplos: **[docs/contrato-vania.md](docs/contrato-vania.md)**.
