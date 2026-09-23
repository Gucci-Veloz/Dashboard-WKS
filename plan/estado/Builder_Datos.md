# Estado · Builder_Datos

Solo **Builder_Datos** escribe en este archivo. Protocolo: `plan/REANUDAR.md`. Detalle de cada tarea: `plan/PLAN.md`.

Última actualización: 2026-09-23 · creado por el planificador (Mapping). Plan aprobado el 2026-09-23; D-1, D-2 y D-3 resueltas.

## En curso

(ninguna)

## Tareas

| ID | Título | Estado | Espera |
|---|---|---|---|
| DAT-01 | Esqueleto del servicio FastAPI | hecha (aaf12f0) | D-2 |
| DAT-02 | Conexión a SQLite y migraciones numeradas | hecha (42a94c8) | DAT-01 |
| DAT-03 | Contrato del estado de atención | hecha (4b97f20) | — (libre) |
| DAT-04 | Esquema de las cuatro áreas | hecha (8b32345) | DAT-02 |
| DAT-05 | Interfaz de fuentes de datos y cargador | hecha (762ec17) | DAT-04 |
| DAT-06 | Fuente sintética con dos escenarios | hecha (26b0f1e) | DAT-05, DAT-03 |
| DAT-07 | Motor del estado de atención | hecha (892a89a) | D-3, DAT-06 |
| DAT-08 | Endpoint del estado | hecha (pendiente de hash) | D-3, DAT-07 |
| DAT-09 | API de oficinas | pendiente | DAT-04, INT-01, INT-04 |
| DAT-10 | API de inquilinos | pendiente | DAT-09 |
| DAT-11 | API de contratos | pendiente | DAT-10 |
| DAT-12 | API de pagos y registrar pago | pendiente | DAT-11 |
| DAT-13 | Datos mínimos de personas para el pizarrón | pendiente | D-10, DAT-09 |
| DAT-14 | Mapeo del Excel al modelo | pendiente | U-1 (Excel) |
| DAT-15 | Fuente Excel | pendiente | DAT-14, INT-13 |
| DAT-16 | Reporte de calidad de la importación | pendiente | DAT-15 |

## Qué sigue

Sin tareas propias disponibles: DAT-09 espera INT-01 e INT-04 (Builder_Integraciones), DAT-13 espera D-10 y DAT-09, DAT-14 espera U-1 (Excel). Reviso si INT-01/INT-04 ya están hechas la próxima vez que retome.

## Observaciones

Mejoras o dudas que no se convierten en requisito. La sesión maestra las revisa.

- 2026-09-23: al construir DAT-08 encontré que `app/fuentes/cargar.py` (DAT-05) borraba las cuatro áreas en el mismo orden de inserción (oficinas, inquilinos, contratos, pagos), lo que rompe las llaves foráneas al recargar una base que ya tiene datos (pagos referencia contratos; contratos referencia oficinas e inquilinos). Lo corregí dentro de mi propio commit de DAT-08, cambiando solo el orden de borrado a inverso (`reversed(AREAS)`). No cambia ningún contrato ni decisión, es una corrección de un bug propio.

## Bitácora

Una línea por cambio, solo se agrega al final: `AAAA-MM-DD HH:MM · ID · estado · nota`.

- 2026-09-23 · — · creado · todas las tareas en pendiente
- 2026-09-23 04:58 · DAT-01 · en curso · D-2 resuelta (A + pip/venv + pytest, Python 3.10 mínimo)
- 2026-09-23 05:03 · DAT-01 · hecha (aaf12f0) · prueba pasa (2 passed); .venv creado con pip/venv, Playwright + Chromium instalados; git check-ignore confirma var/ y datos_reales/
- 2026-09-23 05:05 · DAT-03 · en curso · libre desde el inicio
- 2026-09-23 05:08 · DAT-03 · hecha (4b97f20) · las tres comprobaciones pasan; estado-tranquilo.json tiene asuntos: []
- 2026-09-23 05:09 · DAT-02 · en curso · espera DAT-01 cumplida
- 2026-09-23 05:13 · DAT-02 · hecha (42a94c8) · prueba pasa; grep de sqlite3 fuera de app/db/ vacío
- 2026-09-23 05:14 · DAT-04 · en curso · espera DAT-02 cumplida
- 2026-09-23 05:18 · DAT-04 · hecha (8b32345) · prueba pasa (4 passed): columnas, NOT NULL y CHECK de origen_dato
- 2026-09-23 05:19 · DAT-05 · en curso · espera DAT-04 cumplida
- 2026-09-23 05:24 · DAT-05 · hecha (762ec17) · prueba pasa (3 passed): fuente falsa carga, excel falla con el mensaje, carga parcial se revierte
- 2026-09-23 05:25 · DAT-06 · en curso · espera DAT-05 y DAT-03 cumplidas
- 2026-09-23 05:33 · DAT-06 · hecha (26b0f1e) · prueba pasa (4 passed); carga real por CLI con --escenario con_atencion sin error (21/21/21/21)
- 2026-09-23 05:34 · DAT-07 · en curso · D-3 resuelta (A) y DAT-06 cumplida
- 2026-09-23 05:45 · DAT-07 · hecha (892a89a) · prueba pasa (4 passed); grep sqlite3/fastapi en app/estado vacío; umbrales.toml con tomllib si hay 3.11+, con parser propio si no
- 2026-09-23 05:46 · DAT-08 · en curso · D-3 resuelta y DAT-07 cumplida
- 2026-09-23 05:58 · DAT-08 · hecha (pendiente de hash) · prueba pasa (4 passed); corregido bug de orden de borrado en app/fuentes/cargar.py (violaba llaves foráneas al recargar sobre datos existentes); suite completa 22 passed
