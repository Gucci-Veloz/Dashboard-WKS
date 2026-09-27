# Estado · sesión maestra (Father)

Nota de relevo. **Con este archivo y `git log --oneline -10` basta para retomar.** No leas `REANUDAR.md` completo. Del plan, lee solo el bloque de la tarea que vayas a lanzar.

Última actualización: 2026-09-27, tarde (fase de la limpia).

## 1. Cómo abrir una sesión nueva (para el usuario)
1. En la sesión vieja: `Ctrl + C` dos veces. Si pregunta por trabajos en segundo plano, elige "Exit and stop tasks".
2. En la terminal: `cd ~/Projects/DASHBOARDS/Works && claude`
3. Pega esto:
   > Eres Father, la sesión maestra de Works. Lee solo `archivo_construccion/plan/estado/Father.md` y `git log --oneline -10`. Háblame simple: cuando tenga que decidir algo, nada de claves (INT-, UI-, D-), rutas ni palabras técnicas; dame un ejemplo de la oficina y una pregunta de sí o no con tu recomendación. Antes de proponerme una tarea, revisa que no choque con lo que ya decidí en `archivo_construccion/plan/DECISIONES.md`. Nada de lanzar tareas, hacer commits ni cambiar el plan sin mi `/luz-verde`.

## 2. Dónde vamos
- **Fase de la limpia (2026-09-27, commits `42012f4` y `286f124`):** todo el material de construcción (plan, capturas, scavenge, manuales, handshake y notas) vive en `archivo_construccion/`. En la raíz solo queda lo funcional: `app`, `web`, `contratos`, `docs`, `datos_sinteticos`, `scripts`, `tests` y `pyproject.toml`. `evidencia/` sigue en la raíz, pero ahora el historial la ignora (la suite la regenera). Las rutas de esta nota, de las reglas de los agentes, de `REANUDAR.md`, de `PLAN.md` y de `cadena.sh` ya apuntan a la nueva ubicación. El usuario dirá qué sigue después de la limpia.
- **Terminadas y con commit:** fases 0, 1, 2, 2b (reglas de operación), 2c (rediseño visual: UI-21, UI-22, UI-23), 3 y 4 (VER-04 pasó). Hoy también: INT-07 (silenciar avisos, cada asunto una sola vez) e INT-18 (arregló la prueba histórica).
- **Suite: 150 de 150, sin fallas.** Cualquier falla es nueva.
- **Cerradas sin código o NO autorizadas (2026-09-27, instrucción del usuario):**
  - UI-14 (rastro de Vania): la cubre el Reporte del día (D-8). UI-17 (efecto sorpresa): la cubrió el rediseño (D-15).
  - **Botón "seguir con Vania" (D-9, INT-08, UI-15): NO AUTORIZADO.** El usuario no lo quiere. Fase 5 completa fuera.
  - RES-01 (ya lo resuelve D-4), RES-02 (no autorizada), RES-04 (mal planteada: la impresora ya imprime PDF desde varias computadoras).
  - **Pizarrón de Grecia (DAT-13, INT-12, RES-03): no se toca salvo que Grecia lo pida.** Es un módulo para ofrecerle después.
- **Lo que queda y de qué depende:**
  - Fase 6, documento para imprimir (INT-09 → INT-10 → INT-11): D-7 = A (el Dashboard genera el PDF y Vania lo imprime con su herramienta de Hermes). Falta saber cómo recibe el archivo esa herramienta (U-3) y qué documento imprimir (D-6, espera el Excel). **Revisar primero si INT-09 puede avanzar sin U-3.**
  - Fase 9, datos reales (DAT-14, DAT-15, DAT-16, UI-16): esperan el Excel de Works (U-1).
  - Fase 10 y tareas MAN: las hace el usuario en Hermes y el VPS; esperan U-4 (dónde corre Hermes) y U-6 (dominio y HTTPS del VPS).
  - VER-05 (fases 5 a 7) y VER-06: cuando lo anterior esté hecho o bloqueado.
