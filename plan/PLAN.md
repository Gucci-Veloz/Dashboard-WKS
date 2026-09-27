# Plan · Dashboard de Vania + Works

Etapa: 03 · Mapping. Fecha: 2026-09-23. Estado: **aprobado el 2026-09-23**. D-1, D-2 y D-3 resueltas (ver `DECISIONES.md`, "Respuestas"). Las demás D-x siguen abiertas.

Fuente de verdad del producto: `handshake_vania_dashboard.md`. Hechos y vacíos: `SCAVENGE-Vania-Dashboard.md`. Decisiones pendientes: `plan/DECISIONES.md`. Protocolo de trabajo: `plan/REANUDAR.md`.

## Resumen

- **11 fases (0 a 10) y 70 tareas**: 16 de Builder_Datos, 17 de Builder_UI, 16 de Builder_Integraciones, 8 del Verificador, 4 del Researcher y 9 MANUALES que hace el usuario.
- **Libres desde el primer día:** UI-02, DAT-03, RES-01, RES-02, RES-03 y RES-04.
- **D-1 y D-2 (stack) son las primeras decisiones que hay que resolver**: casi todo lo demás depende de ellas.
- El Excel de Works no existe todavía. Hasta la fase 9 se trabaja **solo con datos sintéticos marcados**. La fase 9 espera el Excel.

## Reglas que aplican a todas las tareas

1. **No se reabre el handshake.** Si una tarea descubre una mejora, se anota en el archivo de estado del agente como "observación". No se convierte en requisito ni se construye.
2. **FastAPI es la única capa que toca SQLite.** Solo `app/db/` abre la base. Ningún archivo de `web/`, ni Hermes, ni un script, la lee directamente.
3. **Datos sintéticos marcados.** Todo registro sintético lleva `origen_dato = 'sintetico'`, y los nombres lo dicen ("Titular Sintético 07"). El Dashboard muestra un aviso discreto de "Datos sintéticos" cuando corresponde. No se usa el Google Sheet preliminar. No se inventan datos que parezcan reales.
4. **No hay datos reales en git.** `datos_reales/` y `var/` están en `.gitignore` desde DAT-01. El Excel nunca se sube al repositorio.
5. **No hay datos reales sin acceso restringido.** Ninguna tarea que cargue datos reales (fase 9) puede empezar antes de que INT-13 esté hecha.
6. **Nadie toca el VPS.** Lo que requiere servidor es MANUAL, y lo hace el usuario.
7. **No se supone cómo está hecho Hermes** ni su integración con la HP. Lo que corre dentro de Hermes es MANUAL.
8. **Vania no contacta inquilinos.** Ningún endpoint ni plantilla envía nada a terceros.
9. **Nivel 1 sin KPI.** La conclusión humana tiene la mayor jerarquía. Nada de `%`, `$` ni gráficas en el nivel 1. No se fabrica actividad.
10. **Mismo orden para todos.** El orden de asuntos es determinista y no depende de quién abre la pantalla.
11. **Textos visibles en español de México**, en frases como las diría una persona ("La oficina 204 vence en 12 días"), no en formato de campo ("Fecha fin: 02/10/2026"). El texto exacto sigue abierto: toda la redacción vive en un solo lugar para poder cambiarla.
12. **Git:** commits locales, sin push. Un commit por tarea, con el ID de la tarea al inicio del mensaje. Solo se agregan los archivos de la tarea más el archivo de estado propio: nunca `git add -A` ni `git add .`. El commit siempre nombra sus rutas: `git commit -m "<ID>: …" -- <rutas>`, para no arrastrar archivos que otro agente tenga preparados. Detalles en `REANUDAR.md`.

## Convenciones

- **Estados de una tarea:** `pendiente`, `en curso`, `bloqueada (motivo)`, `hecha (commit)`.
- **"Espera"** indica de qué depende la tarea: otras tareas, decisiones D-x, vacíos U-x del usuario o el Excel.
- **Comandos de prueba.** Suponen la propuesta del planificador en D-1 (HTML/JS sin build + Playwright desde pytest) y D-2 (`sqlite3` + migraciones `.sql` + `pytest`). Si el usuario elige otra opción, la sesión maestra ajusta rutas y comandos de las tareas afectadas **antes** de liberarlas.
- **Evidencia visual:** capturas en `evidencia/<ID>/`, viewport de teléfono 390×844 y de escritorio 1280×800.
- **Migraciones:** cada tarea que cambia el esquema crea **su propio archivo nuevo** con el número ya asignado y nunca edita uno existente. Asignación: `000` base (DAT-02), `001` áreas (DAT-04), `002` actividad (INT-01), `003` preferencias de avisos (INT-07), `004` personas (DAT-13), `005` cuentas y sesiones (INT-13), `006` roles (INT-15), `007` contextos (INT-08, solo si D-9 lo requiere).

## Estructura de carpetas propuesta

Supone la propuesta del planificador en D-1 y D-2.

```text
app/                    servicio FastAPI
  main.py               arranque; registra routers solos (DAT-01) y nadie más lo toca
  api/                  un archivo por router
  db/                   única capa que abre SQLite; migraciones/
  fuentes/              de dónde vienen los datos: base, sintetica, excel
  estado/               lógica del estado de atención (según D-3)
  actividad/            rastro de Vania
  seguridad/            quién llama: Vania (servicio) o una persona (según D-4)
  documentos/           documentos imprimibles
contratos/              contrato JSON del estado de atención y sus ejemplos
datos_sinteticos/       explicación de los escenarios sintéticos
docs/                   contrato para Vania, mapeo del Excel
web/                    Dashboard (HTML, CSS, JS)
scripts/                utilidades (contraste)
tests/  tests/ui/       pruebas
evidencia/              capturas de las pruebas de UI
```

## Propiedad de archivos y trabajo en paralelo

Cada agente trabaja **una tarea a la vez**. Dos agentes distintos pueden trabajar al mismo tiempo porque sus carpetas no se cruzan:

| Agente | Escribe en | Solo lee |
|---|---|---|
| Builder_Datos | `pyproject.toml` y dependencias, `.gitignore`, `app/main.py`, `app/api/__init__.py`, `app/api/{salud,estado,oficinas,inquilinos,contratos,pagos,personas}.py`, `app/db/**` (migraciones 000, 001, 004), `app/fuentes/**` excepto `actividad_sintetica.py`, `app/estado/**`, `contratos/**`, `datos_sinteticos/**`, `docs/mapeo-excel.md`, `tests/conftest.py`, `tests/test_dat*.py` | `app/actividad/`, `app/seguridad/` |
| Builder_Integraciones | `app/actividad/**`, `app/seguridad/**`, `app/documentos/**`, `app/api/{actividad,avisos,contexto,documentos}.py`, `app/fuentes/actividad_sintetica.py`, migraciones 002, 003, 005, 006, 007, `web/acceso/**`, `web/componentes/continuar-con-vania.js`, `docs/contrato-vania.md`, `tests/test_int*.py`, `tests/ui/test_int*.py` | todo lo demás |
| Builder_UI | `web/**` excepto `web/acceso/**` y `web/componentes/continuar-con-vania.js`, `scripts/**`, `tests/ui/**` excepto `test_int*`, `evidencia/**` | `contratos/`, `app/` |
| Verificador | `plan/verificacion/**` | todo |
| Researcher | `plan/investigacion/**` | todo |
| Sesión maestra | `plan/PLAN.md`, `plan/DECISIONES.md`, `plan/REANUDAR.md`, `plan/estado/Manual.md` | todo |

Además, cada agente escribe **solo** en su `plan/estado/<Agente>.md`.

**Archivos compartidos que nunca se tocan al mismo tiempo**
- `pyproject.toml` (dependencias): DAT-01, INT-09 y DAT-15. Si una está `en curso`, las otras dos esperan. DAT-01 debe instalar desde el inicio todas las dependencias de prueba que fijen D-1 y D-2, Playwright incluido, para que nadie más necesite tocarlo.
- `app/main.py`: solo DAT-01. Los routers nuevos se agregan como archivos en `app/api/` y se registran solos.
- `web/navegacion/rutas.js`: solo UI-08. Las pantallas de detalle se registran por convención (`web/detalle/<area>.js`).

**Paralelo posible el primer día**, sin cruces: UI-02 (Builder_UI), DAT-03 (Builder_Datos), RES-01 a RES-04 (Researcher, en orden).

---

## Fase 0 · Cimientos

Objetivo: el servicio arranca, la base se migra, existe la página base y los tokens de diseño cumplen contraste.

### DAT-01 · Esqueleto del servicio FastAPI
- **Dueño:** Builder_Datos
- **Espera:** D-2
- **Archivos:** `pyproject.toml` (o equivalente según D-2), `.gitignore`, `app/__init__.py`, `app/main.py`, `app/api/__init__.py`, `app/api/salud.py`, `tests/conftest.py`, `tests/test_dat01_salud.py`
- **Entregable:** servicio que arranca en local. Expone `GET /api/salud` → `{"ok": true}`. Registra automáticamente cualquier router que exista en `app/api/*.py`, sin tocar `main.py`. Sirve `web/` como archivos estáticos en `/`. Instala las dependencias de prueba de D-1 y D-2. `.gitignore` incluye `var/`, `datos_reales/`, entornos virtuales y cachés.
- **Prueba:** `pytest tests/test_dat01_salud.py -q`. Incluye una prueba que crea un router temporal en `app/api/` y comprueba que responde sin modificar `main.py`.
- **Hecha cuando:** la prueba pasa y `git check-ignore var/x datos_reales/x` reconoce las dos rutas.
- **Commit:** `DAT-01: esqueleto FastAPI con registro automático de routers`

### DAT-02 · Conexión a SQLite y migraciones numeradas
- **Dueño:** Builder_Datos
- **Espera:** DAT-01
- **Archivos:** `app/db/__init__.py`, `app/db/conexion.py`, `app/db/migrar.py`, `app/db/migraciones/000_base.sql`, `tests/test_dat02_migraciones.py`
- **Entregable:** un único punto de conexión. La ruta de la base viene de la variable `WORKS_DB`, con `var/works.db` por defecto. Las migraciones se aplican en orden numérico y una sola vez, registradas en una tabla de control. Comando: `python -m app.db.migrar`.
- **Prueba:** `pytest tests/test_dat02_migraciones.py -q`: base temporal, migrar dos veces seguidas sin error y sin duplicar registros de control.
- **Hecha cuando:** la prueba pasa y `grep -rn "sqlite3" app --include=*.py | grep -v "^app/db/"` no devuelve nada.
- **Commit:** `DAT-02: conexión SQLite y migraciones numeradas`

### UI-01 · Página base mobile-first
- **Dueño:** Builder_UI
- **Espera:** D-1, DAT-01, UI-02
- **Archivos:** `web/index.html`, `web/app.js`, `web/estilos/base.css`, `tests/ui/conftest.py`, `tests/ui/test_ui01_base.py`
- **Entregable:** documento base con `lang="es-MX"` y viewport móvil. Carga `tokens.css` y `base.css`, con un contenedor principal vacío. `tests/ui/conftest.py` aporta los fixtures de Playwright (viewports 390×844 y 1280×800) y levanta el servicio para las pruebas.
- **Prueba:** `pytest tests/ui/test_ui01_base.py`: carga `/` sin errores de consola en ambos viewports y sin scroll horizontal a 390 px.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `UI-01: página base mobile-first`

### UI-02 · Tokens de diseño y verificador de contraste
- **Dueño:** Builder_UI
- **Espera:** — (libre)
- **Archivos:** `web/estilos/tokens.css`, `scripts/contraste.py`, `scripts/fixtures/par_malo.css`
- **Entregable:**
  - Variables CSS con la paleta del handshake (perla, blanco, crema, gris claro) para fondos y superficies.
  - Texto principal y secundario.
  - **Un acento de mayor contraste** para lo importante y para los cambios de estado. El acento propuesto se documenta en el encabezado del archivo para que el usuario lo vea en VER-01.
  - Sombras clara y oscura para relieve y hundido, borde sutil de 1 px (R3, H9), radios, espaciado y escala tipográfica.
  - Cada par que deba cumplir contraste se declara en un comentario con este formato: `/* par: --texto-principal sobre --superficie 4.5 */`.
  - `scripts/contraste.py` usa solo la biblioteca estándar. Lee esos pares, calcula el ratio WCAG, imprime una tabla y termina con código 1 si alguno falla.
  - Umbrales (R3): texto normal 4.5:1, texto grande 3:1, y límites y estados de componentes 3:1 contra el color adyacente.
