# Decisiones pendientes · Dashboard de Vania + Works

Etapa: 03 · Mapping. Fecha: 2026-09-23. Estado: **borrador para revisión de la sesión maestra y del usuario**.

Este archivo **no decide nada**. Cada punto expone alternativas y consecuencias. Donde aparece "Propuesta del planificador", es solo eso: una propuesta que tú puedes aceptar, cambiar o rechazar. Mientras una D-x no tenga respuesta, las tareas que bloquea se quedan en espera y los agentes pasan a la siguiente tarea disponible.

Fuentes: `handshake_vania_dashboard.md` (fuente de verdad), `SCAVENGE-Vania-Dashboard.md` (con sus notas N1 a N5), `siguientes_pasos.md`.

## Cómo responder

Basta una línea por decisión, en texto plano. Ejemplos:

```text
D-1: A
D-4: A, pero sin ícono en la pantalla de inicio por ahora
D-8: propuesta del planificador
```

La sesión maestra copia tu respuesta a la sección "Respuestas" al final de este archivo y libera las tareas.

## Resumen

| D | Tema | Bloquea directamente | Urgencia |
|---|---|---|---|
| D-1 | Stack del frontend y pruebas de UI | UI-01, UI-03 (y por dependencia casi toda la UI) | **Primera** |
| D-2 | Stack del backend y pruebas | DAT-01, DAT-02 (y por dependencia casi todo el backend) | **Primera** |
| D-3 | Dónde vive la lógica del estado de atención | DAT-07, DAT-08, INT-05, INT-06 | Alta |
| D-4 | Cómo entran al Dashboard (acceso mínimo) | INT-13, INT-14, INT-16 | Alta, antes de datos reales |
| D-5 | Roles `Admin` / `Editor` en la primera versión | INT-15 | Media |
| D-6 | Qué documento produce la capacidad heroica y qué puede imprimirse | INT-10, INT-11 | Al llegar el Excel |
| D-7 | Ruta técnica hacia la HP Smart Tank | INT-09, INT-11, MAN-04 | Media, requiere tu dato U-3 |
| D-8 | Rastro de Vania: cómo se ve, dónde va y cómo se ven las correcciones | UI-14 | Media |
| D-9 | Cómo pasa el contexto del Dashboard a la conversación con Vania | INT-08 | Media |
| D-10 | Pizarrón: datos mínimos de personas y fuente de efemérides | DAT-13, INT-12 | Baja, depende del Excel |
| D-11 | Cómo se reducen o silencian los avisos | INT-07 | Media |
| D-12 | Respaldo y persistencia durante la prueba | MAN-07 | Antes del despliegue |
| D-13 | Límites de uso durante la prueba | MAN-08 | Antes de abrir la prueba, requiere U-2 |
| D-14 | Cómo se observará la señal de adopción de Grecia | MAN-09 | Antes de abrir la prueba |
| D-15 | Cómo se produce la sorpresa en un Dashboard que tiende a la calma | UI-17 | Baja |

Las tareas que dependen de otra tarea bloqueada también esperan. La lista completa por tarea está en `plan/PLAN.md`.

---

## D-1 · Stack del frontend y pruebas de UI

**Qué está fijo.** Dashboard propio, con libertad total sobre HTML, CSS y JavaScript. Apache ECharts solo si una visualización realmente lo necesita. Mobile-first, funcionando también en escritorio. (Handshake, "Técnicas" y "Dirección visual".)

**Qué falta.** El handshake no fija si hay framework, paso de compilación ni herramienta de pruebas para la interfaz.

**Alternativas**

- **A · HTML, CSS y JavaScript sin framework ni compilación** (módulos ES nativos), servidos por FastAPI como archivos estáticos.
  - Sin Node ni paso de build: el despliegue en el VPS es copiar archivos.
  - Control total del neumorphism y de cada sombra.
  - El Builder escribe a mano el ruteo y el manejo de formularios. Son pocas pantallas (nivel 1, nivel 2, cuatro áreas de detalle, rastro, acceso), así que el costo es bajo.
  - La propiedad de archivos entre agentes queda limpia: `web/` es de Builder_UI y no toca Python.
- **B · HTML generado por el servidor (plantillas Jinja en FastAPI) + htmx o Alpine.js.**
  - Menos JavaScript para formularios y actualizaciones parciales.
  - Las plantillas viven dentro del servicio Python: Builder_UI y Builder_Datos terminan tocando las mismas carpetas, y aumenta el riesgo de choques entre sesiones.
  - Facilita que lógica de interpretación se cuele en las plantillas, lo que choca con "un solo cerebro, dos superficies".
