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
| DAT-06 | Fuente sintética con dos escenarios | hecha (pendiente de hash) | DAT-05, DAT-03 |
| DAT-07 | Motor del estado de atención | pendiente | D-3, DAT-06 |
| DAT-08 | Endpoint del estado | pendiente | D-3, DAT-07 |
| DAT-09 | API de oficinas | pendiente | DAT-04, INT-01, INT-04 |
| DAT-10 | API de inquilinos | pendiente | DAT-09 |
| DAT-11 | API de contratos | pendiente | DAT-10 |
| DAT-12 | API de pagos y registrar pago | pendiente | DAT-11 |
| DAT-13 | Datos mínimos de personas para el pizarrón | pendiente | D-10, DAT-09 |
| DAT-14 | Mapeo del Excel al modelo | pendiente | U-1 (Excel) |
| DAT-15 | Fuente Excel | pendiente | DAT-14, INT-13 |
| DAT-16 | Reporte de calidad de la importación | pendiente | DAT-15 |

## Qué sigue

DAT-07 espera D-3 (resuelta) y DAT-06 (ya hecha): disponible.

## Observaciones

Mejoras o dudas que no se convierten en requisito. La sesión maestra las revisa.

(ninguna)

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
- 2026-09-23 05:33 · DAT-06 · hecha (pendiente de hash) · prueba pasa (4 passed); carga real por CLI con --escenario con_atencion sin error (21/21/21/21)