- **Prueba:** `python3 scripts/contraste.py web/estilos/tokens.css` termina con código 0 y todos los pares en "PASA". `python3 scripts/contraste.py scripts/fixtures/par_malo.css` termina con código 1.
- **Hecha cuando:** las dos pruebas se comportan así y hay al menos un par de texto, uno de texto grande y uno de límite de componente.
- **Commit:** `UI-02: tokens de diseño y verificador de contraste`

### UI-03 · Componentes neumórficos base
- **Dueño:** Builder_UI
- **Espera:** D-1, UI-01
- **Archivos:** `web/estilos/componentes.css`, `web/muestras/componentes.html`, `tests/ui/test_ui03_componentes.py`, `evidencia/UI-03/`
- **Entregable:**
  - Superficie, tarjeta, botón, campo de texto, enlace discreto e indicador de foco.
  - El botón sobresale en reposo y se hunde al presionarlo. Además, el estado presionado cambia el borde o usa el acento: no depende solo de la sombra (R3, H7 y H12).
  - El texto importante va sobre una superficie de mayor contraste (R3, H11).
  - El foco es visible y no queda tapado (R3, H4 y H5).
- **Prueba:** `pytest tests/ui/test_ui03_componentes.py`: la muestra carga; al presionar el botón cambia un valor computado distinto de `box-shadow` (borde o color); el foco tiene `outline` distinto de `none`; se guardan capturas a 390 px. Además, `python3 scripts/contraste.py web/estilos/tokens.css` sigue terminando en 0.
- **Hecha cuando:** las pruebas pasan y las capturas existen.
- **Commit:** `UI-03: componentes neumórficos base`

### VER-01 · Verificación de la fase 0
- **Dueño:** Verificador
- **Espera:** DAT-01, DAT-02, UI-01, UI-02, UI-03
- **Archivos:** `plan/verificacion/VER-01.md`
- **Entregable:**
  - Reporte con el resultado de volver a correr la prueba de cada tarea: comando, salida resumida y PASA o FALLA.
  - Lista de revisión contra el handshake: paleta perla, blanco, crema y gris claro; neumorphism no dogmático, con acento y bordes; mobile-first.
  - Rutas de las capturas para que el usuario las mire.
  - El acento propuesto en UI-02, señalado para visto bueno del usuario.
- **Prueba:** el reporte existe y cada tarea de la fase tiene PASA o FALLA con la salida de su comando.
- **Hecha cuando:** el reporte está completo. Si algo falla, el reporte nombra la tarea y el síntoma. El Verificador no lo arregla.
- **Commit:** `VER-01: verificación de la fase 0`

---

## Fase 1 · Estado de atención y niveles 1 y 2

Objetivo: la pantalla de nivel 1, la pieza que `siguientes_pasos.md` recomienda empezar primero, vive con datos sintéticos y después con el estado real calculado por el servicio.

### DAT-03 · Contrato del estado de atención
- **Dueño:** Builder_Datos
- **Espera:** — (libre)
- **Archivos:** `contratos/estado.schema.json`, `contratos/ejemplos/estado-tranquilo.json`, `contratos/ejemplos/estado-atencion.json`, `contratos/LEEME.md`
- **Entregable:** JSON Schema de la respuesta del estado de Works, que consumirán el Dashboard y Vania:
  - `conclusion`: `tipo` (`tranquilo` o `atencion`), `frase` y `cantidad`.
  - `asuntos[]`: `id`, `area`, `frase` humana, `por_que_importa`, `referencia` (tipo e id del registro) y `orden`.
  - `indicadores[]`: `area` y `frase_corta`. Ninguno se marca como principal.
  - `origen_datos` (`sintetico` o `real`) y `generado_en`.

  Incluye dos ejemplos con `"origen_datos": "sintetico"`. En `LEEME.md` se aclara que las frases son provisionales, porque el texto exacto sigue abierto.
- **Prueba:** `python3 -c "import json,sys; [json.load(open(f)) for f in sys.argv[1:]]" contratos/estado.schema.json contratos/ejemplos/*.json` sin error. `grep -L '"origen_datos": "sintetico"' contratos/ejemplos/*.json` no devuelve nada. `grep -E '[0-9]{2}/[0-9]{2}/[0-9]{4}' contratos/ejemplos/*.json` no devuelve nada, es decir, no hay fechas crudas en las frases.
- **Hecha cuando:** las tres comprobaciones pasan y el ejemplo tranquilo tiene `asuntos: []`.
- **Commit:** `DAT-03: contrato del estado de atención con ejemplos sintéticos`

### DAT-04 · Esquema de las cuatro áreas
- **Dueño:** Builder_Datos
- **Espera:** DAT-02
- **Archivos:** `app/db/migraciones/001_areas.sql`, `tests/test_dat04_esquema.py`
- **Entregable:** tablas con los campos del handshake:
  - `oficinas`: tipo, número, piso, m², estatus.
  - `inquilinos`: titular, contacto.
  - `contratos`: oficina, inquilino, inicio, fin, alerta de renovación.
  - `pagos`: contrato, precio, depósito en garantía, fecha de pago, forma de pago, estatus de pago.

  Todas llevan `origen_dato` obligatorio (`sintetico`, `excel` o `manual`), `extras` (JSON en texto, para columnas del Excel que no estén previstas; así se conectan los datos reales sin rehacer el esquema), `creado_en` y `actualizado_en`. En la cabecera del archivo, un comentario aclara que los campos son provisionales hasta conocer el Excel (P1).
- **Prueba:** `pytest tests/test_dat04_esquema.py -q`: migra una base temporal, las columnas existen, e insertar sin `origen_dato` o con un valor fuera de la lista falla.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `DAT-04: esquema de oficinas, inquilinos, contratos y pagos`

### INT-01 · Tabla de actividad y función para registrarla
- **Dueño:** Builder_Integraciones
- **Espera:** DAT-02
- **Archivos:** `app/db/migraciones/002_actividad.sql`, `app/actividad/__init__.py`, `app/actividad/registrar.py`, `tests/test_int01_actividad.py`
- **Entregable:** tabla `actividad` con estos campos:
  - `momento`.
  - `actor`: `vania`, `dashboard` o `sistema`.
  - `persona`, que puede quedar vacía hasta D-4.
  - `tipo`: `solicitada` (confirma algo que alguien pidió), `detectada` (Vania lo encontró sin que nadie preguntara) o `automatica`. Así se conserva la distinción del handshake entre confirmar y avisar por iniciativa propia.
  - `accion`, `area`, `referencia`, `resumen` en frase humana y `origen_dato`.

  La función `registrar(...)` la usan todas las escrituras y solo escribe a través de `app/db`.
- **Prueba:** `pytest tests/test_int01_actividad.py -q`: registrar y leer; un `actor` o `tipo` inválido falla.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `INT-01: tabla de actividad y función de registro`

### INT-04 · Credencial de servicio para Vania e identificación de quién llama
- **Dueño:** Builder_Integraciones
- **Espera:** DAT-01
- **Archivos:** `app/seguridad/__init__.py`, `app/seguridad/actor.py`, `tests/test_int04_actor.py`
- **Entregable:** una dependencia de FastAPI, `actor_actual()`:
  - Devuelve `vania` si la petición trae la credencial de servicio correcta. La credencial viene de la variable `WORKS_TOKEN_VANIA`; si no está definida, el acceso de servicio queda apagado.
  - En cualquier otro caso devuelve `dashboard`, con la persona vacía.
  - Es el único lugar que INT-13 cambiará para exigir sesión humana.
- **Prueba:** `pytest tests/test_int04_actor.py -q`: sin credencial → `dashboard`; credencial válida → `vania`; credencial inválida → 401; sin variable definida, una credencial → 401.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `INT-04: credencial de servicio de Vania y actor_actual`

### DAT-05 · Interfaz de fuentes de datos y cargador
- **Dueño:** Builder_Datos
- **Espera:** DAT-04
- **Archivos:** `app/fuentes/__init__.py`, `app/fuentes/base.py`, `app/fuentes/excel.py`, `app/fuentes/cargar.py`, `tests/test_dat05_fuentes.py`
- **Entregable:**
  - Contrato `FuenteDatos`: entrega los registros de las cuatro áreas ya normalizados al esquema.
  - Cargador `python -m app.fuentes.cargar --fuente <nombre> [--escenario <nombre>]`, que vacía y carga dentro de una transacción.
  - `excel.py` existe, pero falla con el mensaje "fuente no disponible: el Excel de Works todavía no se entrega".
  - Nada lee el Google Sheet preliminar.
- **Prueba:** `pytest tests/test_dat05_fuentes.py -q`: una fuente falsa definida en la prueba se carga; la fuente `excel` falla con ese mensaje; una carga que falla a medias no deja datos parciales.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `DAT-05: interfaz de fuentes de datos y cargador`

### DAT-06 · Fuente sintética con dos escenarios
- **Dueño:** Builder_Datos
- **Espera:** DAT-05, DAT-03
- **Archivos:** `app/fuentes/sintetica.py`, `datos_sinteticos/LEEME.md`, `tests/test_dat06_sintetica.py`
- **Entregable:** generador determinista con semilla fija y alrededor de 21 titulares. La fecha de "hoy" se puede fijar para las pruebas. Dos escenarios:
  - `tranquilo`: nada requiere atención.
  - `con_atencion`: reproduce los asuntos de `contratos/ejemplos/estado-atencion.json`.

  Todo lleva `origen_dato='sintetico'` y los nombres llevan "Sintético". `LEEME.md` explica que son datos inventados para desarrollo y que no se parecen a los de Works a propósito.
- **Prueba:** `pytest tests/test_dat06_sintetica.py -q`: 0 registros con otro origen; los conteos esperados; todos los nombres de titular contienen "Sintético"; dos corridas dan exactamente los mismos datos.
- **Hecha cuando:** la prueba pasa y `python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion` carga sin error en una base local.
- **Commit:** `DAT-06: fuente sintética con escenarios tranquilo y con_atencion`

### DAT-07 · Motor del estado de atención
- **Dueño:** Builder_Datos
- **Espera:** **D-3**, DAT-06
- **Archivos** (según la propuesta A de D-3): `app/estado/__init__.py`, `app/estado/reglas.py`, `app/estado/redaccion.py`, `app/estado/umbrales.toml`, `tests/test_dat07_estado.py`
- **Entregable:** una función pura que recibe los datos y devuelve un estado conforme a `contratos/estado.schema.json`.
  - Primer conjunto de reglas, tomado del handshake: contrato que se acerca a revisión o renovación, pago pendiente del mes y dato incompleto o contradictorio.
  - Los umbrales van en `umbrales.toml`, marcados como "provisionales hasta ver datos reales".
  - Toda la redacción vive en `redaccion.py`.
  - El orden es determinista.
  - Ninguna regla produce asuntos si no hay un hecho que los sostenga.
- **Prueba:** `pytest tests/test_dat07_estado.py -q`, con la fecha fija:
  - `tranquilo` → `tipo = tranquilo` y 0 asuntos.
  - `con_atencion` → los asuntos del ejemplo, en el mismo orden en dos corridas.
  - Ninguna frase contiene una fecha con formato `dd/mm/aaaa`.
  - La salida valida contra el esquema.
- **Hecha cuando:** la prueba pasa y `grep -rn "sqlite3\|fastapi" app/estado` no devuelve nada, porque el módulo es puro.
- **Commit:** `DAT-07: motor del estado de atención`

### DAT-08 · Endpoint del estado
- **Dueño:** Builder_Datos
- **Espera:** **D-3**, DAT-07
- **Archivos:** `app/api/estado.py`, `tests/test_dat08_api_estado.py`
- **Entregable:** `GET /api/estado`. Lee a través de `app/db`, invoca `app/estado` y responde conforme al contrato. `origen_datos` refleja lo que hay cargado.
- **Prueba:** `pytest tests/test_dat08_api_estado.py -q`: con cada escenario cargado, la respuesta valida contra el esquema y coincide con el motor.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `DAT-08: endpoint GET /api/estado`