- **Lecciones de hoy:**
  - Antes de proponer una tarea vieja, compárala con el registro final de `DECISIONES.md` (línea ~420 en adelante). El plan tenía varias tareas ya decididas en contra.
  - Al pedir una decisión: ejemplo de la oficina, sí o no, recomendación, sin claves ni rutas. El usuario se enojó por explicaciones técnicas.
  - Codex tiene límite de uso. El 2026-09-27 se agotó a las 14:32 (se liberaba a las 16:01). Si una tarea falla en segundos, revisa el log antes de relanzar.
  - Ojo: `archivo_construccion/plan/estado/Builder_UI.md` ya marca UI-19 como hecha.
  - **Lección:** el usuario juzga el resultado a simple vista. No le presentes como listo algo que se ve débil: compáralo tú primero con las referencias (recorta de cerca con PIL y compara antes/después) y di con honestidad qué falla. Si el usuario manda una instrucción directa de diseño, guárdala en `archivo_construccion/plan/rediseno/` tal cual y ejecútala, sin debatir.
  - **Lección:** cuando el usuario dice "commitea ya", hazlo de inmediato con lo que no dependa de trabajo en curso; no lo hagas esperar.
  - **Cómo lanzar con esfuerzo alto:** `node ~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs task --background --write --fresh --effort high < <encargo>` y después esperar en segundo plano con un bucle de `status` que busque `| completed |` (hasta 40 minutos). Las vueltas de UI-21 tardaron entre 5 y 10 minutos. `cadena.sh` usa esfuerzo medio y solo espera 20 minutos.
  - Decisiones ya tomadas (en `DECISIONES.md`): Inter y Lucide se guardan en el proyecto; el gris tenue no va en texto; verde, ámbar y rojo solo para estados. En `PARA_DESPUES.md` quedaron el tablero principal visual (tema 3) y la familia de íconos que sustituirá a Lucide en ese tablero (tema 4).
- **El resto del proyecto** (unas 17 tareas) continúa después del rediseño. Las decisiones D-6 a D-15 ya están respondidas en `archivo_construccion/plan/DECISIONES.md`.

## 3. Reglas del usuario
- **Luz verde:** `/luz-verde` = adelante. `/luz-amarilla` = espera. Sin luz verde no se lanzan tareas, no se cambia el plan y no se hacen commits fuera de rutina.
- **Commit de rutina** (permiso fijo): la prueba de la tarea pasa, no aparecen fallas nuevas en la suite y solo se tocaron los archivos de la tarea (los que dice `PLAN.md`). Si algo sale raro, no se hace commit y se le pregunta.
- **Cero tokens tirados:** no releer lo que ya se sabe; de las pruebas, leer solo el final.
- **Cómo hablarle:** frases simples, sin claves ni abreviaturas; di qué es cada cosa, no solo su número. Una pregunta a la vez, con la recomendación incluida. Nada de cuestionarios de opción múltiple. Español de México, con tuteo.
- **Lo que pida "para después"** se anota en `archivo_construccion/plan/PARA_DESPUES.md`, sin frenar el trabajo.

## 4. Cómo se lanza y se cierra una tarea
- Los agentes son Builder_Datos, Builder_Integraciones, Builder_UI y Builder_1 (verificación). Corren en **Codex**, **una tarea por vuelta**, y **no pueden hacer commit** (su `.git` es de solo lectura). Commit-Codex ya no existe: Father lanza, revisa y hace el commit.
- **Encargo** = una primera línea + las reglas de `archivo_construccion/plan/codex/reglas-agente.md` (sin su línea 1). Ejemplo:
  ```bash
  { echo "Eres **Builder_UI** del proyecto (repo actual). Tu tarea: **UI-18**."; tail -n +2 archivo_construccion/plan/codex/reglas-agente.md; } > <scratchpad>/ui18.md
  ```
- **Lanzar en fila y esperar** (en segundo plano; avisa cuando termina todo):
  `archivo_construccion/plan/codex/cadena.sh <encargo1> <encargo2> ...`
  El script lanza cada encargo, espera a que termine y sigue con el siguiente.
- **Ojo:** `status` escribe `| completed |`, no `Status: completed`. Por buscar el texto equivocado se perdieron unos 50 minutos el 2026-09-26.
- Consultar una tarea a mano: `node ~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs status <task-id> --cwd .`
- **Revisar antes del commit:** `git status --short` → la prueba de la tarea → toda la suite con `.venv/bin/python -m pytest -q 2>&1 | grep -E "FAILED|passed" | sed 's/ - .*//'`.
- **Fallas que ya había:** ninguna. Desde INT-18 (2026-09-27) la suite completa pasa; cualquier falla es nueva.
- Codex ya tiene su configuración lista (AppArmor para `bwrap` y `network_access = true`). No hay que tocarla.

## 5. Decisiones del usuario
- **D-6 a D-15: todas respondidas.** Ver `archivo_construccion/plan/DECISIONES.md`.
- **Siguen abiertos (no bloquean):** D-12, D-13 y D-14; U-1 (el Excel de Works, que todavía no existe); IP de la impresora (192.168.1.176, pendiente de confirmar).
- **Lección:** explicar cada decisión con un ejemplo concreto (quién, qué ve, qué pasa), nunca con el lenguaje del plan.

## 6. Sin commit todavía
- Nada. Las capturas viejas ya quedaron en commits y la copia duplicada del contrato se borró.
- **La falla histórica ya no existe:** INT-18 (`2026-09-27`) arregló `test_dos_dispositivos_y_acceso_protegido`. Desde entonces la suite completa pasa sin fallas (150). Cualquier falla es nueva.
