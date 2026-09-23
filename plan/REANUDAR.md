# Reanudar · protocolo fijo

Este archivo lo sigue **cualquier agente** al empezar una sesión o al volver después de un corte (se acabaron los tokens, se cerró la sesión, el usuario se tuvo que ir). Todo el estado vive en disco y en git. Nada depende de lo que recuerde una sesión.

Archivos que cuentan:
- `plan/PLAN.md`: qué hay que hacer, en qué orden y quién lo hace.
- `plan/DECISIONES.md`: qué espera una decisión del usuario, y sus respuestas al final.
- `plan/estado/<Agente>.md`: el avance de cada agente. **Cada agente escribe solo en el suyo.**
- `git log`: lo que de verdad quedó terminado.

## Protocolo de un agente (Builder_UI, Builder_Datos, Builder_Integraciones, Verificador, Researcher)

### 1 · Leer

1. Tu archivo `plan/estado/<TuAgente>.md`.
2. `plan/PLAN.md`: las reglas generales, la tabla de propiedad de archivos y tus tareas.
3. La sección "Respuestas" de `plan/DECISIONES.md`, para saber qué D-x ya se resolvió.
4. `git log --oneline -15` y `git status --short`.

### 2 · Si hay una tarea "en curso" sin cerrar

No la empieces de cero y no borres nada.

1. Mira qué quedó a medias: `git status --short` y `git diff -- <archivos de la tarea>`. Los archivos de cada tarea están en su bloque de `PLAN.md`.
2. Comprueba si ya existe su commit: `git log --oneline --grep "^<ID>:"`.
   - **Si el commit existe:** la tarea terminó, pero el estado no alcanzó a actualizarse. Marca `hecha (<hash>)` y sigue al paso 5.
   - **Si no existe:** lee lo que hay, termina lo que falta a partir de ahí y corre la prueba.
3. Si lo que quedó está roto o no se entiende, **no hagas `git checkout`, `git restore`, `git reset` ni `git stash`**. Anota en tu estado `bloqueada (trabajo a medias que no entiendo: <detalle>)` y avisa a la sesión maestra en tu reporte final. Ella decide.

### 3 · Marcar "en curso" antes de empezar

1. Elige la **primera** tarea tuya en `pendiente` cuya columna "Espera" esté completa: tareas en `hecha` y D-x con respuesta. Si una tarea que esperas es de otro agente, revisa su estado en `plan/estado/<OtroAgente>.md` o su commit en `git log`.
2. Revisa la sección "Archivos compartidos que nunca se tocan al mismo tiempo" de `PLAN.md`. Si tu tarea toca `pyproject.toml`, confirma que ninguna de las otras tareas que lo tocan (DAT-01, INT-09, DAT-15) esté `en curso` en otro archivo de estado.
3. En tu archivo de estado, cambia la tarea a `en curso`, pon la fecha y hora en "En curso", y agrega una línea a la bitácora. **Guarda el archivo antes de tocar cualquier otro.**

### 4 · Al terminar

1. Corre la prueba exacta de la tarea, tal como aparece en `PLAN.md`.
2. **Si falla**, arréglalo dentro de los archivos de la tarea. Si no se puede sin tocar archivos de otro agente, marca `bloqueada (motivo)` y sigue al paso 5.
3. **Si pasa:**
   1. Marca la tarea `hecha` en tu estado, deja "En curso" vacío y escribe en "Qué sigue" tu próxima tarea disponible.
   2. Agrega solo tus archivos: `git add <archivos de la tarea> plan/estado/<TuAgente>.md`. **Nunca uses `git add -A` ni `git add .`.**
   3. Haz el commit con el mensaje sugerido en `PLAN.md`: `git commit -m "<ID>: <descripción>"`.
   4. Anota el hash en tu estado: `hecha (<hash>)`. Esta anotación queda sin commit hasta tu siguiente tarea, y está bien así. En el paso 2, `git log --grep` resuelve cualquier duda.
4. Si `git commit` falla porque existe `.git/index.lock`, otra sesión está haciendo commit. Espera unos segundos y reintenta. No borres el lock mientras otra sesión esté activa.
5. **Nadie hace push.** No hay remoto.

### 5 · Si está bloqueada

Márcala `bloqueada (<motivo>)`, con el motivo concreto: "requiere D-3 del usuario", "espera DAT-08", "U-3: falta el formato de impresión de Hermes". Agrega una línea a la bitácora y pasa a tu siguiente tarea disponible. Si no te queda ninguna, escribe en "Qué sigue": "sin tareas disponibles: espero <lista>", y termina.

### Reglas que no cambian

- No reabras decisiones del handshake. Si encuentras una mejora, va en "Observaciones" de tu estado, no en el código.
- No escribas fuera de los archivos de tu tarea y de tu estado.
- No toques el VPS. Si algo lo necesita, es MANUAL y lo hace el usuario.
- No leas ni subas datos reales a git.
- Escribe en español de México (tuteo).

## Protocolo de la sesión maestra

La sesión maestra coordina: revisa, responde dudas, anota decisiones y lleva `plan/estado/Manual.md`. No construye.

### Si se pierde la sesión maestra actual: cómo retoma una nueva

1. Lee, en este orden:
   - `handshake_vania_dashboard.md`, secciones "Decisiones ya tomadas", "Decisiones todavía abiertas" y "Resultado del grilling".
   - `plan/PLAN.md`, `plan/DECISIONES.md` (sobre todo "Respuestas") y este archivo.
   - Todos los `plan/estado/*.md`.
   - `plan/verificacion/` y `plan/investigacion/`, si tienen contenido.
2. Reconstruye la foto:
   - `git log --oneline`: cada commit empieza con el ID de su tarea.
   - Compara con los archivos de estado. Una tarea con commit pero sin `hecha` quedó cortada después del commit. Una tarea `hecha` sin commit es un error que hay que revisar.
   - `git status --short`: archivos sin commit indican una tarea en curso. Localiza de quién es con la tabla de propiedad de `PLAN.md`.
3. Revisa si hay sesiones de agentes vivas antes de mandarles nada. Pregúntale al usuario si hace falta.
4. Resume al usuario, en pocas líneas: qué está hecho, qué está en curso, qué está bloqueado y qué D-x o U-x faltan.
5. No liberes tareas nuevas ni cambies el plan sin la luz verde del usuario.

### Cuando el usuario responde una D-x

1. Copia la respuesta, con fecha, a "Respuestas" en `plan/DECISIONES.md`.
2. Si la respuesta cambia rutas o comandos, por ejemplo si D-1 o D-2 no siguen la propuesta, ajusta los bloques de `PLAN.md` de las tareas afectadas **antes** de que las tome un agente.
3. Haz un commit con los cambios del plan: `git commit -m "PLAN: respuesta a D-x"`.
4. Los agentes verán la respuesta la próxima vez que lean el paso 1.

### Tareas MANUALES

Las hace el usuario, y la sesión maestra registra el avance en `plan/estado/Manual.md` cuando él lo reporta.

### Integrar investigación

Cuando el Researcher entrega un `plan/investigacion/RES-0x.md`, la sesión maestra lo revisa con el criterio del Scavenge (lo no verificado o inferido es vacío) y agrega una referencia en la D-x que corresponde. No reescribe el texto del Researcher.
