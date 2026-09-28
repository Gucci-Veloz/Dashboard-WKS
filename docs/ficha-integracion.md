# Ficha del tablero · Dashboard de Works

**Última actualización:** 2026-09-27 · commit de referencia `50cbfea`
**Para qué sirve esta ficha:** es lo único que la sala de integración necesita saber del tablero. Si algo aquí cambia, se actualiza la ficha y su fecha. La sala **no** decide sobre lo que no esté escrito aquí: lo pregunta.

## 1. Qué es

Un tablero web para David y Grecia que muestra cómo está Works (oficinas, inquilinos, contratos y pagos) y qué requiere atención. Vania consulta el mismo estado y registra cambios a través de su API. **Un solo cerebro, dos superficies:** el tablero y Vania leen lo mismo.

- **Estado:** construido y probado (150 pruebas automáticas pasan). Corre hoy con **datos inventados**; el Excel real de Works todavía no existe.
- **Forma de entrega:** una sola caja Docker (`docker-compose.yml` en la raíz del repo). Guía completa: `docs/despliegue-docker.md`.

## 2. Qué ofrece

| Pieza | Dato |
|---|---|
| Servicio | Un contenedor, `works-dashboard`, imagen `works-dashboard:latest` |
| Puerto | `8010`, publicado solo en `127.0.0.1` del servidor (dentro del contenedor la app sigue en `8000`) |
| Pantallas | Se sirven desde la raíz `/` del mismo servicio |
| API | Bajo `/api/…`. Lista de rutas y reglas para Vania: `docs/contrato-vania.md` |
| Revisión de salud | `GET /api/salud` → `{"ok": true}` (sin credencial) |
| Datos | Un archivo SQLite dentro del volumen `works_datos` (montado en `/datos`) |

## 3. Qué necesita de cada proyecto

### Del proyecto del servidor (tiene la última palabra sobre el servidor)
1. **Dirección pública con https. Es obligatoria:** la sesión de David y Grecia usa una cookie marcada como segura, y el navegador no la guarda sin https. Sin https nadie puede entrar al tablero.
2. Un proxy que reciba esa dirección y reenvíe a `127.0.0.1:8010`, pasando los encabezados `X-Forwarded-*`.
3. Docker con Compose, y un lugar donde vivan el repo y el archivo `.env`, fuera del historial.
4. Respaldo periódico del volumen `works_datos` (la guía trae el comando).
5. Decidir por dónde llama Vania a la API: por la dirección pública o por una red interna del servidor.

### Del proyecto de Vania
1. Mandar `Authorization: Bearer <WORKS_TOKEN_VANIA>` en cada llamada.
2. Para crear, modificar, borrar o confirmar cambios, mandar además `X-Works-Solicitante: <número de WhatsApp>` de quien lo pidió.
3. **Enlace de entrada:** `POST /api/acceso/enlace?numero_whatsapp=…` devuelve una ruta relativa (`/acceso/?token=…`). **Vania le antepone la dirección pública del tablero** antes de mandarla por WhatsApp. El enlace dura 10 minutos y sirve una sola vez; la sesión dura hasta las 18:00 o, si se entra después de esa hora, hasta las 23:59 (hora de la Ciudad de México).
4. Respetar las reglas de `docs/contrato-vania.md`: no inventa datos, confirma antes de actuar, no contacta inquilinos, crea pendientes (no cambios oficiales) y pregunta "¿Sí o No?".

### Del proyecto de Dennis
- **Nada.** Dennis no toca el tablero: no recibe `WORKS_TOKEN_VANIA` ni ninguna ruta de la API. Si algún día lo necesita, se decide primero en la sala y se actualiza esta ficha.

## 4. Claves (solo nombres; los valores viven únicamente en el `.env` del servidor)

| Nombre | Qué es | Quién la usa |
|---|---|---|
| `WORKS_TOKEN_VANIA` | Contraseña de servicio de Vania ante la API | El tablero y Vania. La misma en ambos lados |
| `WORKS_WHATSAPP_DAVID`, `WORKS_WHATSAPP_GRECIA` | Opcionales: teléfonos de las cuentas | Solo el tablero. Es preferible darlos de alta con el comando de cuentas de la guía |

## 5. Reglas que no se negocian en la sala

- Nadie más que Vania escribe en la API del tablero.
- El tablero nunca manda mensajes a nadie; quien escribe por WhatsApp es Vania.
- `docker compose down -v` está prohibido en el servidor: borra la base de datos.
- Los datos reales solo entran por la carga del Excel, cuando exista. La carga vacía y vuelve a llenar las cuatro áreas.

## 6. Quién tiene la última palabra

El proyecto del Dashboard decide sobre sus pantallas, su API, sus reglas de estado y su base de datos. Todo lo que toca el servidor (dirección, proxy, carpetas, respaldos) lo decide el proyecto del servidor.

## 7. Lo que todavía no existe (no planear sobre esto como si ya estuviera)

| Pendiente | De qué depende |
|---|---|
| Datos reales | El Excel de Works |
| Documento para imprimir (PDF que Vania manda a la HP con su herramienta de Hermes) | Saber cómo recibe el archivo la herramienta de impresión de Vania y qué documento imprimir (se decide con el Excel) |
| Dirección pública y https | Proyecto del servidor |
| Dónde corre Hermes respecto al tablero | Proyecto del servidor y proyecto de Vania |

## 8. Respuestas a preguntas de otras fichas

Todavía ninguna: es la primera ficha que llega a la sala.

## 9. Preguntas abiertas para la sala

1. ¿Cuál será la dirección pública del tablero?
2. ¿Vania llama a la API por la dirección pública o por la red interna del servidor?
3. ¿Cómo recibe un archivo PDF la herramienta de impresión de Vania: una ruta, una dirección web o el contenido directo?
4. ¿Cada cuánto se respalda el volumen `works_datos` y a dónde va el respaldo?
