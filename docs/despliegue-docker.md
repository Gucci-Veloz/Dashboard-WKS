# Despliegue del Dashboard con Docker Compose

Guía para levantar el Dashboard de Works en el VPS. Adáptala al protocolo del
servidor (carpetas, nombres, proxy y https); aquí solo va lo que el Dashboard
necesita.

## Qué hay en el proyecto

| Archivo | Para qué sirve |
|---|---|
| `Dockerfile` | La receta: arma una imagen con Python, `app/` y `web/`. Nada más entra. |
| `docker-compose.yml` | Cómo se levanta: dónde viven los datos, de dónde salen las claves y en qué puerto escucha. |
| `.dockerignore` | Lista blanca de lo que entra a la imagen. Pruebas, documentación y `archivo_construccion/` se quedan fuera. |
| `.env.example` | Plantilla de claves, sin valores. |

## 1. Primera vez en el servidor

```bash
cp .env.example .env        # llena WORKS_TOKEN_VANIA en el servidor, nunca en el repo
docker compose up -d --build
docker compose ps           # debe decir "healthy" a los ~30 segundos
curl http://127.0.0.1:8000/api/salud   # {"ok":true}
```

Al arrancar, el contenedor aplica solo las migraciones pendientes. No borra datos.

## 2. Cuentas de David y Grecia

Los teléfonos se guardan en `/datos/works_cuentas.json`, dentro del volumen:

```bash
docker compose exec works python -m app.seguridad.admin crear david  <número>
docker compose exec works python -m app.seguridad.admin crear grecia <número>
docker compose exec works python -m app.seguridad.admin listar
```

## 3. Datos

Mientras no exista el Excel de Works, se pueden cargar los datos sintéticos:

```bash
docker compose exec works python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion
```

**Ojo:** `cargar` vacía las cuatro áreas y las vuelve a llenar. No lo corras sobre datos reales.

## 4. Actualizar el Dashboard

```bash
git pull                     # o como el protocolo del VPS traiga el código
docker compose up -d --build
```

La base vive en el volumen `works_datos`: sobrevive a cada actualización.
**Nunca uses `docker compose down -v`**: la `-v` borra el volumen con la base.

## 5. Respaldo de la base

```bash
docker compose exec works python -c "import sqlite3; s=sqlite3.connect('/datos/works.db'); d=sqlite3.connect('/datos/respaldo.db'); s.backup(d)"
docker compose cp works:/datos/respaldo.db ./respaldo-$(date +%F).db
```

## Notas

- El puerto `8000` solo escucha dentro del servidor (`127.0.0.1`). La dirección
  pública y el https los pone el proxy del VPS, que debe reenviar a
  `127.0.0.1:8000`.
- La hora del contenedor es la de la Ciudad de México (`TZ`), igual que las sesiones.
- El contenedor corre con un usuario sin privilegios (`works`).