### UI-04 · Nivel 1: estado general con los ejemplos del contrato
- **Dueño:** Builder_UI
- **Espera:** UI-03, DAT-03
- **Archivos:** `web/nivel1/nivel1.js`, `web/nivel1/nivel1.css`, `web/datos/estado.js`, `web/muestras/nivel1.html`, `tests/ui/test_ui04_nivel1.py`, `evidencia/UI-04/`
- **Entregable:**
  - La conclusión humana es lo primero que se ve y lo de mayor jerarquía.
  - En estado tranquilo transmite calma y no rellena la pantalla. En estado de atención dice cuántas cosas hay.
  - Aviso discreto de "Datos sintéticos" cuando `origen_datos = sintetico`.
  - Toda la lectura de datos pasa por `obtenerEstado()` en `web/datos/estado.js`, que por ahora lee un ejemplo del contrato. Es lo único que cambiará en UI-07.
- **Prueba:** `pytest tests/ui/test_ui04_nivel1.py`, con cada ejemplo:
  - El elemento de la conclusión tiene el `font-size` computado más grande de la página.
  - En estado tranquilo no se muestra ninguna lista.
  - Ningún texto visible del nivel 1 contiene `%` ni `$`.
  - El aviso de datos sintéticos está presente.
  - Se guardan capturas a 390 px.
- **Hecha cuando:** la prueba pasa en ambos viewports.
- **Commit:** `UI-04: nivel 1 con conclusión humana`

### UI-05 · Nivel 2: lo que merece atención
- **Dueño:** Builder_UI
- **Espera:** UI-04
- **Archivos:** `web/nivel2/nivel2.js`, `web/nivel2/nivel2.css`, `web/muestras/nivel1.html`, `tests/ui/test_ui05_nivel2.py`, `evidencia/UI-05/`
- **Entregable:** los asuntos en frases humanas, cada uno con su "por qué importa", en el orden del contrato. Cada elemento se puede tocar; su destino es provisional hasta UI-08. En estado tranquilo no se muestra nada de este nivel.
- **Prueba:** `pytest tests/ui/test_ui05_nivel2.py`: el orden en pantalla coincide con `orden` del ejemplo; en estado tranquilo no se renderiza ningún asunto; ninguna frase visible tiene formato de fecha `dd/mm/aaaa`.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `UI-05: nivel 2 con asuntos en lenguaje humano`

### UI-06 · Indicadores que explican el estado
- **Dueño:** Builder_UI
- **Espera:** UI-05
- **Archivos:** `web/indicadores/indicadores.js`, `web/indicadores/indicadores.css`, `web/muestras/nivel1.html`, `tests/ui/test_ui06_indicadores.py`, `evidencia/UI-06/`
- **Entregable:** frases cortas por área (por ejemplo, "Pagos · al día"), debajo de los asuntos y con menor jerarquía que la conclusión. Ninguna se destaca como número principal.
- **Prueba:** `pytest tests/ui/test_ui06_indicadores.py`: el `font-size` de cada indicador es menor que el de la conclusión; todos los indicadores tienen el mismo estilo, así que ninguno domina.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `UI-06: indicadores textuales sin KPI dominante`

### UI-07 · Conectar niveles 1 y 2 al servicio
- **Dueño:** Builder_UI
- **Espera:** DAT-08 (por lo tanto **D-3**), UI-06
- **Archivos:** `web/datos/estado.js`, `web/index.html`, `tests/ui/test_ui07_api.py`
- **Entregable:** `obtenerEstado()` lee `GET /api/estado`, y `index.html` muestra los niveles 1 y 2 con los indicadores. Si la carga falla, aparece un mensaje en palabras normales, no una pantalla técnica.
- **Prueba:** `pytest tests/ui/test_ui07_api.py`: con `con_atencion` cargado, la pantalla muestra los mismos asuntos que `/api/estado` y en el mismo orden; con el servicio caído, aparece el mensaje humano.
- **Hecha cuando:** la prueba pasa.
- **Commit:** `UI-07: niveles 1 y 2 conectados a /api/estado`

### VER-02 · Verificación de la fase 1
- **Dueño:** Verificador
- **Espera:** todas las tareas de la fase 1 hechas o bloqueadas
- **Archivos:** `plan/verificacion/VER-02.md`
- **Entregable:** vuelve a correr las pruebas de la fase. Revisión contra el handshake, con comandos concretos:
  - No hay KPI dominante ni `%` o `$` en el nivel 1.
  - En estado tranquilo no hay actividad artificial.
  - El mismo orden sale en dos corridas.
  - Todo es sintético: `sqlite3 var/works.db "select count(*) from oficinas where origen_dato<>'sintetico'"` devuelve 0, y lo mismo para las otras tres tablas.
  - Solo `app/db` abre SQLite: `grep -rn "sqlite3" app --include=*.py | grep -v "^app/db/"` no devuelve nada.

  Anota las tareas que quedaron bloqueadas, con su D-x.
- **Prueba:** el reporte existe con PASA o FALLA por tarea y por punto de la revisión.
- **Hecha cuando:** el reporte está completo.
- **Commit:** `VER-02: verificación de la fase 1`

---

## Fase 2 · Detalle y edición (nivel 3)

Objetivo: el Dashboard no es de solo lectura. Se puede ver, crear, editar y eliminar en las cuatro áreas, y cada cambio deja rastro. Por defecto todo se puede gestionar: el handshake deja las restricciones por campo para cuando se conozcan los datos reales.

### DAT-09 · API de oficinas
- **Dueño:** Builder_Datos
- **Espera:** DAT-04, INT-01, INT-04
- **Archivos:** `app/api/oficinas.py`, `tests/test_dat09_oficinas.py`
- **Entregable:** listar, ver, crear, editar y eliminar oficinas.
  - Cada escritura llama a `registrar(...)` de `app/actividad`, con el actor de `actor_actual()` y `tipo='solicitada'`.
  - Lo que se crea desde la API lleva `origen_dato='manual'`.
  - Los errores de validación vienen en frases normales.
- **Prueba:** `pytest tests/test_dat09_oficinas.py -q`: el ciclo completo; cada escritura deja una fila en `actividad` con el actor correcto (`dashboard` sin credencial, `vania` con credencial).
- **Hecha cuando:** la prueba pasa.
- **Commit:** `DAT-09: API de oficinas con rastro de actividad`

### DAT-10 · API de inquilinos
- **Dueño:** Builder_Datos · **Espera:** DAT-09 · **Archivos:** `app/api/inquilinos.py`, `tests/test_dat10_inquilinos.py`
- **Entregable, prueba y hecha cuando:** igual que DAT-09, aplicado a inquilinos.
- **Commit:** `DAT-10: API de inquilinos con rastro de actividad`

### DAT-11 · API de contratos
- **Dueño:** Builder_Datos · **Espera:** DAT-10 · **Archivos:** `app/api/contratos.py`, `tests/test_dat11_contratos.py`
- **Entregable:** igual que DAT-09, aplicado a contratos. Además, valida que la oficina y el inquilino existan.
- **Prueba:** como DAT-09, más la creación de un contrato con una oficina inexistente, que debe fallar con un mensaje humano.
- **Commit:** `DAT-11: API de contratos con rastro de actividad`

### DAT-12 · API de pagos y "registrar pago"
- **Dueño:** Builder_Datos · **Espera:** DAT-11 · **Archivos:** `app/api/pagos.py`, `tests/test_dat12_pagos.py`
- **Entregable:** el CRUD de pagos más una operación explícita de "registrar pago" (contrato, periodo, forma de pago). Es la que usarán tanto el Dashboard como Vania ("Vania, registra que la oficina 204 pagó septiembre por transferencia"). El resumen de actividad queda en frase humana.
- **Prueba:** `pytest tests/test_dat12_pagos.py -q`: registrar un pago cambia su estatus y deja actividad. Si DAT-08 ya está hecha, la prueba también comprueba que `/api/estado` tiene un asunto menos después de registrar un pago pendiente. Si no lo está, esa parte queda marcada como `skip`, con el motivo.
- **Commit:** `DAT-12: API de pagos y registrar pago`

### UI-08 · Entrada al detalle sin que se le eche encima al usuario
- **Dueño:** Builder_UI
- **Espera:** UI-05
- **Archivos:** `web/navegacion/rutas.js`, `web/navegacion/navegacion.css`, `tests/ui/test_ui08_navegacion.py`
- **Entregable:** navegación por hash. Se entra al nivel 3 con un enlace discreto ("ver todo") y tocando un asunto, que lleva a su registro. Siempre hay un "volver". Las pantallas de detalle se registran por convención (`web/detalle/<area>.js`), sin editar `rutas.js`. El nivel 3 nunca aparece al abrir la aplicación.
- **Prueba:** `pytest tests/ui/test_ui08_navegacion.py`: al cargar `/` no hay tablas ni listas de detalle visibles; tocar un asunto cambia la ruta a su registro; "volver" regresa al nivel 1.
- **Commit:** `UI-08: navegación al detalle bajo demanda`

### UI-09 · Formulario editable y confirmación visible
- **Dueño:** Builder_UI
- **Espera:** UI-03
- **Archivos:** `web/componentes/formulario.js`, `web/componentes/confirmacion.js`, `web/estilos/formulario.css`, `web/muestras/formulario.html`, `tests/ui/test_ui09_formulario.py`, `evidencia/UI-09/`
- **Entregable:** componente de edición y guardado. Al guardar, muestra una confirmación clara y el dato actualizado a la vista, para dar la sensación de "control, certeza y avance" que pide el handshake. Si hay un error, lo dice en palabras normales y conserva lo que la persona escribió.
- **Prueba:** `pytest tests/ui/test_ui09_formulario.py`, contra un servicio simulado dentro de la prueba: guardar con éxito muestra la confirmación; un error muestra el mensaje y los campos conservan su valor.
- **Commit:** `UI-09: formulario y confirmación de guardado`

### UI-10 · Detalle de oficinas
- **Dueño:** Builder_UI · **Espera:** DAT-09, UI-08, UI-09
- **Archivos:** `web/detalle/oficinas.js`, `tests/ui/test_ui10_oficinas.py`, `evidencia/UI-10/`
- **Entregable:** lista de oficinas y ficha editable con el componente de UI-09, contra la API real.
- **Prueba:** `pytest tests/ui/test_ui10_oficinas.py`: editar un campo, guardar, recargar y ver el valor nuevo; aparece una fila nueva en `actividad` con actor `dashboard`.
- **Commit:** `UI-10: detalle editable de oficinas`

### UI-11 · Detalle de inquilinos
- **Dueño:** Builder_UI · **Espera:** DAT-10, UI-10 · **Archivos:** `web/detalle/inquilinos.js`, `tests/ui/test_ui11_inquilinos.py`, `evidencia/UI-11/`
- **Entregable y prueba:** igual que UI-10, aplicado a inquilinos. **Commit:** `UI-11: detalle editable de inquilinos`

### UI-12 · Detalle de contratos
- **Dueño:** Builder_UI · **Espera:** DAT-11, UI-11 · **Archivos:** `web/detalle/contratos.js`, `tests/ui/test_ui12_contratos.py`, `evidencia/UI-12/`
- **Entregable y prueba:** igual que UI-10, aplicado a contratos. Las fechas se muestran también en forma humana ("vence en 12 días"). **Commit:** `UI-12: detalle editable de contratos`

### UI-13 · Detalle de pagos y registrar pago
- **Dueño:** Builder_UI · **Espera:** DAT-12, UI-12 · **Archivos:** `web/detalle/pagos.js`, `tests/ui/test_ui13_pagos.py`, `evidencia/UI-13/`
- **Entregable:** lista y ficha de pagos, más la acción "registrar pago". Desde un asunto de pago pendiente del nivel 2 se llega directo a esa acción.
- **Prueba:** `pytest tests/ui/test_ui13_pagos.py`: desde el asunto de pago pendiente se registra el pago; al volver al nivel 1 ese asunto ya no aparece (requiere UI-07; si no está hecha, esa parte queda `skip` con el motivo).
- **Commit:** `UI-13: detalle de pagos y registrar pago`