- **C · Framework con compilación** (por ejemplo Svelte con Vite).
  - Componentes y reactividad cómodos.
  - Agrega Node, dependencias y un paso de build al despliegue. Eso es más trabajo MANUAL en el VPS y en una eventual migración al servidor de David.

**Pruebas de UI (aplica a cualquier opción).**
- **Playwright desde pytest**, con viewport de teléfono (390×844) y de escritorio (1280×800), capturas guardadas en `evidencia/`. Permite pruebas concretas: qué elemento tiene la mayor jerarquía, que no haya scroll horizontal, que el estado presionado cambie algo más que la sombra. Un agente Haiku puede correrlas.
- Sin herramienta: solo revisión manual. No es verificable por el Verificador.

**Propuesta del planificador:** A + Playwright desde pytest. Menos piezas, despliegue simple y propiedad de archivos limpia.

**Bloquea:** UI-01, UI-03 y, por dependencia, UI-04 a UI-17 e INT-14. UI-02 no espera esta decisión.

---

## D-2 · Stack del backend y pruebas

**Qué está fijo.** `Vania → FastAPI → SQLite` y `Dashboard → FastAPI → SQLite`. FastAPI es la única capa que toca SQLite. Desarrollo local primero, con portabilidad.

**Qué falta.** Cómo se accede a SQLite, cómo se versiona el esquema, cómo se gestionan dependencias y con qué se prueba.

**Alternativas de acceso a datos**

- **A · `sqlite3` de la biblioteca estándar + SQL escrito a mano + migraciones `.sql` numeradas.**
  - Cero dependencias para la base; el esquema se lee directamente en los archivos.
  - Se puede asignar desde ahora un número de migración a cada tarea (ver PLAN), así que dos agentes nunca generan la misma migración.
  - Un poco más de código repetido en el CRUD.
- **B · SQLModel o SQLAlchemy + Alembic.**
  - Menos código de CRUD y validación integrada con Pydantic.
  - Alembic lleva un historial lineal de revisiones: si dos agentes generan migraciones al mismo tiempo, el historial se bifurca y hay que reconciliarlo a mano.
  - Una dependencia más en el VPS y en la migración futura.

**Dependencias:** `pip` + `venv` con versiones fijadas (disponible en cualquier servidor) o `uv` (más rápido, pero hay que instalarlo en el VPS).

**Pruebas:** `pytest` con el `TestClient` de FastAPI. No se ve alternativa razonable; se incluye para que quede explícito.

**Versión de Python:** la que tenga el VPS. Es un dato tuyo (U-6).

**Propuesta del planificador:** A + `pip`/`venv` + `pytest`. Encaja con agentes en paralelo y con portabilidad.

**Bloquea:** DAT-01 y DAT-02 y, por dependencia, casi todo el backend (DAT-04 en adelante, todas las INT). DAT-03 no espera esta decisión.

---

## D-3 · Dónde vive la lógica que interpreta el estado de atención

**Qué está fijo.** "El Dashboard y Vania deben reflejar el mismo estado de Works y compartir una lógica coherente." FastAPI es la única capa con acceso directo a SQLite, pero eso **no implica** que FastAPI sea quien interpreta. El handshake pide al planificador proponer y justificar la ubicación.

**Alternativas**

- **A · Módulo de dominio en Python puro** (`app/estado/`), sin depender de FastAPI ni de SQLite. Recibe los datos ya leídos y devuelve el estado (conclusión, asuntos, indicadores) con frases humanas. FastAPI lo invoca y lo expone en `/api/estado`. Vania consume ese mismo endpoint y el de avisos.
  - Una sola interpretación para las dos superficies.
  - Determinista: se prueba sin red, sin modelo de lenguaje y sin costo de tokens.
  - Si mañana lo necesita otro proceso, el módulo se reutiliza tal cual.
  - Vania solo repite las frases del módulo; su voz en WhatsApp queda limitada a esas frases.
- **B · Vania interpreta** (en Hermes, con su modelo) y escribe su conclusión en la API. El Dashboard muestra lo que Vania concluyó.
  - La conclusión "suena" a Vania.
  - Depende de un modelo de lenguaje: no es determinista, cuesta tokens y puede equivocarse. El handshake anota como riesgo conocido que "un error de Vania que nadie note puede costar más que la ausencia de la función".
  - Si Vania falla o no corre, el Dashboard no tiene estado.
  - La lógica vive en Hermes, que es privado y está fuera de este repositorio, así que aquí no se puede probar.
