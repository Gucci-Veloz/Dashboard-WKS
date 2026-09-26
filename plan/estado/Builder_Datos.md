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
| DAT-08 | Endpoint del estado | hecha (fac977b) | D-3, DAT-07 |
| DAT-09 | API de oficinas | hecha (8d9c352) | DAT-04, INT-01, INT-04 |
| DAT-10 | API de inquilinos | hecha (051e2d7) | DAT-09 |
| DAT-11 | API de contratos | hecha (b0159c3) | DAT-10 |
| DAT-12 | API de pagos y registrar pago | hecha (4bd23f6) | DAT-11 |
| DAT-13 | Datos mínimos de personas para el pizarrón | pendiente | D-10, DAT-09 |
| DAT-14 | Mapeo del Excel al modelo | pendiente | U-1 (Excel) |
| DAT-15 | Fuente Excel | pendiente | DAT-14, INT-13 |
| DAT-16 | Reporte de calidad de la importación | pendiente | DAT-15 |
| DAT-17 | Una sola forma de conectarse a la base | hecha (9641113) | VER-03 |
| DAT-18 | Cambios: pre-registro, confirmación e historial | hecha (e50b6af) | DAT-17 |
| DAT-19 | Las APIs de las cuatro áreas pasan por cambios | hecha (pendiente de commit) | DAT-18, INT-13 |
| DAT-20 | Aviso de posibles duplicados | pendiente | DAT-19 |
| DAT-21 | Reporte del día | pendiente | DAT-19 |

## Qué sigue

DAT-20 espera el commit de DAT-19.

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
- 2026-09-23 05:58 · DAT-08 · hecha (fac977b) · prueba pasa (4 passed); corregido bug de orden de borrado en app/fuentes/cargar.py (violaba llaves foráneas al recargar sobre datos existentes); suite completa 22 passed
- 2026-09-23 06:05 · DAT-09 · en curso · works-94 confirmó INT-01 (0fdc1c7) e INT-04 (222394d) hechas
- 2026-09-23 06:14 · DAT-09 · hecha (8d9c352) · prueba pasa (3 passed); actividad usa origen_dato='real' (no 'manual', esa columna solo admite sintetico/real); suite completa 40 passed
- 2026-09-23 06:15 · DAT-10 · en curso · espera DAT-09 cumplida
- 2026-09-23 06:22 · DAT-10 · hecha (051e2d7) · prueba pasa (3 passed)
- 2026-09-23 06:23 · DAT-11 · en curso · espera DAT-10 cumplida
- 2026-09-23 06:31 · DAT-11 · hecha (b0159c3) · prueba pasa (4 passed), incluida oficina inexistente → 400 con mensaje humano; suite completa 47 passed
- 2026-09-23 06:32 · DAT-12 · en curso · espera DAT-11 cumplida
- 2026-09-23 06:42 · DAT-12 · hecha (4bd23f6) · prueba pasa (4 passed), incluida la comprobación de que /api/estado pierde un asunto al registrar el pago pendiente; suite completa 51 passed
- 2026-09-26 06:24 · DAT-17 · en curso · espera VER-03 cumplida (2b60460)
- 2026-09-26 06:25 · DAT-17 · prueba pasa (pendiente de commit) · grep vacío y suite completa 92 passed
- 2026-09-26 06:26 · DAT-17 · bloqueada (entorno: `.git` es de solo lectura; `git commit` no pudo crear `index.lock`) · implementación y prueba quedan sin commit
- 2026-09-26 06:26 · DAT-18 · bloqueada (espera DAT-17 bloqueada)
- 2026-09-26 06:26 · DAT-19 · bloqueada (espera DAT-18 e INT-13 sin commit)
- 2026-09-26 07:22 · DAT-17 · hecha (9641113) · commit confirmado; estado reconciliado
- 2026-09-26 07:22 · DAT-18 · en curso · espera DAT-17 cumplida
- 2026-09-26 07:25 · DAT-18 · hecha (pendiente de commit) · prueba exacta pasa (5 passed); archivos: app/db/migraciones/008_cambios.sql, app/cambios/__init__.py, app/cambios/servicio.py, tests/test_dat18_cambios.py, plan/estado/Builder_Datos.md
- 2026-09-26 07:32 · DAT-18 · hecha (e50b6af) · commit confirmado; estado reconciliado
- 2026-09-26 07:32 · DAT-19 · en curso · esperas DAT-18 e INT-13 cumplidas
- 2026-09-26 07:38 · DAT-19 · hecha (pendiente de commit) · prueba exacta pasa (11 passed); archivos: app/api/oficinas.py, app/api/inquilinos.py, app/api/contratos.py, app/api/pagos.py, app/api/cambios.py, tests/test_dat09_oficinas.py, tests/test_dat10_inquilinos.py, tests/test_dat11_contratos.py, tests/test_dat12_pagos.py, tests/test_dat19_api_cambios.py, plan/estado/Builder_Datos.md