### VER-03 · Verificación de la fase 2
- **Dueño:** Verificador · **Espera:** todas las tareas de la fase 2 hechas o bloqueadas · **Archivos:** `plan/verificacion/VER-03.md`
- **Entregable:** vuelve a correr las pruebas. Revisión:
  - Cada escritura deja actividad con el actor correcto.
  - El nivel 3 no aparece al abrir.
  - No hay chat dentro del Dashboard: `grep -rni "chat" web/` se revisa a mano.
  - Los registros creados desde la API llevan `origen_dato='manual'` y no se mezclan con los sintéticos sin marca.
- **Commit:** `VER-03: verificación de la fase 2`

---

## Fase 2b · Reglas de operación (2026-09-26)

Objetivo: aplicar `plan/REGLAS_OPERACION.md` sobre lo que ya está construido. **Léelo completo antes de tomar cualquier tarea de esta fase.** Reemplaza el guardado inmediato de las fases 2 (UI-09 a UI-13, DAT-09 a DAT-12) y el acceso libre de Vania para escribir (INT-04, INT-05).

**Arranque:** ninguna tarea de esta fase empieza sin el `/luz-verde` del usuario, que la sesión maestra anota en "Respuestas" de `DECISIONES.md`. **Filas de estado:** cada agente agrega a su tabla de `plan/estado/<Agente>.md` sus tareas nuevas de esta fase, en `pendiente`, antes de empezar la primera.

**Commits:** el aislamiento de Codex deja `.git` en solo lectura. Los agentes de Codex **no hacen commit**: al terminar una tarea la marcan `hecha (pendiente de commit)` y anotan en su bitácora la lista exacta de archivos. La sesión **Commit-Codex** corre la prueba, revisa que solo cambiaron esos archivos y hace el commit con el mensaje del plan. Cada vuelta de un agente es **una sola tarea**.

**Pruebas y aislamiento:** los agentes que corren en Codex ya tienen acceso a la red local (`network_access = true`). Si una prueba falla por algo del entorno y no del código, anótalo como "bloqueada (entorno: <detalle>)". No la marques como fallida ni la arregles.

### DAT-17 · Una sola forma de conectarse a la base (VER-02, opción B)
- **Dueño:** Builder_Datos · **Espera:** VER-03
- **Archivos:** `app/db/conexion.py`, `app/api/oficinas.py`, `app/api/inquilinos.py`, `app/api/contratos.py`, `app/api/pagos.py`, `app/api/estado.py` y, **con permiso explícito de esta tarea**, `app/api/actividad.py`, que es de Builder_Integraciones.
- **Entregable:** `conectar_con_filas()` vive en `app/db/conexion.py`. Los seis helpers locales desaparecen. `app/api/` ya no importa `sqlite3`. No cambia ningún comportamiento.
- **Prueba:** `grep -rn "sqlite3" app --include=*.py | grep -v "^app/db/"` no devuelve nada, y `.venv/bin/python -m pytest -q` (suite completa) pasa.
- **Commit:** `DAT-17: conexión con filas centralizada en app/db`

### DAT-18 · Cambios: pre-registro, confirmación e historial
- **Dueño:** Builder_Datos · **Espera:** DAT-17
- **Archivos:** `app/db/migraciones/008_cambios.sql`, `app/cambios/**`, `tests/test_dat18_cambios.py`
- **Entregable:** una sola tabla `cambios` que sirve a la vez de pre-registro, historial y fuente del reporte (KISS):
  - Columnas: `id`, `creado_en`, `vence_en` (creación + 24 h), `estado` (`pendiente`/`confirmado`), `area`, `registro_id`, `operacion` (`alta`/`modificacion`/`baja`), `valores_anteriores` y `valores_nuevos` (JSON), `observaciones` (opcional), `solicitante` (`david`/`grecia`), `ejecutor` (`david`/`grecia`/`vania`), `confirmado_en`.
  - Funciones:
    - `crear_pendiente()`.
    - `confirmar(id, persona)`: aplica el cambio al dato oficial dentro de una transacción. Si el cambio venció, falla con un mensaje humano.
    - `pendientes(area, registro_id)`.
    - `historial(area, registro_id)`.
    - `purgar_vencidos()`: la llaman las otras funciones, sin tareas programadas.
  - Todo `solicitante` es David o Grecia. Vania solo puede ser `ejecutor`.
- **Prueba:** `pytest tests/test_dat18_cambios.py -q`:
  - Un pendiente no cambia el dato oficial.
  - Al confirmarlo, el dato cambia y el historial guarda el valor anterior y el nuevo.
  - Un pendiente con más de 24 h no se confirma y desaparece.
  - Un cambio con `solicitante='vania'` se rechaza.
  - La baja confirmada borra el registro y deja historial.
- **Commit:** `DAT-18: cambios con pre-registro, confirmación e historial`

### DAT-19 · Las APIs de las cuatro áreas pasan por cambios
- **Dueño:** Builder_Datos · **Espera:** DAT-18, INT-13
- **Archivos:** `app/api/oficinas.py`, `app/api/inquilinos.py`, `app/api/contratos.py`, `app/api/pagos.py`, `app/api/cambios.py`, `tests/test_dat09_oficinas.py`, `tests/test_dat10_*.py`, `tests/test_dat11_*.py`, `tests/test_dat12_*.py`, `tests/test_dat19_api_cambios.py`
- **Entregable:**
  - `POST`, `PUT` y `DELETE` de las cuatro áreas, y "registrar pago", ya no escriben el dato oficial. Crean un pendiente y responden con su `id` y un resumen.
  - `POST /api/cambios/{id}/confirmar` lo aplica.
  - `GET /api/cambios?area=&registro_id=&estado=pendiente` lista los pendientes, para cualquier dispositivo.
  - Aceptan el campo opcional `observaciones`.
  - `solicitante` y `ejecutor` salen de `actor_actual()` (INT-13 e INT-17). Nunca vienen del cuerpo de la petición.
- **Prueba:** `pytest tests/test_dat19_api_cambios.py tests/test_dat09_oficinas.py tests/test_dat10_*.py tests/test_dat11_*.py tests/test_dat12_*.py -q`:
  - `PUT` sin confirmar deja el `GET` igual.
  - Al confirmar, el `GET` devuelve el valor nuevo.
  - El pendiente aparece en `GET /api/cambios`.
  - `/api/estado` pierde el asunto solo cuando se confirma el pago.
- **Commit:** `DAT-19: APIs de las áreas con pre-registro y confirmación`

### DAT-20 · Aviso de posibles duplicados
- **Dueño:** Builder_Datos · **Espera:** DAT-19
- **Archivos:** `app/cambios/duplicados.py`, `app/api/oficinas.py`, `app/api/inquilinos.py`, `app/api/contratos.py`, `app/api/pagos.py`, `tests/test_dat20_duplicados.py`
- **Entregable:**
  - Al crear, aplica **solo** los criterios de `REGLAS_OPERACION.md`, sin inventar otros.
  - Si hay coincidencia, responde `409` con `posible_duplicado: {area, id, resumen}` y el texto "Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?".
  - Con `crear_de_todos_modos: true` se crea el pendiente normal.
- **Prueba:** `pytest tests/test_dat20_duplicados.py -q`: un caso por criterio (coincide → 409; con la bandera → pendiente creado), y un caso sin coincidencia que no avisa.
- **Commit:** `DAT-20: aviso de posibles duplicados`

### DAT-21 · Reporte del día
- **Dueño:** Builder_Datos · **Espera:** DAT-19
- **Archivos:** `app/cambios/reporte.py`, `app/api/reporte.py`, `tests/test_dat21_reporte.py`
- **Entregable:**
  - `GET /api/reporte?fecha=AAAA-MM-DD`. Sin fecha, usa hoy en `America/Mexico_City`.
  - Una fila por cambio **confirmado** ese día, con: `id`, `fecha`, `inquilino` ("—" si no aplica), `concepto`, `observaciones`, `solicitante` y `ejecutor`. El `concepto` sigue la regla de `REGLAS_OPERACION.md`.
  - Se calcula a partir de `cambios`, sin guardar el reporte aparte. Así cualquier día pasado queda consultable.
- **Prueba:** `pytest tests/test_dat21_reporte.py -q`:
  - Los pendientes no aparecen.
  - Un cambio de las 23:30 de Querétaro cae en su día, no en el siguiente.
  - Un pago muestra su estatus como concepto.
  - Un cambio hecho por Vania muestra `solicitante=grecia, ejecutor=vania`.
- **Commit:** `DAT-21: reporte del día`

### DAT-22 · Descartar un cambio pendiente (agregada el 2026-09-26: la pide UI-18)
- **Dueño:** Builder_Datos · **Espera:** DAT-19
- **Archivos:** `app/cambios/servicio.py`, `app/api/cambios.py`, `tests/test_dat22_descartar.py`
- **Entregable:**
  - `descartar(cambio_id, persona)` en el servicio: borra el pendiente, igual que cuando vence. Si no existe o ya se confirmó, da error.
  - `POST /api/cambios/{cambio_id}/descartar`, con la misma validación de persona que `confirmar`. Deja una actividad, como `confirmar`.
- **Prueba:** `pytest tests/test_dat22_descartar.py -q`: un pendiente descartado ya no sale en la lista ni cambia el registro; descartar uno confirmado da 400.
- **Commit:** `DAT-22: descartar un cambio pendiente`

### INT-17 · Vania solo cambia datos con la sesión de quien lo pide
- **Dueño:** Builder_Integraciones · **Espera:** INT-13, DAT-19
- **Archivos:** `app/seguridad/actor.py`, `app/seguridad/vania.py`, `docs/contrato-vania.md`, `tests/test_int17_vania_sesion.py`
- **Entregable:**
  - Para escribir, Vania usa su credencial de servicio **y** el encabezado `X-Works-Solicitante: <número de WhatsApp>`. El número se resuelve a David o Grecia con la configuración del servidor.
  - Si esa persona no tiene una sesión vigente, la respuesta es `401` con `codigo: "sin_sesion"`. Vania entonces pide el link (INT-13).
  - Con sesión vigente, `actor_actual()` devuelve `solicitante=<persona>, ejecutor=vania`.
  - Las lecturas de Vania no cambian.
  - `docs/contrato-vania.md` explica el flujo completo: pedir link, crear pendiente, preguntar "¿Sí o No?", confirmar, observaciones y reporte.
- **Prueba:** `pytest tests/test_int17_vania_sesion.py -q`:
  - Vania escribe para Grecia sin sesión de Grecia → 401 `sin_sesion`.
  - Con sesión de David, pero la instrucción es de Grecia → 401.
  - Con sesión de Grecia → pendiente creado con `ejecutor=vania`.
  - Un número desconocido o el del desarrollador → 403.
- **Commit:** `INT-17: Vania escribe solo con la sesión del solicitante`

### UI-18 · Ventana de confirmación y cambios pendientes
- **Dueño:** Builder_UI · **Espera:** DAT-19, INT-14, DAT-22
- **Archivos:** `web/componentes/formulario.js`, `web/componentes/confirmacion.js`, `web/estilos/formulario.css`, `web/detalle/**`, `tests/ui/test_ui09_formulario.py`, `tests/ui/test_ui10_*.py` a `tests/ui/test_ui13_*.py`, `tests/ui/test_ui18_confirmar.py`, `evidencia/UI-18/`
- **Entregable:**
  - Al presionar Enter o el botón sale "**[Nombre], ¿deseas confirmar el cambio?**" con Sí y No. El nombre sale de la sesión.
  - Con Sí, el cambio se confirma y se ve el dato nuevo.
  - Con No, o si la persona cierra, el registro muestra "**Cambio pendiente de confirmar**" y la opción de confirmar o descartar.
  - Casilla opcional "Observaciones".
  - Crear, modificar y borrar se comportan igual.
  - Texto escrito sin presionar Enter se pierde al cerrar, y eso es correcto.
- **Prueba:** `pytest tests/ui/test_ui18_confirmar.py` más las pruebas de UI-09 a UI-13, actualizadas y en viewport de teléfono:
  - Sí → dato nuevo.
  - No → el dato no cambia y aparece el pendiente.
  - Recargar la página, que simula otro dispositivo → el pendiente sigue ahí.
  - Borrar pide confirmación.
- **Commit:** `UI-18: confirmación de cambios y pendientes`

