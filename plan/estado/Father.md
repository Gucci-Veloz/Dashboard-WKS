# Estado · sesión maestra (Father)

Nota de relevo para retomar **sin releer todo**. Solo la sesión maestra escribe aquí. Si necesitas más detalle, lee solo la parte que haga falta de `PLAN.md` o de `DECISIONES.md` ("Respuestas").

Última actualización: 2026-09-26

## Cómo se trabaja ahora
- Los builders corren en **Codex**: Builder_Datos, Builder_Integraciones y Builder_UI. Builder_1 hace la verificación y la revisión.
- El aislamiento de Codex deja `.git` en solo lectura. Los agentes hacen **una tarea por vuelta** y no hacen commit.
- **Father lanza y cierra cada vuelta** (Commit-Codex ya no se usa, 2026-09-26). **Antes de lanzar tareas, pedir `/luz-verde`.** Encargos nuevos: `/tmp/claude-1000/-home-gusta-Projects-DASHBOARDS-Works/b9cd5006-78dd-4925-82fc-b28f31da3cdf/scratchpad/` (`datos.md`, `integ.md`, `ui.md`). Permiso fijo del usuario para commits de rutina: la prueba de la tarea pasa, la suite no suma fallas nuevas y solo se tocan los archivos de la tarea. Si algo sale raro, se le pregunta.
- Ahorro de tokens (regla del usuario): leer solo el final de la salida de pruebas; no releer lo que ya se sabe.
- Para saber si una tarea terminó, `status` muestra `| completed |` (no `Status: completed`). Las esperas deben buscar eso.
- Si el usuario lanza una tarea desde su terminal, se revisa con `node <script> status <task-id> --cwd ~/Projects/DASHBOARDS/Works`.
- Fallas que ya había antes de la fase 2b (no las causa cada tarea): 8 en `tests/ui` y `test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`.
- Pruebas: `.venv/bin/python -m pytest` (no hay `pytest` suelto).
- Encargos de Codex: `/tmp/claude-1000/-home-gusta-Projects-DASHBOARDS-Works/5da4069b-b70e-41cc-9242-b523a05ca96d/scratchpad/` (`datos-siguiente.md`, `integ-siguiente.md`, `comun.md`). Se pierden si se reinicia la computadora; si pasa, hay que rehacerlos.
- Script de Codex: `~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs task --background --write --fresh --effort medium < encargo`. Cada sesión de Claude solo ve los trabajos que ella misma lanzó.
- Codex necesitó un perfil de AppArmor para `/usr/bin/bwrap` y `network_access = true` en `~/.codex/config.toml`. Ya están puestos.

## Dónde vamos: fase 2b (reglas de `plan/REGLAS_OPERACION.md`)
- **Hechas:** DAT-17 a DAT-20, INT-13, INT-14, INT-16, INT-17.
- **UI-18 bloqueada:** DAT-19 no tiene API para descartar un pendiente. Hay que decidir con el usuario quién la agrega (cambio al plan).
- **Siguen:**
  - DAT-21: ya puede arrancar.
  - UI-19 y UI-20: esperan UI-18.
  - VER-09 con Builder_1, al final de la fase.
- **Al terminar la fase 2b:** reportar al usuario y proponer qué sigue.

## Pendiente del usuario
- **D-6 a D-15:** abiertas, excepto las que ya tienen respuesta en `DECISIONES.md`.
- **U-1 a U-6:** abiertos. El WhatsApp de Vania es **WhatsApp Web**. Vania ya conoce los números de David y de Grecia (no van en git).

## Cómo hablarle al usuario
- Es nuevo en esto: frases simples, sin claves ni abreviaturas, una pregunta a la vez y con la recomendación incluida.
- Nada de cuestionarios de opción múltiple. Español de México, con tuteo.
- Cambios al plan sin su `/luz-verde`: nunca. Commits: solo los de rutina, con el permiso fijo de arriba.
- No gastar tokens en repetir cosas.
