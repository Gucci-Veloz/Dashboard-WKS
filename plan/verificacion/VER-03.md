# VER-03 · Verificación de la fase 2

**Ejecutada:** 2026-09-26 · 06:01 CST  
**Ejecutor:** Builder_1 (Codex), en papel de Verificador  
**Estado:** COMPLETA

---

## Pruebas por tarea

| Tarea | Comando definido en el plan | Extracto real | Resultado |
|---|---|---|---|
| DAT-09 | `pytest tests/test_dat09_oficinas.py -q` | `3 passed, 1 warning in 1.37s` | **PASA** |
| DAT-10 | `pytest tests/test_dat10_inquilinos.py -q` | `3 passed, 1 warning in 1.33s` | **PASA** |
| DAT-11 | `pytest tests/test_dat11_contratos.py -q` | `4 passed, 1 warning in 1.77s` | **PASA** |
| DAT-12 | `pytest tests/test_dat12_pagos.py -q` | `4 passed, 1 warning in 2.17s` | **PASA** |
| UI-08 | `pytest tests/ui/test_ui08_navegacion.py` | `3 passed in 2.55s` | **PASA** |
| UI-09 | `pytest tests/ui/test_ui09_formulario.py` | `3 passed in 2.34s` | **PASA** |
| UI-10 | `pytest tests/ui/test_ui10_oficinas.py` | `2 passed in 2.45s` | **PASA** |
| UI-11 | `pytest tests/ui/test_ui11_inquilinos.py` | `2 passed in 2.34s` | **PASA** |
| UI-12 | `pytest tests/ui/test_ui12_contratos.py` | `3 passed in 2.85s` | **PASA** |
| UI-13 | `pytest tests/ui/test_ui13_pagos.py` | `1 passed in 2.16s` | **PASA** |

Todas se ejecutaron con `.venv/bin/python -m pytest <ruta>`, conservando los argumentos de cada prueba del plan. Las cuatro pruebas DAT emitieron una advertencia de deprecación de Starlette; no afectó el resultado.

La preparación de la base temporal para las revisiones fue:

```text
WORKS_DB=/tmp/builder1-ver03/works.db .venv/bin/python -m app.db.migrar
Migraciones aplicadas.
WORKS_DB=/tmp/builder1-ver03/works.db .venv/bin/python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion
Fuente 'sintetica' cargada.
```

---

## Revisión de VER-03

### Cada escritura deja actividad con el actor correcto

**Comandos corridos:**

```text
.venv/bin/python -m pytest tests/test_dat09_oficinas.py -q
.venv/bin/python -m pytest tests/test_dat10_inquilinos.py -q
.venv/bin/python -m pytest tests/test_dat11_contratos.py -q
.venv/bin/python -m pytest tests/test_dat12_pagos.py -q
rg -n -e '@router\.(post|put|delete)' -e 'def (crear|editar|eliminar|registrar)' -e 'registrar\(' -e 'actor: str = Depends\(actor_actual\)' app/api/oficinas.py app/api/inquilinos.py app/api/contratos.py app/api/pagos.py
```

**Resultado real:** las pruebas DAT pasaron **3 + 3 + 4 + 4**. Sus casos comprueban actividad con `dashboard` sin credencial y `vania` con `Bearer token-de-prueba`; DAT-12 además comprueba `registrar_pago` con `dashboard`. La inspección produjo los cuatro grupos de rutas POST/PUT/DELETE (y POST de registrar pago); cada escritura recibe `actor: str = Depends(actor_actual)` y cada una tiene una llamada posterior a `registrar(`.

**Verificación:** **OK**.

### El nivel 3 no aparece al abrir

**Comando corrido:**

```text
.venv/bin/python -m pytest tests/ui/test_ui08_navegacion.py -q
```

**Resultado real:**

```text
3 passed in 2.55s
```

El caso `test_al_cargar_no_hay_detalle_visible` verificó al cargar `/`: cero tablas, cero enlaces `.navegacion__volver` y cero encabezados con `Detalle`.

**Verificación:** **OK**.

### No hay chat dentro del Dashboard

**Comando corrido:**

```text
grep -rni "chat" web/
```

**Resultado real:** no produjo salida y terminó con código 1, que en `grep` significa que no encontró coincidencias.

**Revisión manual:** no hubo coincidencias que revisar.

**Verificación:** **OK**.

### `origen_dato`

**Resultado:** **CONTRADICCIÓN DEL PLAN** (no es falla del código).

**Comando corrido:**

```text
rg -n "CHECK \(origen_dato IN \('sintetico', 'real'\)\)|origen_dato=\"real\"|VALUES \([^\n]*'manual'" app/db/migraciones/002_actividad.sql app/api/oficinas.py app/api/inquilinos.py app/api/contratos.py app/api/pagos.py
```

**Resultado real:**

```text
app/db/migraciones/002_actividad.sql:15: origen_dato TEXT NOT NULL CHECK (origen_dato IN ('sintetico', 'real'))
app/api/oficinas.py:64: VALUES (?, ?, ?, ?, ?, 'manual', ?)
app/api/inquilinos.py:61: VALUES (?, ?, 'manual', ?)
app/api/contratos.py:83: VALUES (?, ?, ?, ?, ?, 'manual', ?)
app/api/pagos.py:99: VALUES (?, ?, ?, ?, ?, ?, 'manual', ?)
app/api/oficinas.py:81: origen_dato="real",
app/api/inquilinos.py:78: origen_dato="real",
app/api/contratos.py:107: origen_dato="real",
app/api/pagos.py:124: origen_dato="real",
```

El CHECK de `actividad` solo admite `sintetico` o `real`, mientras que las cuatro APIs insertan `manual` en los registros de negocio y envían `real` a `registrar(...)`. Esto choca con el texto del plan que pide `origen_dato='manual'` sin distinguir la tabla de actividad. La evidencia no muestra un error de código.

**Lo que sí importa:** las pruebas DAT-09, DAT-10 y DAT-11 comprobaron en la respuesta de creación `origen_dato == 'manual'`; la inserción de pagos quedó comprobada en `app/api/pagos.py:99`. Por tanto, lo creado desde la API no queda marcado como `sintetico`.

**Verificación:** **OK**, con la contradicción del plan documentada.

### Hallazgo previo de arquitectura

`import sqlite3` en `app/api/`: pendiente de decisión, ver VER-02.

---

## Tareas bloqueadas y decisiones

No hay tareas bloqueadas en la fase 2 ni D-x pendiente asociada: DAT-09, DAT-10, DAT-11, DAT-12, UI-08, UI-09, UI-10, UI-11, UI-12 y UI-13 tienen commit.

## Tabla resumen

| Elemento | Resultado | Evidencia |
|---|---|---|
| Pruebas de tareas | **PASA** | 10 de 10 archivos de prueba pasaron (30 pruebas) |
| Actividad y actor | **OK** | Pruebas DAT y revisión de las rutas de escritura |
| Nivel 3 al abrir | **OK** | UI-08, 3 pruebas pasaron |
| Chat en Dashboard | **OK** | `grep -rni "chat" web/` sin coincidencias |
| `origen_dato` | **CONTRADICCIÓN DEL PLAN** | `actividad`: `sintetico/real`; entidades API: `manual` |
| Bloqueos | **NINGUNO** | Las diez tareas tienen commit |

## Conclusión

**La fase 2 PASA.** Las diez pruebas prescritas pasaron. La actividad usa el actor correcto, el nivel 3 se mantiene oculto al abrir y no hay chat dentro del Dashboard. La diferencia entre `manual` para entidades y `real` para actividad es una contradicción del plan, no una falla del código.