### UI-19 · Aviso de posible duplicado
- **Dueño:** Builder_UI · **Espera:** DAT-20, UI-18
- **Archivos:** `web/componentes/duplicado.js`, `web/estilos/formulario.css`, `tests/ui/test_ui19_duplicado.py`
- **Entregable:** ante un `409 posible_duplicado`, muestra "Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?" con tres opciones:
  - **Revisar:** abre el registro existente.
  - **Cancelar.**
  - **Crear de todos modos.**
- **Prueba:** `pytest tests/ui/test_ui19_duplicado.py`: las tres opciones hacen lo que dicen.
- **Commit:** `UI-19: aviso de posible duplicado`

### INT-18 · Arreglar la prueba histórica de dos dispositivos
- **Dueño:** Builder_Integraciones · **Espera:** — (libre) · **Agregada 2026-09-27 con `/luz-verde`.**
- **Archivos:** `tests/test_int13_acceso.py` (solo `test_dos_dispositivos_y_acceso_protegido`). **Excepción autorizada** a la regla de no editar pruebas existentes.
- **Entregable:** la prueba se escribió antes de la confirmación Sí/No de la fase 2b. Se actualiza para que confirme el alta con "Sí" (`POST /api/cambios/{id}/confirmar`) antes de revisar la actividad. Lo que comprueba no se debilita: dos dispositivos con sesión, credencial de servicio y actividad a nombre de quien confirmó.
- **Prueba:** `pytest tests/test_int13_acceso.py -q` pasa; la suite completa, sin fallas.
- **Commit:** `INT-18: prueba de dos dispositivos con confirmación Sí`

### UI-20 · Botón y pantalla "Reporte del día"
- **Dueño:** Builder_UI · **Espera:** DAT-21, UI-18
- **Archivos:** `web/reporte/**`, `web/navegacion/rutas.js`, `web/app.js`, `tests/ui/test_ui20_reporte.py`, `evidencia/UI-20/`
- **Entregable:**
  - Botón "Reporte del día" junto a las áreas del detalle. **No va en el nivel 1**, que sigue sin tablas ni cifras.
  - Tabla con las 7 columnas y selector de fecha para ver días pasados.
  - Se nota a simple vista cuándo ejecutó Vania y cuándo una persona.
- **Prueba:** `pytest tests/ui/test_ui20_reporte.py` en viewport de teléfono:
  - El botón abre el reporte de hoy.
  - Cambiar la fecha muestra ese día.
  - El nivel 1 no muestra ninguna tabla.
- **Commit:** `UI-20: reporte del día en el Dashboard`

### MAN-10 · Vania: link de entrada, confirmación Sí/No y observaciones (MANUAL, Hermes)
- **Espera:** INT-17, MAN-01
- **Entregable:** configurar en Hermes y SOUL.md lo siguiente:
  - Vania pide el link (`POST /api/acceso/enlace`) solo cuando la persona lo solicita, y avisa que tiene 10 minutos.
  - Crea el cambio, pregunta "¿Sí o No?" y confirma.
  - Pregunta si hay alguna observación que registrar.
  - Manda el reporte del día cuando se lo piden.

### VER-09 · Verificación de la fase 2b
- **Dueño:** Verificador · **Espera:** las tareas de la fase 2b hechas o bloqueadas · **Archivos:** `plan/verificacion/VER-09.md`
- **Entregable:** vuelve a correr las pruebas de la fase. Revisa, contra `REGLAS_OPERACION.md`:
  - Ningún camino escribe el dato oficial sin confirmación: recorrer las rutas de escritura de `/openapi.json`.
  - Vania nunca aparece como solicitante.
  - Un pendiente vencido no se confirma.
  - El reporte solo muestra cambios confirmados.
  - Las sesiones vencen a las 18:00, o a las 23:59 si se crearon después.
  - No hay números de teléfono en git: `git grep -nE "\+?52 ?1? ?[0-9]{2,3} ?[0-9]{3,4} ?[0-9]{4}"` no devuelve nada.
- **Commit:** `VER-09: verificación de la fase 2b`

---

## Fase 3 · Rastro de Vania

### INT-02 · API de actividad
- **Dueño:** Builder_Integraciones · **Espera:** INT-01 · **Archivos:** `app/api/actividad.py`, `tests/test_int02_api_actividad.py`
- **Entregable:** `GET /api/actividad`, de la más reciente a la más antigua, paginado y con filtros por `actor` y `area`. Devuelve solo lo que ocurrió: sin contadores ni resúmenes de "engagement".
- **Prueba:** `pytest tests/test_int02_api_actividad.py -q`: el orden, la paginación y los filtros.
- **Commit:** `INT-02: API de actividad`

### INT-03 · Actividad sintética de Vania
- **Dueño:** Builder_Integraciones · **Espera:** INT-01, DAT-06 · **Archivos:** `app/fuentes/actividad_sintetica.py`, `tests/test_int03_actividad_sintetica.py`
- **Entregable:** comando `python -m app.fuentes.actividad_sintetica`, que carga movimientos de ejemplo con actor `vania`, marcados como sintéticos, tomando como base los ejemplos del handshake: registró un pago, actualizó un dato, detectó un vencimiento, encontró algo que necesita revisión. Las referencias apuntan a registros que existen en el escenario `con_atencion`.
- **Prueba:** `pytest tests/test_int03_actividad_sintetica.py -q`: todo es sintético y todas las referencias existen.
- **Commit:** `INT-03: actividad sintética de Vania`

### UI-14 · Rastro de Vania visible
- **CERRADA sin código (2026-09-27, `/luz-verde`):** la cubre el Reporte del día (columna Ejecutor, DAT-21 y UI-20), según D-8. No se hace bitácora aparte.
- **Dueño:** Builder_UI. La representación visual queda en Builder_UI para mantener un solo lenguaje visual; los datos y la API son de Builder_Integraciones.
- **Espera:** **D-8**, INT-02, INT-03, UI-07
- **Archivos:** `web/rastro/rastro.js`, `web/rastro/rastro.css`, `tests/ui/test_ui14_rastro.py`, `evidencia/UI-14/`
- **Entregable:** el rastro según D-8, incluido el tratamiento de las correcciones humanas.
- **Prueba:** `pytest tests/ui/test_ui14_rastro.py`: con actividad sintética cargada, los movimientos de Vania aparecen como decide D-8; sin actividad no aparece nada inventado; la jerarquía del rastro es menor que la de la conclusión.
- **Commit:** `UI-14: rastro de Vania`

---

## Fase 4 · Superficie para Vania

Objetivo: que Vania pueda consultar y actuar a través de la API, con el mismo estado que el Dashboard. **Lo que ocurre dentro de Hermes es MANUAL.**

### INT-05 · Contrato de uso para Vania
- **Dueño:** Builder_Integraciones · **Espera:** **D-3**, DAT-08, DAT-12, INT-02, INT-04 · **Archivos:** `docs/contrato-vania.md`
- **Entregable:** documento para quien conecte a Vania. Cubre:
  - Qué endpoint usar para cada intención, con ejemplos: "¿cómo está Works?" → `/api/estado`; "registra que la 204 pagó septiembre" → registrar pago.
  - Cómo se autentica (credencial de servicio).
  - Reglas del handshake que Vania debe respetar: no inventar datos, confirmar lo que se le pidió, no contactar inquilinos y registrar siempre con actor `vania`.
  - El caso de error.
- **Prueba:** cada endpoint citado existe en `GET /openapi.json` del servicio local. Comando: `python3 -c` que extrae las rutas del documento y las compara contra el OpenAPI; no debe faltar ninguna.
- **Commit:** `INT-05: contrato de uso de la API para Vania`

### INT-06 · Resumen de avisos agrupados
- **Dueño:** Builder_Integraciones · **Espera:** **D-3**, DAT-07 · **Archivos:** `app/api/avisos.py`, `tests/test_int06_avisos.py`
- **Entregable:** `GET /api/vania/avisos`, solo con credencial de servicio.
  - Si el estado tiene asuntos, devuelve **un solo** mensaje agrupado ("Hay tres cosas que requieren atención hoy: …") con sus asuntos.
  - Si no hay nada, responde `204` sin contenido.
  - No envía nada por sí mismo: quien escribe por WhatsApp es Vania, desde Hermes.
- **Prueba:** `pytest tests/test_int06_avisos.py -q`: `tranquilo` → 204; `con_atencion` → un mensaje con N asuntos, los mismos del estado; sin credencial → 401.
- **Commit:** `INT-06: resumen de avisos agrupados para Vania`

### INT-07 · Preferencias para reducir o silenciar avisos
- **Dueño:** Builder_Integraciones · **Espera:** **D-11**, INT-06 · **Archivos:** `app/db/migraciones/003_preferencias_avisos.sql`, `app/api/avisos.py`, `tests/test_int07_preferencias.py`
- **Entregable:** según D-11. Guardar, consultar y quitar preferencias (persona, tipo de evento, hasta cuándo). `GET /api/vania/avisos` las respeta.
- **Prueba:** `pytest tests/test_int07_preferencias.py -q`: silenciar "contratos" hace que el aviso excluya esos asuntos mientras dure la preferencia; el Dashboard sigue mostrándolos, porque silenciar avisos no oculta el estado.
- **Commit:** `INT-07: preferencias de avisos`

### MAN-01 · Conectar a Vania con la API (MANUAL, la hace el usuario)
- **Espera:** INT-05, MAN-06, U-4
- **Instrucciones:**
  1. En el VPS, define `WORKS_TOKEN_VANIA` con un valor largo y aleatorio en el entorno del servicio (MAN-06) y guárdalo solo en la configuración del perfil `vania` en Hermes.
  2. En el perfil `vania` de Hermes, agrega las herramientas que llaman a los endpoints de `docs/contrato-vania.md`, con la credencial en el encabezado que indica ese documento.
  3. Desde tu WhatsApp autorizado, pregúntale a Vania "¿cómo está Works?". Compara su respuesta con lo que muestra el Dashboard: deben coincidir.
  4. Pídele "registra que la oficina <una sintética> pagó este mes por transferencia". Comprueba en el Dashboard que el pago cambió y que aparece en el rastro con actor Vania.
  5. Avísale a la sesión maestra el resultado, para que actualice `plan/estado/Manual.md`.

### MAN-02 · Proactividad de Vania para Works (MANUAL)
- **Espera:** INT-06, MAN-01. D-11 para que quede completa.
- **Instrucciones:**
  1. En Hermes, programa una revisión periódica que consulte `GET /api/vania/avisos`. La frecuencia la eliges tú, porque el handshake rechazó fijar un tope.
  2. Si la respuesta es `204`, Vania no escribe. Si trae contenido, Vania manda **un solo** mensaje a David y a Grecia.
  3. Prueba con el escenario `tranquilo`: no debe llegar nada. Luego con `con_atencion`: debe llegar un mensaje agrupado.
  4. Reporta el resultado a la sesión maestra.

### MAN-03 · Especializar a Vania para Works (MANUAL)
- **Espera:** INT-05
- **Instrucciones:** en `SOUL.md` o en la configuración del perfil `vania`, agrega las reglas de `docs/contrato-vania.md`: trabaja solo con datos del sistema y no inventa; confirma las acciones solicitadas; no contacta inquilinos; agrupa los avisos; si no hay nada, no escribe; respeta cuando le piden bajarle a los avisos. Reporta a la sesión maestra cuando esté listo.

### VER-04 · Verificación de las fases 3 y 4
- **Dueño:** Verificador · **Espera:** las tareas de las fases 3 y 4 hechas o bloqueadas (sin incluir MAN) · **Archivos:** `plan/verificacion/VER-04.md`
- **Entregable:** vuelve a correr las pruebas. Revisión:
  - Avisos y estado dicen lo mismo: un solo cerebro.
  - `204` cuando no hay nada.
  - Ningún endpoint envía mensajes a terceros: `grep -rniE "wa\.me|whatsapp|smtp|sms" app/` se revisa a mano.
  - La actividad sintética está marcada.
- **Commit:** `VER-04: verificación de las fases 3 y 4`

---

## Fase 5 · Seguir la conversación con Vania desde el Dashboard

