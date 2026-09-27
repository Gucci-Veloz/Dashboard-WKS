# Estado · sesión maestra (Father)

Nota de relevo. **Con este archivo y `git log --oneline -10` basta para retomar.** No leas `REANUDAR.md` completo. Del plan, lee solo el bloque de la tarea que vayas a lanzar.

Última actualización: 2026-09-26, noche.

## 1. Cómo abrir una sesión nueva (para el usuario)
1. En la sesión vieja: `Ctrl + C` dos veces. Si pregunta por trabajos en segundo plano, elige "Exit and stop tasks".
2. En la terminal: `cd ~/Projects/DASHBOARDS/Works && claude`
3. Pega esto:
   > Eres Father, la sesión maestra de Works. Lee solo `plan/estado/Father.md` y `git log --oneline -10`. Háblame simple. Nada de lanzar tareas, hacer commits ni cambiar el plan sin mi `/luz-verde`.

## 2. Dónde vamos
- **Fase 2b: COMPLETA.** Todos los commits están en master: DAT-17 a DAT-22, INT-13, INT-14, INT-16, INT-17, UI-18, UI-19, UI-20, VER-09. 125 pruebas pasan; solo falla la histórica `test_dos_dispositivos_y_acceso_protegido`.
- **En curso: rediseño visual (fase 2c de `PLAN.md`).** Fuente de verdad: `plan/rediseno/DASHBOARD_DESIGN_SPEC.md` (ya revisado y limpio). Solo cambia el aspecto; la funcionalidad queda igual.
  - **UI-21 (base)** lanzada con Builder_UI en Codex. Al terminar: revisar, enseñarle al usuario las capturas de `evidencia/UI-21/` y, con su visto bueno, hacer el commit.
  - Después, **UI-22 (Builder_UI_2) y UI-23 (Builder_UI_3) en paralelo**; sus archivos no se cruzan. El encargo es igual, con el nombre del agente y la tarea.
  - Decisiones ya tomadas (en `DECISIONES.md`): el acento es azul `#0A66D9`; Inter y Lucide se guardan en el proyecto; el gris tenue no va en texto; verde, ámbar y rojo solo para estados; las pruebas existentes no se editan.
- **El resto del proyecto** (unas 17 tareas) continúa después del rediseño. Las decisiones D-6 a D-15 ya están respondidas en `plan/DECISIONES.md`.

## 3. Reglas del usuario
- **Luz verde:** `/luz-verde` = adelante. `/luz-amarilla` = espera. Sin luz verde no se lanzan tareas, no se cambia el plan y no se hacen commits fuera de rutina.
- **Commit de rutina** (permiso fijo): la prueba de la tarea pasa, no aparecen fallas nuevas en la suite y solo se tocaron los archivos de la tarea (los que dice `PLAN.md`). Si algo sale raro, no se hace commit y se le pregunta.
- **Cero tokens tirados:** no releer lo que ya se sabe; de las pruebas, leer solo el final.
- **Cómo hablarle:** frases simples, sin claves ni abreviaturas; di qué es cada cosa, no solo su número. Una pregunta a la vez, con la recomendación incluida. Nada de cuestionarios de opción múltiple. Español de México, con tuteo.
- **Lo que pida "para después"** se anota en `plan/PARA_DESPUES.md`, sin frenar el trabajo.

## 4. Cómo se lanza y se cierra una tarea
- Los agentes son Builder_Datos, Builder_Integraciones, Builder_UI y Builder_1 (verificación). Corren en **Codex**, **una tarea por vuelta**, y **no pueden hacer commit** (su `.git` es de solo lectura). Commit-Codex ya no existe: Father lanza, revisa y hace el commit.
- **Encargo** = una primera línea + las reglas de `plan/codex/reglas-agente.md` (sin su línea 1). Ejemplo:
  ```bash
  { echo "Eres **Builder_UI** del proyecto (repo actual). Tu tarea: **UI-18**."; tail -n +2 plan/codex/reglas-agente.md; } > <scratchpad>/ui18.md
  ```
- **Lanzar en fila y esperar** (en segundo plano; avisa cuando termina todo):
  `plan/codex/cadena.sh <encargo1> <encargo2> ...`
  El script lanza cada encargo, espera a que termine y sigue con el siguiente.
- **Ojo:** `status` escribe `| completed |`, no `Status: completed`. Por buscar el texto equivocado se perdieron unos 50 minutos el 2026-09-26.
- Consultar una tarea a mano: `node ~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs status <task-id> --cwd .`
- **Revisar antes del commit:** `git status --short` → la prueba de la tarea → toda la suite con `.venv/bin/python -m pytest -q 2>&1 | grep -E "FAILED|passed" | sed 's/ - .*//'`.
- **Fallas que ya había** y que no cuentan como nuevas (son 9): 8 en `tests/ui/test_ui10` a `test_ui13`, que UI-18 debe arreglar, y `test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`.
- Codex ya tiene su configuración lista (AppArmor para `bwrap` y `network_access = true`). No hay que tocarla.

## 5. Decisiones del usuario
- **D-6 a D-15: todas respondidas.** Ver `plan/DECISIONES.md`.
- **Siguen abiertos (no bloquean):** D-12, D-13 y D-14; U-1 (el Excel de Works, que todavía no existe); IP de la impresora (192.168.1.176, pendiente de confirmar).
- **Lección:** explicar cada decisión con un ejemplo concreto (quién, qué ve, qué pasa), nunca con el lenguaje del plan.

## 6. Sin commit todavía
- Solo `evidencia/UI-20/reporte-390.png` (captura regenerada) y lo que deje Builder_UI con UI-21.