- **C · Híbrido.** Las reglas deterministas de A deciden **qué** merece atención y en qué orden. El Dashboard usa las frases del módulo. Vania recibe los mismos asuntos estructurados y los **redacta con su voz** para WhatsApp.
  - Mismos hechos en las dos superficies; redacción distinta pero coherente.
  - La redacción de WhatsApp vive en Hermes (MANUAL).
- **D · Cálculo en el navegador** (JavaScript del Dashboard).
  - Rompe "un solo cerebro": Vania no puede usarlo. Se lista solo para descartarla de forma explícita.

**Propuesta del planificador:** A como base, que permite C sin cambiar nada de este repositorio. El módulo entrega los asuntos estructurados **y** una frase sugerida; Vania decide si la usa tal cual o la redacta.

**Bloquea:** DAT-07, DAT-08, INT-05, INT-06 y, por dependencia, UI-07, MAN-01 y MAN-02. Mientras tanto, UI-04 a UI-06 avanzan con los ejemplos del contrato (DAT-03), que no dependen de esta decisión.

---

## D-4 · Cómo entran al Dashboard

**Qué está fijo.** Tiene que haber control de acceso antes de usar datos reales, y conocer la URL no basta como protección. Entrar debe ser **extremadamente sencillo** y no depender de que el desarrollador los guíe. El usuario **declinó elegir** en el handshake y no dejó opción por defecto.

**Hechos útiles del Scavenge (R4)**, con sus notas: las fricciones de "sesión de larga duración" y "PIN local" son **vacíos** (N2), y el PIN local, One-Tap y Zero-Tap dependen de una app nativa, así que no se dan por disponibles en un Dashboard web (N3).

**Alternativas**

- **A · Enlace de acceso que manda Vania por WhatsApp** (un solo uso, expira pronto) **+ sesión larga en ese teléfono.**
  - Usa el canal que David y Grecia ya usan. No hay nada que recordar.
  - Depende de cómo está hecho el WhatsApp de Vania (U-5). Si es la plataforma oficial de WhatsApp Business, Meta reserva las plantillas de autenticación para códigos, y un enlace tendría que ir como plantilla de utilidad (R4, V1). Si es otro tipo de puente, Vania lo manda como un mensaje normal. No hay fuente pública sobre riesgos específicos de enlaces enviados por WhatsApp (R4, V2).
  - NIST indica que las cookies de "recordar navegador" no deben sustituir la autenticación, salvo como reautenticación (R4). Una sesión larga es una concesión explícita a la baja fricción, y conviene que tú la aceptes sabiéndolo.
  - Riesgo: que el enlace se reenvíe. Se mitiga con un solo uso y expiración corta (R4, magic links).
  - Requiere HTTPS en el VPS (U-6).
- **B · Passkeys** (Face ID, huella).
  - Resistentes a phishing (R4).
  - El "día 2" es el problema: teléfono nuevo o perdido sin sincronización requiere una ruta de recuperación diseñada de antemano (R4). En la práctica, B necesita A u otra opción como respaldo.
  - Se reportan fallas en algunos Android que no son Pixel (R4).
  - Requiere dominio estable y HTTPS.
- **C · Iniciar sesión con Google.**
  - Baja fricción si ya tienen sesión de Google en el teléfono. No sabemos si David y Grecia la usan.
  - Depende de un proveedor externo y de registrar la aplicación en su consola.
- **D · Enlace por correo.**
  - Obliga a salir de WhatsApp al correo y volver. NIST no admite el correo como canal fuera de banda (R4). No sabemos si usan correo en el teléfono.
- **E · Código de un solo uso por SMS o por WhatsApp.**
  - Hay que copiar y pegar un código. NIST 800-63B-4 clasifica el SMS como autenticador restringido (R4).

**Complemento compatible con cualquiera:** ícono en la pantalla de inicio (PWA o acceso directo). RES-01 investiga si la sesión sobrevive en Safari de iOS y en una PWA instalada, que es justo el punto débil de A.

**Propuesta del planificador:** A + ícono en la pantalla de inicio, sujeto a que U-5 confirme que Vania puede mandar un enlace normal. Si U-5 dice que es la plataforma oficial de WhatsApp Business, conviene revisar A contra el costo y la aprobación de plantillas antes de decidir.

**Bloquea:** INT-13, INT-14, INT-16 y, por dependencia, INT-15, DAT-15, DAT-16, UI-16 y MAN-06. **Regla del plan:** ningún dato real entra al sistema antes de que INT-13 esté hecha.

---