### INT-08 · Mecanismo para pasar el contexto
- **NO AUTORIZADA (2026-09-27, instrucción del usuario):** el usuario no quiere un botón que abra WhatsApp con Vania y el mensaje ya escrito. No se construye ni se propone.
- **Dueño:** Builder_Integraciones · **Espera:** **D-9**, U-5 (número de Vania), INT-02
- **Archivos:** `web/componentes/continuar-con-vania.js`, `tests/ui/test_int08_contexto.py`. Si D-9 = B o C, además `app/api/contexto.py` y `app/db/migraciones/007_contextos.sql`.
- **Entregable:** función `enlaceParaVania(asunto)`, que produce el enlace o la referencia según D-9. El número de Vania se configura en un solo lugar y no se escribe en el código.
- **Prueba:** `pytest tests/ui/test_int08_contexto.py`: para un asunto de ejemplo, el enlace tiene el formato documentado (RES-02) y el texto incluye la frase del asunto.
- **Commit:** `INT-08: paso de contexto del Dashboard a Vania`

### UI-15 · Botón "seguir con Vania" en asuntos y detalle
- **NO AUTORIZADA (2026-09-27, instrucción del usuario):** el usuario no quiere un botón que abra WhatsApp con Vania y el mensaje ya escrito. No se construye ni se propone.
- **Dueño:** Builder_UI · **Espera:** INT-08, UI-13 · **Archivos:** `web/nivel2/nivel2.js`, `web/detalle/*.js`, `tests/ui/test_ui15_seguir_con_vania.py`, `evidencia/UI-15/`
- **Entregable:** en cada asunto y en cada ficha, una acción discreta que usa `enlaceParaVania`. No hay chat dentro del Dashboard.
- **Prueba:** `pytest tests/ui/test_ui15_seguir_con_vania.py`: la acción existe en asuntos y fichas y su `href` sale de `enlaceParaVania`.
- **Commit:** `UI-15: seguir con Vania desde el Dashboard`

---

## Fase 6 · Capacidad heroica: documento útil → HP Smart Tank

### INT-09 · Tubería de documento imprimible
- **Dueño:** Builder_Integraciones · **Espera:** **D-7**, U-3, DAT-08
- **Archivos:** `pyproject.toml` (no al mismo tiempo que DAT-01 ni DAT-15), `app/documentos/__init__.py`, `app/documentos/generar.py`, `app/documentos/plantillas/base.html`, `app/documentos/plantillas/prueba.html`, `tests/test_int09_documentos.py`
- **Entregable:** plantilla → archivo en el formato que acepta la ruta elegida en D-7 (dato U-3). Usa un documento de prueba con los datos del estado, encabezado "Documento de prueba · datos sintéticos". Lee los datos por `app/`, nunca de SQLite directamente.
- **Prueba:** `pytest tests/test_int09_documentos.py -q`: se genera un archivo no vacío del tipo esperado, que contiene la conclusión del estado y la marca de datos sintéticos.
- **Commit:** `INT-09: tubería de documento imprimible`

### INT-10 · Primer documento de Works
- **Dueño:** Builder_Integraciones · **Espera:** **D-6**, que el handshake liga a los datos reales, e INT-09
- **Archivos:** `app/documentos/plantillas/<documento>.html`, `app/documentos/<documento>.py`, `tests/test_int10_documento.py`
- **Entregable:** el documento que elija D-6, en frases humanas y a partir del estado. Se prueba con datos sintéticos y se revisa con reales en la fase 9.
- **Prueba:** `pytest tests/test_int10_documento.py -q`: el documento contiene lo que D-6 define y nada fuera de la lista de lo que puede imprimirse.
- **Commit:** `INT-10: documento <nombre> para la capacidad heroica`

### INT-11 · Endpoint para que Vania pida el documento
- **Dueño:** Builder_Integraciones · **Espera:** **D-6**, **D-7**, INT-10 · **Archivos:** `app/api/documentos.py`, `tests/test_int11_api_documentos.py`
- **Entregable:** `GET /api/vania/documentos/<tipo>`, solo con credencial de servicio. Solo sirve tipos que estén en la lista de lo que puede imprimirse (D-6). Cada petición deja actividad ("Vania preparó el documento …").
- **Prueba:** `pytest tests/test_int11_api_documentos.py -q`: un tipo permitido → archivo; un tipo no permitido → 404; sin credencial → 401; se registra la actividad.
- **Commit:** `INT-11: endpoint de documentos para Vania`

### MAN-04 · Imprimir en la HP desde Vania (MANUAL)
- **Espera:** INT-11, MAN-01, **D-7**, U-3
- **Instrucciones:**
  1. En Hermes, conecta la herramienta de impresión que ya existe con `GET /api/vania/documentos/<tipo>`, usando el formato que definiste en U-3.
  2. Desde WhatsApp: "Vania, déjame impreso <el documento de D-6>".
  3. Comprueba que sale en la HP de Works y que el Dashboard muestra en el rastro que Vania preparó el documento.
  4. Reporta a la sesión maestra.

---

## Fase 7 · Pizarrón mensual

### DAT-13 · Datos mínimos de personas para el pizarrón
- **NO SE HACE salvo que Grecia lo pida (2026-09-27, instrucción del usuario):** el pizarrón es un módulo expandible para ofrecerle a Grecia más adelante. Nadie trabaja en él por iniciativa propia.
- **Dueño:** Builder_Datos · **Espera:** **D-10**, DAT-09 · **Archivos:** `app/db/migraciones/004_personas.sql`, `app/api/personas.py`, `tests/test_dat13_personas.py`
- **Entregable:** solo los campos que fije D-10, con `origen_dato`, y una API para listarlas, crearlas y editarlas con rastro de actividad. Nada más: no es un sistema de gestión de comunidad.
- **Prueba:** `pytest tests/test_dat13_personas.py -q`: el CRUD mínimo, la actividad, y que no exista ninguna columna fuera de lo que fija D-10.
- **Commit:** `DAT-13: datos mínimos de personas para el pizarrón`

### INT-12 · Composición del pizarrón del mes
- **NO SE HACE salvo que Grecia lo pida (2026-09-27, instrucción del usuario):** el pizarrón es un módulo expandible para ofrecerle a Grecia más adelante. Nadie trabaja en él por iniciativa propia.
- **Dueño:** Builder_Integraciones · **Espera:** **D-10**, DAT-13, INT-09, RES-03
- **Archivos:** `app/documentos/pizarron.py`, `app/documentos/plantillas/pizarron.html`, `app/api/documentos.py`, `tests/test_int12_pizarron.py`
- **Entregable:** "prepara el pizarrón de octubre" → un documento con los cumpleaños del mes y las efemérides de la fuente que elija D-10. Se sirve por el mismo endpoint de documentos, para que Vania lo deje listo o lo mande a imprimir.
- **Prueba:** `pytest tests/test_int12_pizarron.py -q`: con personas sintéticas, el pizarrón de un mes incluye solo a quienes cumplen en ese mes y las efemérides de ese mes.
- **Commit:** `INT-12: pizarrón mensual de cumpleaños y efemérides`

### VER-05 · Verificación de las fases 5, 6 y 7
- **Dueño:** Verificador · **Espera:** las tareas de las fases 5 a 7 hechas o bloqueadas · **Archivos:** `plan/verificacion/VER-05.md`
- **Entregable:** vuelve a correr las pruebas. Revisión:
  - Solo se imprime lo que está en la lista.
  - Los documentos sintéticos están marcados.
  - El pizarrón no agrega campos de personas fuera de D-10.
  - No hay chat dentro del Dashboard.
- **Commit:** `VER-05: verificación de las fases 5 a 7`

---

## Fase 8 · Acceso

Objetivo: el acceso restringido que el handshake exige antes de usar datos reales.

### INT-13 · Control de acceso mínimo
- **Dueño:** Builder_Integraciones · **Espera:** **D-4**, INT-04
- **Archivos:** `app/db/migraciones/005_cuentas.sql`, `app/seguridad/sesion.py`, `app/seguridad/actor.py`, `app/api/acceso.py`, `tests/test_int13_acceso.py` y, para que las pruebas existentes entren con una sesión de prueba y la actividad registre a la persona, `app/actividad/registrar.py`, `tests/conftest.py` y `tests/ui/conftest.py` (corrección del 2026-09-26)
- **Entregable:** el mecanismo de D-4, según `plan/REGLAS_OPERACION.md` (acceso y sesiones):
  - `POST /api/acceso/enlace`: solo con la credencial de Vania y el número de WhatsApp de David o Grecia. Devuelve un link con token de un solo uso que vence a los **10 minutos**, junto con `vence_en`. El número del desarrollador o uno desconocido → 403.
  - Abrir el link consume el token y crea una sesión para ese dispositivo. Un token usado, vencido o inválido no sirve.
  - Varias sesiones por persona y por dispositivo al mismo tiempo. Una sesión nueva no invalida las otras.
  - La sesión vence a las **18:00 de `America/Mexico_City`** del día en que se creó, o a las 23:59 si se creó a las 18:00 o después.
  - Los números de WhatsApp viven en la configuración del servidor (`var/` o variables de entorno). **Nunca en git.**
  - Sin sesión válida, todo `/api/*` responde 401, excepto `/api/salud` y el propio flujo de entrada.
  - `actor_actual()` ahora identifica también a la persona (David o Grecia).
  - La credencial de servicio de Vania sigue funcionando.
  - Cookies con `Secure`, `HttpOnly` y `SameSite` (R4).
- **Prueba:** `pytest tests/test_int13_acceso.py -q` y la suite completa (`.venv/bin/python -m pytest -q`) en verde. En `test_int13_acceso.py`: token usado dos veces → la segunda falla; token de 11 minutos → falla; sesión creada a las 17:00 vence a las 18:00 y una de las 19:00 vence a las 23:59 (reloj simulado); dos dispositivos de Grecia con sesión a la vez; sin sesión → 401; con sesión → 200 y la actividad registra a la persona; Vania con credencial → 200; la cookie trae los tres atributos.
- **Commit:** `INT-13: control de acceso mínimo`

### INT-14 · Flujo de entrada en el teléfono
- **Dueño:** Builder_Integraciones · **Espera:** **D-4**, INT-13, UI-03 · **Archivos:** `web/acceso/**`, `tests/ui/test_int14_entrada.py`, `evidencia/INT-14/`
- **Entregable:** la pantalla o pantallas de entrada según D-4, con los componentes neumórficos de UI-03. Sin instrucciones técnicas y en muy pocos pasos. Sin ícono en la pantalla de inicio (D-4). Link vencido o ya usado → "Este enlace ya no sirve. Pídele a Vania uno nuevo."
- **Prueba:** `pytest tests/ui/test_int14_entrada.py`: el flujo completo en viewport de teléfono termina en el nivel 1; un enlace o credencial vencidos muestran un mensaje humano con qué hacer.
- **Commit:** `INT-14: flujo de entrada al Dashboard`

### INT-15 · Roles `Admin` y `Editor` · CANCELADA (D-5, 2026-09-26: sin roles; solo el desarrollador administra cuentas con INT-16)
- **Dueño:** Builder_Integraciones · **Espera:** **D-5** (solo si D-5 = B), INT-14 · **Archivos:** `app/db/migraciones/006_roles.sql`, `app/seguridad/roles.py`, `web/acceso/cuentas.*`, `tests/test_int15_roles.py`
- **Entregable:** David (`Admin`) puede desactivar y reactivar la cuenta de Grecia. Grecia (`Editor`) ve y edita lo mismo, pero no puede administrar la cuenta de David. No cambia nada de lo que cada quien ve.
- **Prueba:** `pytest tests/test_int15_roles.py -q`: Editor intenta desactivar a Admin → 403; Admin desactiva a Editor → la sesión de Editor deja de valer; los dos obtienen la misma respuesta de `/api/estado`.
- **Commit:** `INT-15: roles Admin y Editor`

### INT-16 · Acceso técnico del desarrollador
- **Dueño:** Builder_Integraciones · **Espera:** **D-4**, INT-13 · **Archivos:** `app/seguridad/admin.py`, `app/seguridad/sesion.py` (corrección del 2026-09-26), `tests/test_int16_admin.py`
- **Entregable:** comando `python -m app.seguridad.admin` para crear, desactivar y listar cuentas, registrar el número de WhatsApp de cada cuenta (se guarda fuera de git) y revocar sesiones. Solo se usa en el servidor y no está expuesto en el Dashboard. Queda separado de `Admin`/`Editor`.
- **Prueba:** `pytest tests/test_int16_admin.py -q`: crear una cuenta, revocar sus sesiones y comprobar que ya no puede entrar.
- **Commit:** `INT-16: comando de administración técnica`

