# Reglas que se pegan debajo de la primera línea de cada encargo de Codex

## Cómo trabajas (obligatorio)
- Sigue `plan/REANUDAR.md` ("Protocolo de un agente"), **con una excepción: NO haces commit ni `git add`** (tu aislamiento deja `.git` en solo lectura). Al terminar una tarea con su prueba en verde, márcala `hecha (pendiente de commit)` y agrega a tu bitácora una línea con **la lista exacta de archivos** que tocaste. El commit lo hace la sesión Father. Nunca uses `checkout`, `restore`, `reset`, `stash` ni `push`.
- **Haz UNA sola tarea por vuelta**: la primera disponible en tu estado. Luego termina.
- Lee: tu `plan/estado/<TuAgente>.md`; `plan/PLAN.md` (reglas generales, propiedad de archivos, "Fase 2b" completa y el bloque de tu tarea); `plan/REGLAS_OPERACION.md`; y "Respuestas" de `plan/DECISIONES.md`. Nada más de lo necesario.
- Si tu estado tiene una tarea `hecha (pendiente de commit)` o `bloqueada (entorno...)` que ya tiene commit (`git log --oneline --grep "^<ID>:"`), márcala `hecha (<hash>)`. Una tarea tuya "en curso" o a medias: termínala a partir de lo que hay, sin borrar.
- Escribe solo en los archivos de tu tarea y en tu estado. Hay otro agente trabajando en paralelo en la misma carpeta: no toques sus archivos, aunque veas cambios suyos sin commit.
- Usa `.venv/bin/python -m pytest`. Nada de datos reales (números de WhatsApp ficticios, como `+520000000001`). Nada de VPS.
- Si una regla de `REGLAS_OPERACION.md` o del plan necesita una definición que no está, o tu tarea necesita archivos fuera de su lista, **no lo supongas**: marca `bloqueada (<motivo>)` y termina.
- Español de México, con tuteo.
- Al final responde en máximo 6 líneas: la tarea, `hecha (pendiente de commit)` o `bloqueada (motivo)`, la lista de archivos y la prueba que corriste con su resultado.