## D-5 · Roles `Admin` / `Editor` en la primera versión

**Qué está fijo.** El control de acceso mínimo es requisito. Los roles son **condicionales**: se implementan "si resulta razonablemente sencillo", y no deben volverse un requisito que bloquee el proyecto. Si se implementan, David es `Admin` y Grecia es `Editor`: los dos ven lo mismo, y la única diferencia es quién administra cuentas. El acceso técnico del desarrollador es aparte.

**Alternativas**

- **A · Sin roles en la primera versión.** Dos cuentas equivalentes. El desarrollador administra cuentas con un comando en el servidor (INT-16).
  - Lo más simple.
  - Si David quisiera desactivar a Grecia, te lo pide a ti.
- **B · Roles como los describe el handshake.** Una pantalla mínima donde David puede desactivar o reactivar la cuenta de Grecia, y Grecia no puede tocar la de David.
  - Estimación del planificador: una vez resuelta D-4, cuesta una tarea pequeña (INT-15) y una pantalla sencilla.
  - Más superficie de prueba.

**Propuesta del planificador:** B, porque con A o B de D-4 resulta razonablemente sencillo. Si D-4 termina siendo una opción más pesada, conviene A.

**Bloquea:** INT-15.

---

## D-6 · Qué documento produce la capacidad heroica y qué puede imprimirse

**Qué está fijo.** La apuesta es: datos reales → comprensión → resultado útil → acción física. No se fija que sea un reporte de pagos. El handshake dice que **se decidirá cuando existan los datos reales**. No se asume que todo dato pueda imprimirse.

**Candidatos de documento** (ninguno es requisito):
- Lo que merece atención hoy o esta semana, en frases humanas: el mismo estado del Dashboard, en papel.
- Estado de cobranza del mes.
- Contratos que se acercan a una fecha de revisión.
- Ficha de una oficina o de un inquilino.

**Consecuencias para comparar:**
- Algunos candidatos necesitan historial de pagos, y no sabemos si el Excel lo tiene (P1).
- Imprimir montos o nombres deja papel en la oficina a la vista de otras personas.
- El que más se parece al Dashboard refuerza "un solo cerebro", pero puede sorprender menos.

**Alternativas para "qué puede imprimirse":**
- **A · Lista blanca de tipos de documento.** Vania solo puede imprimir los tipos definidos.
- **B · Cualquier cosa, con confirmación** antes de mandar.
- **C · Lista blanca + confirmación.**

**Propuesta del planificador:** elegir el documento cuando llegue el Excel, como dice el handshake. Mientras tanto, INT-09 construye la tubería con un documento de prueba sintético. Para imprimir, A: la lista blanca es la forma más simple de cumplir "no se asume que todo dato puede imprimirse".

**Bloquea:** INT-10, INT-11.

---

## D-7 · Ruta técnica hacia la HP Smart Tank

**Hechos.** La integración de impresión ya funciona en Hermes y es privada; aquí no se supone cómo está hecha. En Ubuntu 24.04 la impresora se vinculó por IPP, con el driver detectado como IPP Everywhere (R1, H10; la certificación pública no está confirmada, R1, V1). El lenguaje nativo documentado es HP PCL 3 GUI (R1, H1). La impresora está en la oficina de Works y la prueba corre en tu VPS. **Ningún documento explica cómo llega hoy un trabajo desde el servidor a la impresora** (U-3).

**Alternativas**

- **A · Reutilizar la integración de Hermes.** Este repositorio solo **genera el documento** (un archivo) y lo expone por la API. Vania, desde Hermes, lo manda a imprimir con la herramienta que ya existe.
  - No se duplica una integración que ya funciona.
  - Este repositorio no toca la red de la oficina.
  - Depende de qué formato recibe esa herramienta y cómo recibe el archivo (U-3).
- **B · FastAPI imprime directo por IPP.**
  - Requiere que el VPS alcance la red de la oficina (túnel o VPN). Eso es infraestructura nueva y duplica lo que Hermes ya hace.
- **C · Un pequeño agente de impresión en la oficina** que recoge trabajos pendientes.
  - Es una pieza física nueva en Works. Por el criterio de frontera del handshake, probablemente pertenece a una fase posterior.

**Propuesta del planificador:** A.

**Lo que necesito de ti (U-3):** qué formato acepta hoy la herramienta de impresión de Hermes (PDF, imagen u otro), cómo recibe el archivo (ruta local, URL o contenido) y desde qué máquina sale hoy el trabajo hacia la impresora.

