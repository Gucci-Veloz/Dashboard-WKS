# VER-04 · Verificación de las fases 3 y 4

Fecha: 2026-09-27  
Resultado: **PASA con 1 hallazgo medio**.

## Alcance y pruebas

- Suite completa, ejecutada en una copia del repositorio en `/tmp` para no regenerar evidencia de otros agentes: `.venv/bin/python -m pytest -q` → **150 passed, 1 warning** en 77.30 s. La advertencia es deprecación de `httpx` en `fastapi.testclient`; no hubo fallas.
- Pruebas dirigidas: `.venv/bin/python -m pytest tests/test_int02_api_actividad.py tests/test_int03_actividad_sintetica.py tests/test_int06_avisos.py tests/test_int07_preferencias.py tests/test_dat21_reporte.py -q` → **19 passed, 1 warning** en 11.64 s.
- Revisión manual exigida: `grep -rniE "wa\.me|whatsapp|smtp|sms" app/`. Los resultados de fuente fueron identificadores y configuración local de WhatsApp en `app/seguridad/vania.py:7-16`, `app/seguridad/admin.py:20-48,88-105`, `app/seguridad/sesion.py:29-37` y `app/api/acceso.py:35-48`. No hay cliente, URL ni llamada que envíe WhatsApp, correo o SMS a terceros. También hubo coincidencias binarias en `__pycache__`, sin evidencia adicional.
- Inspección del Reporte del día a 390×844 con datos sintéticos temporales y navegador automatizado: sin errores de JavaScript reportados. La captura auxiliar se dejó fuera del repositorio en `/tmp/ver04-reporte-ejecutores-390.png`.

## Resultado por criterio

### Avisos y estado dicen lo mismo — PASA

`GET /api/vania/avisos` lee los mismos datos y llama al mismo `calcular_estado()` que `GET /api/estado` (`app/api/avisos.py:12-15,252-258`; `app/api/estado.py:32-45`). La prueba compara cantidad, asuntos y frase de conclusión (`tests/test_int06_avisos.py:44-60`).

Las preferencias filtran solo la salida de avisos (`app/api/avisos.py:260-283`); el estado no se modifica. La prueba conserva exactamente los asuntos del estado al silenciar contratos (`tests/test_int07_preferencias.py:47-72`). Además, el mismo asunto no se repite hasta que cambia o reaparece y el paso de un día por sí solo no lo reactiva (`tests/test_int07_preferencias.py:97-173`).

### `204` cuando no hay nada — PASA

Cuando no quedan asuntos nuevos, el endpoint devuelve `Response(status_code=204)` (`app/api/avisos.py:288-289`). Se comprobó tanto con el escenario tranquilo (`tests/test_int06_avisos.py:38-41`) como tras haber avisado una vez (`tests/test_int07_preferencias.py:97-101`).

### Ningún endpoint manda mensajes a terceros — PASA

La revisión manual del `grep` exigido solo encontró resolución de identidad, almacenamiento local de teléfonos y generación de un enlace interno. `GET /api/vania/avisos` se limita a devolver JSON o `204` (`app/api/avisos.py:244-298`). No se encontró ningún mecanismo de envío a WhatsApp, SMTP o SMS dentro de `app/`.

### Actividad sintética marcada — PASA

El cargador registra todos los movimientos con `actor="vania"` y `origen_dato="sintetico"` (`app/fuentes/actividad_sintetica.py:42-48`). La prueba valida esos dos campos en cada fila y que todas las referencias existan (`tests/test_int03_actividad_sintetica.py:42-53`).

### Rastro de Vania y correcciones humanas en el reporte — PASA

La API conserva `solicitante=grecia` y `ejecutor=vania` en el reporte (`tests/test_dat21_reporte.py:63-77`). En la inspección a 390 px se observaron dos filas sintéticas del mismo registro:

- Alta ejecutada por Vania: la columna Ejecutor mostró **Vania**, en azul `#0758b8` y peso 700.
- Corrección humana posterior: apareció como otra fila con concepto **Cambio de titular**, su observación y ejecutor `grecia`, en color principal `#202734` y peso 450.

La presentación corresponde a `web/reporte/reporte.js:12-30` y `web/reporte/reporte.css:77-80`: Vania recibe énfasis visual; una ejecución humana queda en el estilo normal. El reporte es el rastro aprobado por D-8; no se requirió una bitácora separada.

## Hallazgos

### H-01 · El contrato de Vania no documenta las rutas de preferencias

- **Gravedad:** media.
- **Archivo y líneas:** `docs/contrato-vania.md:29-40` enumera las rutas por intención, pero omite guardar, consultar y quitar preferencias. Las rutas existentes son `PATCH /api/vania/preferencias-avisos`, `GET /api/vania/preferencias-avisos` y `PATCH /api/vania/preferencias-avisos/quitar` (`app/api/avisos.py:158-241`).
- **Impacto:** la API cumple D-11 y sus pruebas pasan, pero quien conecta a Vania desde Hermes no tiene documentado cómo aplicar “por persona, tipo y hasta cuándo” ni cómo quitar el silencio.
- **Tarea que lo tocaría:** **INT-07** (corrección documental en `docs/contrato-vania.md`, propiedad de Builder_Integraciones).

## NO VERIFICADO

Nada dentro del alcance no manual de VER-04. La operación real dentro de Hermes y los envíos por WhatsApp corresponden a MAN-01, MAN-02 y MAN-03, excluidas expresamente de esta verificación.