### VER-06 · Verificación de la fase 8
- **Dueño:** Verificador · **Espera:** las tareas de la fase 8 hechas o bloqueadas · **Archivos:** `plan/verificacion/VER-06.md`
- **Entregable:** vuelve a correr las pruebas. Revisión:
  - Ningún endpoint de datos responde sin sesión ni credencial: recorrer todas las rutas de `/openapi.json` sin credenciales y confirmar 401, salvo las excepciones documentadas.
  - La misma información para David y Grecia.
  - El acceso del desarrollador está separado.
- **Commit:** `VER-06: verificación de la fase 8`

---

## Fase 9 · Datos reales (espera el Excel de Works)

**Toda la fase espera U-1, el Excel.** Además, ninguna tarea carga datos reales antes de que INT-13 esté hecha. El archivo vive en `datos_reales/`, que está fuera de git.

### DAT-14 · Mapeo del Excel al modelo
- **Dueño:** Builder_Datos · **Espera:** U-1 · **Archivos:** `docs/mapeo-excel.md`
- **Entregable:** las columnas reales y su correspondencia con el esquema; lo que va a `extras`; los huecos, que se registran como vacíos y no se rellenan; cuánto historial de pagos hay (P1); si hay fechas de nacimiento (P2); y los cambios de esquema necesarios, que **no** se aplican, sino que se proponen a la sesión maestra. El documento no copia datos personales: solo nombres de columnas y conteos.
- **Prueba:** el documento cubre cada columna del Excel. Comprobación: el conteo de columnas que menciona el documento coincide con el del archivo.
- **Commit:** `DAT-14: mapeo del Excel de Works al modelo`

### DAT-15 · Fuente Excel
- **Dueño:** Builder_Datos · **Espera:** DAT-14, INT-13 · **Archivos:** `pyproject.toml` (no al mismo tiempo que DAT-01 ni INT-09), `app/fuentes/excel.py`, `tests/test_dat15_excel.py`
- **Entregable:** implementa `FuenteDatos` para el Excel según el mapeo. Marca todo con `origen_dato='excel'` y no inventa valores faltantes. La prueba usa un Excel **sintético** con la misma forma, creado dentro de la prueba; nunca el real.
- **Prueba:** `pytest tests/test_dat15_excel.py -q`: el Excel sintético se carga, los huecos quedan vacíos y el `origen_dato` es correcto.
- **Commit:** `DAT-15: fuente de datos desde el Excel`

### DAT-16 · Reporte de calidad de la importación
- **Dueño:** Builder_Datos · **Espera:** DAT-15 · **Archivos:** `app/fuentes/reporte.py`, `tests/test_dat16_reporte.py`
- **Entregable:** `python -m app.fuentes.reporte`, que lista faltantes, contradicciones y registros sin correspondencia, en frases humanas y sin corregir nada.
- **Prueba:** `pytest tests/test_dat16_reporte.py -q`: un Excel sintético con huecos conocidos produce exactamente esos hallazgos.
- **Commit:** `DAT-16: reporte de calidad de la importación`

### UI-16 · Ajustar el detalle a los campos reales
- **Dueño:** Builder_UI · **Espera:** DAT-15, UI-13 · **Archivos:** `web/detalle/*.js`, `tests/ui/test_ui16_campos_reales.py`
- **Entregable:** las fichas muestran y editan los campos que resulten del mapeo, incluidos los de `extras` que el mapeo marque como visibles. No se rehace ninguna pantalla.
- **Prueba:** `pytest tests/ui/test_ui16_campos_reales.py`, con el Excel sintético de DAT-15: cada campo mapeado aparece en su ficha.
- **Commit:** `UI-16: detalle ajustado a los campos reales`

### VER-07 · Verificación de la fase 9
- **Dueño:** Verificador · **Espera:** las tareas de la fase 9 · **Archivos:** `plan/verificacion/VER-07.md`
- **Entregable:** vuelve a correr las pruebas. Revisión:
  - `git ls-files datos_reales` no devuelve nada.
  - No hay valores inventados: los faltantes siguen vacíos.
  - INT-13 estaba hecha antes de la primera carga real, según el orden de los commits (`git log`).
- **Commit:** `VER-07: verificación de la fase 9`

---

## Fase 10 · Despliegue y prueba con David y Grecia

Todo lo que ocurre en el VPS es **MANUAL**. La sesión maestra registra el avance en `plan/estado/Manual.md` cuando tú se lo reportas.

### VER-08 · Revisión completa previa al despliegue
- **Dueño:** Verificador · **Espera:** VER-01 a VER-07 · **Archivos:** `plan/verificacion/VER-08.md`
- **Entregable:** corre toda la suite (`pytest -q` y `pytest tests/ui`) y recorre "Decisiones ya tomadas" del handshake punto por punto. Cada punto queda como cumple, no cumple o no aplica, con evidencia. Al final, la lista de D-x y U-x que siguen abiertas.
- **Commit:** `VER-08: revisión completa previa al despliegue`

### MAN-05 · Dominio y HTTPS en el VPS (MANUAL)
- **Espera:** U-6
- **Instrucciones:** elige el subdominio del Dashboard, configura HTTPS en el proxy inverso que ya uses, y comprueba desde tu teléfono que la dirección abre con candado. Reporta a la sesión maestra el dominio final, porque se necesita para D-4 y D-9.

### MAN-06 · Desplegar el servicio en el VPS (MANUAL)
- **Espera:** MAN-05, VER-06 (acceso probado), VER-08
- **Instrucciones:**
  1. En tu máquina, dentro del repositorio: `git bundle create works.bundle --all`. No hay remoto y nadie hace push.
  2. Copia `works.bundle` al VPS y ahí: `git clone works.bundle works`.
  3. Crea el entorno según D-2 e instala las dependencias.
  4. Define las variables de entorno `WORKS_DB` (fuera de la carpeta del código), `WORKS_TOKEN_VANIA` y las que agregue INT-13.
  5. `python -m app.db.migrar`.
  6. Arranca el servicio como servicio del sistema detrás del proxy de MAN-05.
  7. Carga el escenario sintético `con_atencion` y ábrelo desde tu teléfono: debe pedirte entrar (D-4) y luego mostrar el nivel 1 con el aviso de datos sintéticos.
  8. Reporta a la sesión maestra.

### MAN-07 · Respaldo durante la prueba (MANUAL)
- **Espera:** **D-12**, MAN-06
- **Instrucciones:** aplica la opción de D-12. Si es A o B: programa `sqlite3 "$WORKS_DB" ".backup '<ruta>/works-$(date +%F).db'"` una vez al día, borra las copias que excedan la retención elegida, y restaura una copia en una ruta temporal para comprobar que abre. Reporta a la sesión maestra.

### MAN-08 · Límites de uso durante la prueba (MANUAL)
- **Espera:** **D-13**, U-2, MAN-01
- **Instrucciones:** aplica en Hermes el límite que decidas en D-13 y anota la cifra en `plan/DECISIONES.md`, en "Respuestas", a través de la sesión maestra.

### MAN-09 · Pruebas finales con datos reales y apertura (MANUAL)
- **Espera:** VER-07, MAN-01 a MAN-08, **D-14**
- **Instrucciones:**
  1. Copia el Excel a `datos_reales/` en el VPS y carga con la fuente `excel`.
  2. Corre `python -m app.fuentes.reporte` y revisa los hallazgos antes de abrir el acceso.
  3. Comprueba que el Dashboard y Vania dicen lo mismo.
  4. Da de alta a David y a Grecia según D-4.
  5. Prepara la observación de adopción según D-14.
  6. Avisa a la sesión maestra la fecha de apertura.

---

## Tareas del Researcher (transversales, libres desde el inicio)

Reglas: solo web pública, nada del VPS. Formato igual al del Scavenge: fuentes consultadas, hechos con fuente y vacíos. Lo no verificado o inferido va como vacío. No modifica el Scavenge ni `DECISIONES.md`: entrega su archivo, y la sesión maestra lo integra.

### RES-01 · Persistencia de sesión en navegadores móviles y PWA
- **CERRADA sin investigar (2026-09-27, instrucción del usuario):** ya está definido en D-4. El enlace de Vania dura 10 minutos y es de un solo uso; la sesión dura hasta las 23:59 de ese día; al día siguiente se pide otro enlace a Vania.
- **Dueño:** Researcher · **Espera:** — · **Archivos:** `plan/investigacion/RES-01.md`
- **Pregunta:** ¿cuánto dura una cookie de sesión `HttpOnly` fijada por el servidor en Safari de iOS y en Chrome de Android? ¿Qué cambia si el sitio se agrega a la pantalla de inicio (PWA)? ¿Hay borrados automáticos (por ejemplo, las políticas de ITP de Safari)? Busca también una fuente para la fricción de la "sesión de larga duración", que el Scavenge dejó como vacío (N2). Alimenta D-4.
- **Prueba:** cada hecho tiene URL. Los vacíos están declarados.
- **Commit:** `RES-01: persistencia de sesión en móvil y PWA`

### RES-02 · Enlaces de WhatsApp con texto prellenado
- **NO AUTORIZADA (2026-09-27, instrucción del usuario):** el usuario ya había dicho que no quiere esto. No se investiga ni se construye.
- **Dueño:** Researcher · **Espera:** — · **Archivos:** `plan/investigacion/RES-02.md`
- **Pregunta:** formato oficial de `wa.me` / "click to chat" con texto; límites de longitud; comportamiento en iOS, Android y escritorio; si funciona igual hacia números de WhatsApp Business y personales. Alimenta D-9.
- **Commit:** `RES-02: enlaces de WhatsApp con texto prellenado`

### RES-03 · Fuentes públicas de efemérides de México
- **NO SE HACE salvo que Grecia lo pida (2026-09-27, instrucción del usuario):** el pizarrón es un módulo expandible para ofrecerle a Grecia más adelante. Nadie trabaja en él por iniciativa propia.
- **Dueño:** Researcher · **Espera:** — · **Archivos:** `plan/investigacion/RES-03.md`
- **Pregunta:** ¿qué fuentes oficiales o públicas listan las fechas cívicas y efemérides de México (por ejemplo, las fechas solemnes de la Ley sobre el Escudo, la Bandera y el Himno Nacionales)? ¿En qué formato están y con qué condiciones de uso? Alimenta D-10.
- **Commit:** `RES-03: fuentes de efemérides de México`

### RES-04 · HP Smart Tank 750 en listados IPP Everywhere / Mopria
- **CERRADA sin investigar (2026-09-27, instrucción del usuario):** pregunta mal planteada. La impresora es de oficina y varias computadoras imprimen en ella a diario; ya está vinculada por IPP y acepta PDF (`vinculacion-hp-smart-tank-750-ubuntu.md`). Con D-7 = A, el Dashboard solo genera el PDF y Vania lo imprime con la herramienta que ya tiene en Hermes; la certificación no cambia nada.
- **Dueño:** Researcher · **Espera:** — · **Archivos:** `plan/investigacion/RES-04.md`
- **Pregunta:** ¿aparece el modelo en el listado público de impresoras IPP Everywhere de la PWG o en el de dispositivos certificados de Mopria? ¿Qué formatos de documento declaran esos listados (PDF, PWG-Raster, URF, JPEG)? Cierra o confirma los vacíos V1, V4 y V5 de R1. Alimenta D-7.
- **Commit:** `RES-04: certificación IPP Everywhere / Mopria del Smart Tank 750`

---

## Fase 2c · Rediseño visual (2026-09-26)

**Fuente de verdad:** `plan/rediseno/DASHBOARD_DESIGN_SPEC.md` (en adelante, "el documento"). Manda sobre cualquier regla visual anterior de este plan (paleta, acento terracota, sombras de UI-02 y UI-03).