**Bloquea:** INT-09, INT-11, MAN-04 y, por dependencia, INT-10 e INT-12.

---

## D-8 · Rastro de Vania: cómo se ve, dónde va y cómo se ven las correcciones

**Qué está fijo.** El Dashboard debe permitir percibir la actividad de Vania. Sin eso, se construye "una base de datos bonita". No se fabrica actividad ni se usa para atraer visitas. El handshake la ubica en la jerarquía debajo de los indicadores.

**Observaciones que el handshake mandó a esta etapa:** el boceto muestra un contador ("3 movimientos registrados hoy"), que conviene revisar contra "no des la hora si no te la piden"; y falta el tratamiento visual de las correcciones humanas sobre acciones de Vania.

**Alternativas de representación**

- **A · Bitácora discreta en frases**, debajo de lo que merece atención: "Vania registró el pago de la oficina 204 · hoy, 10:12". Muestra solo las más recientes, con un "ver todo".
  - Visible sin gritar. Ocupa un lugar fijo aunque no haya nada nuevo.
- **B · Marca en cada registro del detalle** ("registrado por Vania") + sección propia en el nivel 3.
  - Muy tranquila, pero el rastro casi no se ve. Riesgo alto de "base de datos bonita".
- **C · Una línea en el nivel 1 solo cuando hubo actividad relevante** desde la última visita ("Vania registró 2 pagos desde ayer"), que abre la bitácora.
  - Máxima visibilidad cuando hay algo y silencio cuando no.
  - Requiere saber cuándo fue la última visita de cada persona, lo que depende de D-4.
  - Si se usa de más, se siente como el contador de engagement que el handshake quiere evitar.

**El contador del boceto:** quitarlo, mantenerlo, o mostrarlo solo cuando hay actividad real (que es C).

**Correcciones humanas**
- (i) La entrada de Vania queda y debajo aparece "Grecia lo corrigió: …".
- (ii) La entrada de Vania se marca como corregida y muestra el valor nuevo.
- (iii) Sin tratamiento especial: la corrección aparece como una entrada más.

**Propuesta del planificador:** A, sin contador, + corrección (i). Muestra lo que Vania hace sin llamar la atención y deja visible que las personas conservan el control.

**Bloquea:** UI-14. La tabla de actividad y su API (INT-01 a INT-03) no esperan esta decisión.

---

## D-9 · Cómo pasa el contexto del Dashboard a la conversación con Vania

**Qué está fijo.** Desde un elemento del Dashboard debe poder seguirse la conversación con Vania sobre ese mismo contexto, sin empezar de cero. No hay chat duplicado dentro del Dashboard.

**Alternativas**

- **A · Enlace `wa.me` al número de Vania con texto prellenado** ("Sobre esto: la oficina 204 vence en 12 días").
  - Lo más simple. No requiere cambios en Hermes.
  - La persona tiene que tocar "enviar". El contexto viaja como texto visible, y eso también le sirve a ella.
  - Depende del número de Vania (U-5) y del comportamiento documentado de estos enlaces (RES-02).
- **B · Enlace `wa.me` con un código corto** ("Sobre #A7F3") + un endpoint para que Vania traduzca el código al registro exacto.
  - Vania recibe una referencia precisa a los datos.
  - Requiere una herramienta nueva en Hermes (MANUAL) y una tabla de contextos (migración 007).
- **C · "Contexto pendiente" guardado en la API por persona.** Cuando esa persona le escriba, Vania lo lee.
  - No hay texto extra, pero es invisible: la persona no sabe si Vania "ya sabe". Es ambiguo si luego escribe de otra cosa.

**Propuesta del planificador:** A. B solo si A se queda corto en la práctica.

**Bloquea:** INT-08 y, por dependencia, UI-15.

---

## D-10 · Pizarrón mensual: datos mínimos de personas y fuente de efemérides

**Qué está fijo.** El pizarrón está dentro del alcance, **condicionado** a que los datos existan o se puedan capturar. Toca el modelo de datos de forma limitada. No debe convertirse en un sistema de gestión de comunidad. No se sabe si el Excel tiene fechas de nacimiento (P2).

**Datos mínimos por persona**
- **A ·** Nombre para mostrar + día y mes de cumpleaños (sin año) + a qué inquilino pertenece (opcional).
- **B ·** A + una marca de que la persona acepta aparecer en el pizarrón. Son empleados de los inquilinos, o sea terceros.

**Si el Excel no trae esos datos**
- Grecia los captura en el Dashboard: se agregaría una tarea UI pequeña.
- Grecia se los dicta a Vania por WhatsApp.
- La función espera hasta que existan.

