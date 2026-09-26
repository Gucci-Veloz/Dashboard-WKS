# Estado · sesión maestra (Father)

Nota de relevo para retomar **sin releer todo**. Solo la sesión maestra escribe aquí. Si necesitas más detalle, lee solo la parte que haga falta de `PLAN.md` o de `DECISIONES.md` ("Respuestas").

Última actualización: 2026-09-26

## Cómo se trabaja ahora
- Los builders corren en **Codex**: Builder_Datos, Builder_Integraciones y Builder_UI. Builder_1 hace la verificación y la revisión.
- El aislamiento de Codex deja `.git` en solo lectura. Los agentes hacen **una tarea por vuelta** y no hacen commit.
- La sesión de Claude **Commit-Codex** (Sonnet) cierra cada vuelta: espera al agente, corre la prueba, hace el commit con las rutas y lo relanza. Solo avisa a Father cuando algo se bloquea, cuando un agente se queda sin tareas o cuando ya puede arrancar Builder_UI.
- Encargos de Codex: `/tmp/claude-1000/-home-gusta-Projects-DASHBOARDS-Works/5da4069b-b70e-41cc-9242-b523a05ca96d/scratchpad/` (`datos-siguiente.md`, `integ-siguiente.md`, `comun.md`). Se pierden si se reinicia la computadora; si pasa, hay que rehacerlos.
- Script de Codex: `~/.claude/plugins/cache/openai-codex/codex/1.0.6/scripts/codex-companion.mjs task --background --write --fresh --effort medium < encargo`. Cada sesión de Claude solo ve los trabajos que ella misma lanzó.
- Codex necesitó un perfil de AppArmor para `/usr/bin/bwrap` y `network_access = true` en `~/.codex/config.toml`. Ya están puestos.

## Dónde vamos: fase 2b (reglas de `plan/REGLAS_OPERACION.md`)
- **Hechas:** DAT-17, DAT-18, INT-13, INT-14.
- **En curso:** DAT-19, con Builder_Datos.
- **Siguen:**
  - INT-16: ya autorizada con `sesion.py`; la relanza Commit-Codex.
  - INT-17: espera DAT-19.
  - DAT-20 y DAT-21: esperan DAT-19.
  - UI-18 a UI-20: Builder_UI arranca cuando DAT-19 e INT-14 tengan commit.
  - VER-09 con Builder_1, al final de la fase.
- **Al terminar la fase 2b:** reportar al usuario y proponer qué sigue.

## Pendiente del usuario
- **D-6 a D-15:** abiertas, excepto las que ya tienen respuesta en `DECISIONES.md`.
- **U-1 a U-6:** abiertos. El WhatsApp de Vania es **WhatsApp Web**. Vania ya conoce los números de David y de Grecia (no van en git).

## Cómo hablarle al usuario
- Es nuevo en esto: frases simples, sin claves ni abreviaturas, una pregunta a la vez y con la recomendación incluida.
- Nada de cuestionarios de opción múltiple. Español de México, con tuteo.
- Ni commits ni cambios al plan sin su `/luz-verde`.