**Reglas de la fase (valen para UI-21, UI-22 y UI-23):**
- **Solo cambia el aspecto y la respuesta de los controles.** No cambian datos, textos de negocio, acciones, flujos, rutas, sesiones, confirmación, pendientes, duplicados ni reporte. No se quita ni se esconde nada que hoy se vea (sección 1.11 del documento: la app no tiene nada clasificado como secundario).
- **Las pruebas que ya existen no se editan.** Tienen que seguir pasando igual. Si una falla por un cambio visual, la tarea queda `bloqueada (<prueba> falla por <motivo>)`.
- **Recursos locales, sin internet al abrir la app:** la letra Inter Variable (`.woff2`) y los íconos Lucide (`.svg` sueltos, solo los que se usen) se guardan dentro de `web/`. Sus licencias (OFL e ISC) van junto a los archivos. Nada se carga desde un CDN.
- `python3 scripts/contraste.py web/estilos/tokens.css` sigue terminando en 0.
- **Uso de los grises y los colores de estado** (decisión del usuario): el texto principal va en `#202734`. El texto secundario y las notas chicas van en `#596575`. El gris tenue `#7B8794` **nunca va en texto**: solo en íconos secundarios, bordes, separadores y adornos. Verde, ámbar y rojo se usan solo para estados (íconos, señales, bordes y fondos tonales), no para texto chico dentro de campos.
- Se respeta `prefers-reduced-motion: reduce`: sin movimientos, solo cambios de color y sombra.
- Evidencia de cada tarea: capturas a 390 px y a 1280 px en `evidencia/<ID>/`.

### UI-21 · Base del rediseño: sistema visual y controles
- **Dueño:** Builder_UI · **Espera:** — (libre)
- **Archivos:** `web/estilos/tokens.css`, `web/estilos/base.css`, `web/estilos/componentes.css`, `web/fuentes/**` (nuevo), `web/iconos/**` (nuevo), `web/componentes/icono.js` (nuevo), `web/muestras/componentes.html`, `tests/ui/test_ui21_base.py` (nuevo), `evidencia/UI-21/`
- **Entregable:**
  - Secciones 1.2 a 1.12 del documento en `tokens.css` y `base.css`: colores, Inter local, escala tipográfica, niveles de profundidad N0, N1, N2, N-1 y N3, radios, espaciado, retícula y tiempos de movimiento.
  - `icono.js`: una función que pone un ícono Lucide de `web/iconos/` en línea, con tamaño y grosor del documento (1.8).
  - Los controles C-01 a C-10 (sección 2) en `componentes.css`, con todos sus estados: reposo, hover, presionado, soltar, foco, procesando, éxito, error y deshabilitado, según el control.
  - `web/muestras/componentes.html` pasa a ser la pantalla S-02: enseña la gramática plano → elevado → hundido → overlay con todos los controles C-01 a C-10 y sus estados.
- **Prueba:** `pytest tests/ui/test_ui21_base.py` a 390 px:
  - Una superficie estática tiene `box-shadow: none` y un botón no.
  - Al presionar C-01 cambian `transform` y `box-shadow`.
  - Un campo C-04 tiene sombra `inset`.
  - La letra que se usa es Inter y se sirve desde el propio servidor.
  - Ninguna petición sale a otro dominio.
  - El documento no se desborda a lo ancho (`scrollWidth <= 390`).
  - Se guardan las capturas.
  - Además: la suite completa, sin fallas nuevas.
- **Vuelta de refinamiento (2026-09-26, `/luz-verde`):** aplicar `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1.md` (secciones 1 a 13 y 16) sobre la base. Además, los CSS de la tarea y `componentes.html` vuelven a formato legible: una regla por bloque, una propiedad por línea y comentarios breves por sección, como estaba antes el repo. `test_ui21_base.py` puede ampliarse con los criterios de la sección 16 que se puedan medir: el enlace lleva `text-decoration` con subrayado, el deshabilitado tiene borde visible y la tabla tiene `overflow-x: auto` dentro de su contenedor.
- **Corrección puntual T1b (2026-09-26, `/luz-verde`):** aplicar `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1b.md`. C-01, C-02 y Procesando pasan al color del fondo y se recalibran sus sombras. La tabla C-10 no se toca; solo se agrega la captura `evidencia/UI-21/tabla-desplazada-390.png`, con la tabla deslizada a la derecha.
- **Corrección T1c (2026-09-26, orden directa del usuario):** aplicar `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1c.md` con la referencia `plan/rediseno/referencia-relieve-1-6.png`. Relieve de niveles 3 a 5 en C-01, C-02, Procesando, Éxito, Error, Deshabilitado, C-03 y C-09; sin contornos de color como recurso principal. `test_ui21_base.py` puede ajustarse a esta dirección.
- **Corrección T1d (2026-09-27, orden directa del usuario):** reorientación visual con `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1d.md` y las referencias de `evidencia/IDEAL/`, que son la autoridad visual. Los tokens de color y sombra pueden cambiar para parecerse a las referencias, siempre que `scripts/contraste.py` siga en 0. `test_ui21_base.py` puede ajustarse a esta dirección. 
- **Contrato T1e (2026-09-27, orden directa del usuario):** ejecutar `plan/rediseno/NEUMORPHIC_UI_EXECUTION_CONTRACT.md`; manda sobre T1 a T1d. Sin documentos de comparación ni reportes. `test_ui21_base.py` se amplía con las validaciones medibles de las secciones 45 a 47 del contrato.
- **Corrección delta T1f (2026-09-27, orden directa del usuario):** la dirección T1e queda aprobada como base. Ejecutar solo los tres DELTAs de `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1f.md` (franja de C-08, una sola familia de íconos, cavidad de C-04 un poco más profunda); manda sobre T1 a T1e en esos tres puntos. Sin rediseño ni documentos de comparación.
- **Delta T1g (2026-09-27, luz verde del usuario):** solo la silueta de C-08 (doble contorno superior y borde inferior fundido con C-10), según `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1g.md`. Todo lo demás, bloqueado.
- **Pulido T1h (2026-09-27, orden directa del usuario):** dirección aprobada; solo pulido óptico de C-04, C-08 y C-10 más una pasada de consistencia, según `plan/rediseno/DASHBOARD_DESIGN_REFINEMENTS_T1h.md`. Sin rediseño ni informes.
- **Commit:** `UI-21: base del rediseño visual`

### UI-22 · Rediseño de entrada, tablero y áreas
- **Dueño:** Builder_UI_2 · **Espera:** UI-21 (con commit y visto bueno del usuario)
- **Archivos:** `web/acceso/acceso.css`, `web/acceso/index.html` (solo marcado visual; `acceso.js` no se toca), `web/nivel1/**`, `web/nivel2/**`, `web/indicadores/**`, `web/navegacion/navegacion.css`, `web/detalle/{oficinas,inquilinos,contratos,pagos}.js` (solo clases e íconos, sin tocar lógica ni llamadas), `tests/ui/test_ui22_pantallas.py` (nuevo), `evidencia/UI-22/`
- **Entregable:** las pantallas S-01, S-03, S-04 y S-05 del documento, más "Entrada a áreas, listas y fichas" (sección 6), usando solo la base de UI-21. Si necesita un control o un token que la base no tiene, no lo inventa: queda `bloqueada (falta <cosa> en la base)`.
- **Prueba:** `pytest tests/ui/test_ui22_pantallas.py` a 390 px:
  - Cada pantalla carga sin desbordarse a lo ancho.
  - Los bloques solo informativos tienen `box-shadow: none`.
  - Los estados llevan ícono, no solo texto.
  - Se guardan las capturas.
  - Además: la suite completa, sin fallas nuevas.
- **Commit:** `UI-22: rediseño de entrada, tablero y áreas`

### UI-23 · Rediseño de formulario, reporte y ventanas
- **Dueño:** Builder_UI_3 · **Espera:** UI-21 (con commit y visto bueno del usuario)
- **Archivos:** `web/estilos/formulario.css`, `web/componentes/{formulario,confirmacion,duplicado}.js` (solo clases e íconos, sin tocar lógica ni llamadas), `web/reporte/**`, `web/muestras/formulario.html`, `tests/ui/test_ui23_formularios.py` (nuevo), `evidencia/UI-23/`
- **Entregable:** las pantallas S-06 y S-07 del documento, más la ventana de confirmación, el aviso de duplicado y los cambios pendientes (sección 6), usando solo la base de UI-21. Aplica la misma regla de bloqueo que UI-22.
- **Prueba:** `pytest tests/ui/test_ui23_formularios.py` a 390 px:
  - El reporte no desborda el documento (`scrollWidth <= 390`) y su tabla se desplaza dentro de su propio contenedor, sin cortar columnas.
  - La fecha y los campos tienen sombra `inset`.
  - La ventana de confirmación y el aviso de duplicado abren como hoja inferior.
  - Se guardan las capturas.
  - Además: la suite completa, sin fallas nuevas.
- **Commit:** `UI-23: rediseño de formulario, reporte y ventanas`

**Paralelo:** UI-22 y UI-23 corren al mismo tiempo; sus archivos no se cruzan. Ninguna de las dos toca `web/estilos/{tokens,base,componentes}.css`, `web/index.html` ni `web/app.js`.

## Mapa de dependencias por fase

```text
Fase 0  UI-02 ─┐        DAT-01 ─ DAT-02            (D-1, D-2)
               └ UI-01 ─ UI-03
Fase 1  DAT-03 ─┬─ UI-04 ─ UI-05 ─ UI-06 ─┐
                │                         └ UI-07 ◄─ DAT-08 ◄─ DAT-07 (D-3)
        DAT-02 ─┼─ DAT-04 ─ DAT-05 ─ DAT-06 ──────────────────┘
                └─ INT-01          INT-04 (DAT-01)
Fase 2  DAT-09..12 (INT-01, INT-04) ─ UI-10..13 (UI-08, UI-09)
Fase 3  INT-02, INT-03 ─ UI-14 (D-8)
Fase 4  INT-05, INT-06 (D-3) ─ INT-07 (D-11) ─ MAN-01..03
Fase 5  INT-08 (D-9) ─ UI-15
Fase 6  INT-09 (D-7) ─ INT-10 (D-6) ─ INT-11 ─ MAN-04
Fase 7  DAT-13 (D-10) ─ INT-12
Fase 8  INT-13 (D-4) ─ INT-14 ─ INT-15 (D-5), INT-16
Fase 9  DAT-14 (Excel) ─ DAT-15 (INT-13) ─ DAT-16, UI-16
Fase 10 VER-08 ─ MAN-05 ─ MAN-06 ─ MAN-07 (D-12), MAN-08 (D-13), MAN-09 (D-14)
UI-17 (D-15) después de UI-07
```

### UI-17 · Efecto de sorpresa por calidad
- **CERRADA sin código (2026-09-27, `/luz-verde`):** D-15 se resolvió dentro del rediseño visual (fase 2c: UI-21, UI-22 y UI-23). El tablero principal visual queda en `PARA_DESPUES.md`, tema 3.
- **Dueño:** Builder_UI · **Espera:** **D-15**, UI-07 · **Archivos:** `web/nivel1/nivel1.css`, `web/nivel1/nivel1.js`, `tests/ui/test_ui17_sorpresa.py`, `evidencia/UI-17/`
- **Entregable:** según D-15. Si es B: transición suave de la conclusión y un acabado cuidado de relieve y hundido, que respete `prefers-reduced-motion`. No agrega información ni actividad.
- **Prueba:** `pytest tests/ui/test_ui17_sorpresa.py`: con `prefers-reduced-motion: reduce` no hay animación; la jerarquía de UI-04 sigue igual (se repite la prueba de `font-size`).
- **Commit:** `UI-17: acabado de la conclusión del nivel 1`

---

## Lo que este plan deja fuera a propósito

Sale del handshake, "Fuera de alcance por ahora", y del criterio de frontera: administración de personal, gestión completa de las ~70 personas, cobranza automatizada, contacto con inquilinos, integración con ZKTeco y otras integraciones físicas. Tampoco se incluyen la capa de análisis de patrones de pago (ver D-15, C) ni restricciones por campo, que el handshake deja para cuando se conozcan los datos reales. Sobre ZKTeco, solo como nota para después y sin tareas: PullSDK está documentado solo para Windows (R2, H18 y H19; vacío V1), así que en su momento necesitará una pieza en Windows o equivalente. La interfaz `FuenteDatos` no cierra esa puerta.