**Efemérides**
- Fuente pública (RES-03 investiga cuáles hay).
- Lista que Grecia mantiene.
- Las dos.

**Propuesta del planificador:** A. Captura por Vania si el Excel no los trae, porque no agrega pantallas. Efemérides de fuente pública con la posibilidad de que Grecia agregue las suyas.

**Bloquea:** DAT-13, INT-12.

---

## D-11 · Cómo se reducen o silencian los avisos

**Qué está fijo.** La proactividad debe ser útil, limitada y controlable. No hay tope artificial de mensajes por día. Vania agrupa en un solo mensaje, y si no hay nada, no escribe. El handshake no decide cómo se configura.

**Alternativas de configuración**
- **A · Por conversación:** "Vania, ya no me avises de X". Vania guarda la preferencia en la API (persona, tipo de evento, hasta cuándo).
- **B ·** A + una pantalla de ajustes en el Dashboard.
- **C ·** Solo el desarrollador la cambia, a petición.

**Consecuencia relacionada que el handshake no fija: la repetición.** Si un asunto sigue abierto, ¿Vania lo vuelve a avisar?
- (i) Una sola vez por asunto, hasta que cambie.
- (ii) Recordatorio si sigue abierto después de cierto tiempo.
- (iii) En cada revisión. Probablemente se vuelve ruido.

**Propuesta del planificador:** A + (i). Respeta "relevancia antes que frecuencia" y no agrega pantallas.

**Bloquea:** INT-07. MAN-02 puede empezar sin esta decisión, pero queda incompleta hasta tenerla.

---

## D-12 · Respaldo y persistencia durante la prueba

**Qué está fijo.** El handshake dice que las garantías de persistencia y respaldo "se definen en planificación". También dice que no se escriban garantías que nadie acordó. Por eso esto es una decisión tuya y no una regla del plan.

**Alternativas**
- **A ·** Copia diaria del SQLite en el VPS (copia en caliente con `sqlite3 .backup`), guardando entre 7 y 14 días.
- **B ·** A + copia fuera del VPS, por ejemplo a tu máquina.
- **C ·** Solo los snapshots del proveedor del VPS, si existen.
- **D ·** Nada adicional durante la semana de prueba.

**Consecuencia:** el handshake anota como riesgo que un error de Vania pase desapercibido. Con un respaldo, más la bitácora de actividad, se puede reconstruir qué pasó y volver atrás.

**Bloquea:** MAN-07.

---

## D-13 · Límites de uso durante la prueba

**Qué está fijo.** Habrá límites razonables. La cifra se estima con tu consumo real de Codex/OpenAI (P5), que sigue sin dato (U-2).

**Alternativas**
- **A ·** Tope diario de mensajes a Vania por persona.
- **B ·** Tope mensual de tokens.
- **C ·** Sin tope técnico, solo monitoreo tuyo durante la semana.

Dónde se aplica: casi seguramente en Hermes, así que sería trabajo MANUAL.

**Bloquea:** MAN-08. No bloquea la construcción.

---

## D-14 · Cómo se observará la señal de adopción de Grecia

**Qué está fijo.** La señal es: "cuando aparece una necesidad real que Vania o el Dashboard pueden resolver, Grecia recurre a ellos por iniciativa propia". **No se mide uso diario**: ni sesiones, ni aperturas, ni rachas. El handshake manda esto a planificación.

**Alternativas**
- **A ·** Conversación corta con Grecia al cierre de la semana: "¿cuándo acudiste a Vania o al Dashboard, y cuándo volviste a hacerlo como antes?".
- **B ·** A + revisión de la bitácora de actividad (quién hizo cada cambio: Vania, el Dashboard o el sistema) para ubicar casos concretos. No se agregan métricas nuevas; la bitácora ya existe por el rastro de Vania.
- **C ·** Solo tu impresión cualitativa.

**Consecuencia:** una semana que caiga en un tramo tranquilo del mes puede dar poca señal sin que eso signifique que el producto falló (riesgo anotado en el handshake). B ayuda a distinguir "no hubo necesidad" de "hubo necesidad y no la usaron".

**Propuesta del planificador:** B.

**Bloquea:** MAN-09. No bloquea la construcción.

---

## D-15 · Cómo se produce la sorpresa en un Dashboard que tiende a la calma

**Qué está fijo.** El Dashboard debe ser útil, fácil, visualmente deseable y capaz de revelar posibilidades. Tiende a la calma: no fabrica actividad. La apuesta declarada de impacto es la capacidad heroica.

