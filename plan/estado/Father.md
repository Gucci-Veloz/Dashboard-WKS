# Estado · sesión maestra (Father)

Nota de relevo para retomar **sin releer todo**. Solo la sesión maestra escribe aquí. Si necesitas más detalle, lee solo la parte que haga falta de `PLAN.md` o de `DECISIONES.md` ("Respuestas").

Última actualización: 2026-09-26

## Cómo se trabaja ahora
- Los builders corren en **Codex**: Builder_Datos, Builder_Integraciones y Builder_UI. Builder_1 hace la verificación y la revisión.
- El aislamiento de Codex deja `.git` en solo lectura. Los agentes hacen **una tarea por vuelta** y no hacen commit.
- **Father lanza y cierra cada vuelta** (Commit-Codex ya no se usa, 2026-09-26). Permiso fijo del usuario para commits de rutina: la prueba de la tarea pasa, la suite no suma fallas nuevas y solo se tocan los archivos de la tarea. Si algo sale raro, se le pregunta.
- Ahorro de tokens (regla del usuario): leer solo el final de la salida de pruebas; no releer lo que ya se sabe.
- Si el usuario lanza una tarea desde su terminal, se revisa con `node <script> status <task-id> --cwd ~/Projects/DASHBOARDS/Works`.
- Fallas que ya había antes de la fase 2b (no las causa cada tarea): 8 en `tests/ui` y `test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`.
- Pruebas: `.venv/bin/python -m pytest` (no hay `pytest` suelto).
- Encargos de Codex: `/tmp/claude-1000/-home-gusta-Projects-DASHBOARDS-Works/5da4069b-b70e-41cc-9242-b523a05ca96d/scratchpad/` (`datos-siguiente.md`, `integ-siguiente.md`, `comun.md`). Se pierden si se reinicia la computadora; si pasa, hay que rehacerlos.
- Script de Codex: `~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs task --background --write --fresh --effort medium < encargo`. Cada sesión de Claude solo ve los trabajos que ella misma lanzó.
- Codex necesitó un perfil de AppArmor para `/usr/bin/bwrap` y `network_access = true` en `~/.codex/config.toml`. Ya están puestos.

## Dónde vamos: fase 2b (reglas de `plan/REGLAS_OPERACION.md`)
- **Hechas:** DAT-17, DAT-18, DAT-19, INT-13, INT-14, INT-16.
- **DAT-20: hecha pero sin commit, con una falla.** En los PUT, `crear_de_todos_modos` se queda en los valores y da 400 (rompe `test_dat19_api_cambios.py::test_put_solo_cambia_al_confirmar_y_se_lista_pendiente`). Hay que devolverla a Builder_Datos para que la corrija en las cuatro APIs.
- **Siguen:**
  - INT-17: ya puede arrancar.
  - DAT-21: espera DAT-20.
  - UI-18 a UI-20: Builder_UI ya puede arrancar.
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