**Alternativas**
- **A ·** La sorpresa vive fuera del Dashboard: en la capacidad heroica y en los avisos. El Dashboard solo asegura calma y cuidado visual.
- **B ·** Sorpresa por calidad, no por cantidad: la conclusión aparece con una transición suave, los controles sobresalen y se hunden de forma convincente, y hay detalles de acabado.
- **C ·** Un hallazgo que no sabían que querían saber, por ejemplo un patrón de puntualidad, cuando los datos lo permitan.
  - Depende del historial de pagos (P1).
  - La "capa de análisis" no aparece en la lista de alcance de la primera versión, así que C la ampliaría. Por la regla del grilling, necesitaría tu decisión expresa.

**Propuesta del planificador:** B ahora. C, si acaso, después de ver el Excel y como decisión aparte.

**Bloquea:** UI-17.

---

## Vacíos que solo tú puedes aportar

No son decisiones: son datos que ningún agente puede investigar. Pueden cambiar el alcance de algunas tareas.

| U | Qué falta | Por qué importa | Afecta |
|---|---|---|---|
| U-1 | El Excel de Works: columnas, completitud, historial de pagos (P1), fechas de nacimiento (P2) | Todo el tramo de datos reales. Nada del plan se basa en su contenido | Fase 9, D-6, D-10 |
| U-2 | Consumo real de referencia de Codex/OpenAI (P5) | Base acordada para los límites de uso | D-13, MAN-08 |
| U-3 | Cómo funciona hoy la impresión desde Hermes: formato que acepta, cómo recibe el archivo, desde qué máquina y red sale el trabajo | La capacidad heroica termina ahí | D-7, INT-09, MAN-04 |
| U-4 | Dónde corre Hermes respecto al servicio FastAPI (mismo VPS u otra máquina) y cómo se le agregan herramientas a Vania | Cómo llama Vania a la API y con qué credencial | INT-04, INT-05, MAN-01 |
| U-5 | De qué tipo es el WhatsApp de Vania (plataforma oficial de WhatsApp Business o un puente de otro tipo) y cuál es su número | Cambia qué opciones de acceso y de contexto aplican; R4 describe la plataforma oficial | D-4, D-9 |
| U-6 | VPS: dominio y HTTPS disponibles, versión de Python, proxy inverso existente, cómo se administran servicios | Despliegue; passkeys y cookies seguras requieren HTTPS | D-2, D-4, MAN-05, MAN-06 |

---

## Respuestas

La sesión maestra anota aquí cada respuesta del usuario, con fecha, y actualiza las tareas afectadas en `plan/PLAN.md` y en los archivos de estado.

- **2026-09-23 · D-1: A + Playwright desde pytest** (propuesta del planificador). El usuario delegó la decisión en la sesión maestra.
- **2026-09-23 · D-2: A + `pip`/`venv` + `pytest`** (propuesta del planificador). Delegada en la sesión maestra. Versión de Python mínima: **3.10**, para no depender de la versión del VPS (U-6 sigue abierto). En local hay 3.13.
- **2026-09-23 · D-3: A, que permite C** (propuesta del planificador). Delegada en la sesión maestra. Motivo: una sola interpretación determinista y comprobable sin gastar tokens; Vania puede redactar con su voz a partir de los mismos asuntos.
- **2026-09-23 · Corrección de proceso (revisión de la sesión maestra, aprobada por el usuario):** cada commit nombra sus rutas (`git commit -m "…" -- <rutas>`), para que un agente no arrastre archivos preparados por otro.
- **2026-09-26 · D-4: link de un solo uso que manda Vania, más sesión diaria.** Decidida por el usuario. El link vence a los 10 minutos, se usa una sola vez y Vania lo manda solo cuando la persona lo pide. Hay una sesión por dispositivo y vence a las 18:00 de Querétaro, o a las 23:59 si se creó después de las 18:00. Sin ícono en la pantalla de inicio. Vania reconoce a la persona por su número de WhatsApp; los números no van en git. Detalle: `plan/REGLAS_OPERACION.md`. Ajustados INT-13, INT-14 e INT-16.
- **2026-09-26 · D-5: sin roles.** David y Grecia tienen las mismas reglas. Solo el desarrollador activa o desactiva cuentas (INT-16). INT-15 queda cancelada.
- **2026-09-26 · Reglas de operación (nuevas):** pre-registro con confirmación Sí/No, pendientes durante 24 h, historial con valor anterior y nuevo, solicitante y ejecutor, duplicados con criterios aprobados, Vania solo escribe con la sesión de quien lo pide (confirmación por texto Sí/No, porque es WhatsApp Web), reporte del día con observaciones opcionales, y borrar también requiere confirmación. Texto completo en `plan/REGLAS_OPERACION.md`. Se agregan la fase 2b (DAT-17 a DAT-21, INT-17, UI-18 a UI-20, MAN-10, VER-09) y el requisito de que no arranque sin el `/luz-verde` del usuario.
- **2026-09-26 · VER-02: opción B.** Una sola función de conexión en `app/db/`. Es DAT-17.
- **2026-09-26 · Acento terracota `#A8501F` aprobado** (propuesta de VER-01).
- **2026-09-26 · `origen_dato` en VER-03:** las cuatro áreas usan `manual` y `actividad` usa `real`, como está construido. No es una falla. Queda documentado en VER-03.
- **2026-09-26 · Agentes en Codex:** Builder_1 (verificación y revisión), Builder_Datos, Builder_Integraciones y Builder_UI corren en Codex. Siguen el mismo protocolo de `REANUDAR.md`.
- **2026-09-26 · `/luz-verde` del usuario:** se autorizan los commits de VER-03 y del plan, y arrancan Builder_Datos y Builder_Integraciones con la fase 2b. Builder_UI arranca cuando lleguen sus dependencias.
- **2026-09-26 · Corrección del plan (`/luz-verde`):** INT-13 puede tocar además `app/actividad/registrar.py`, `tests/conftest.py` y `tests/ui/conftest.py`. En Codex los commits los hace la sesión Commit-Codex, una tarea por vuelta.
- **2026-09-26 · Corrección del plan (`/luz-verde`):** INT-16 puede tocar `app/seguridad/sesion.py`.
- **2026-09-26 · D-7: A.** El usuario delegó la decisión en la sesión maestra, pidiendo la más limpia y la que menos gente necesite. El Dashboard solo genera el PDF; Vania lo imprime con la herramienta que ya tiene en Hermes. Pendientes prácticos (no bloquean el código): reservar la IP de la impresora (`192.168.1.176`, IPP, PDF) en el router y definir qué equipo de la oficina queda encendido. Detalle: `vinculacion-hp-smart-tank-750-ubuntu.md`. Es de las funciones que más van a impresionar a David.
- **2026-09-26 · D-6: el documento se elige cuando llegue el Excel.** Mientras tanto, documento de prueba. Vania solo imprime los tipos aprobados (A).
- **2026-09-26 · D-8: el Reporte del día cubre el rastro de Vania** (columna Ejecutor, DAT-21 y UI-20). No se hace una bitácora aparte.
- **2026-09-27 · Corrección del plan (`/luz-verde`):** UI-14 se cierra sin código; el Reporte del día ya es el rastro de Vania (D-8).
- **2026-09-26 · D-9: A.** Botón junto al dato que abre WhatsApp con Vania y el mensaje ya escrito.
- **2026-09-26 · D-10: se queda en el plan, pero nunca bloquea nada y no se le dedica tiempo ahora.** Es para Grecia: cumpleaños de las ~70 personas de los 19 inquilinos y efemérides del mes, para su pizarrón de la oficina.
- **2026-09-26 · D-11: A + (i).** Vania sí escribe por su cuenta, sin que le pregunten, pero sin atosigar: cada asunto una sola vez, y se apaga pidiéndoselo por WhatsApp.
- **2026-09-26 · D-15: se resuelve dentro del rediseño visual** (`plan/PARA_DESPUES.md`, tema 1).
- **2026-09-26 · Rediseño visual (`/luz-verde`):** la fuente de verdad es `plan/rediseno/DASHBOARD_DESIGN_SPEC.md`. Solo cambia el aspecto; la funcionalidad queda igual. El acento pasa de terracota `#A8501F` a azul `#0A66D9`, como dice el documento. Inter y Lucide se guardan dentro del proyecto, sin CDN. Se hace en tres tareas: UI-21 (base, Builder_UI) y después UI-22 y UI-23 en paralelo (Builder_UI_2 y Builder_UI_3). Builder_UI_2 puede tocar el aspecto de `web/acceso/` (solo `acceso.css` e `index.html`).
- **2026-09-26 · Grises del rediseño:** texto principal en azul carbón `#202734`; texto secundario y notas chicas en gris pizarra `#596575`; el gris tenue `#7B8794` solo en íconos secundarios, bordes, separadores y adornos, nunca en texto (daba un contraste de 3.2). Verde, ámbar y rojo, solo para estados. El azul es el protagonista.
