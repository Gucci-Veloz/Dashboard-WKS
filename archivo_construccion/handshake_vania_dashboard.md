# Handshake · Vania y el Dashboard de Works

Status: complete, grilled · 2026-09-20

Modo: idea nueva. El directorio del proyecto está vacío, no hay código previo que consultar.
Todo lo que se escriba aquí viene del usuario, no del repositorio.

## Cómo leer este documento
Este documento alimentará investigación y planificación, así que distingue cuatro cosas que no deben confundirse:

- **Hecho actual**: algo que ya existe o está confirmado hoy.
- **Decisión**: algo que el usuario ya eligió, para la primera versión o para una etapa posterior.
- **Objetivo o hipótesis**: algo que se busca provocar o comprobar, cuyo resultado todavía no se conoce.
- **Pendiente**: algo que no está decidido, o que dependerá de información que todavía no se tiene.

Las decisiones no son todas del mismo tipo, y el documento conserva la diferencia:
- **Decisión de diseño**: el estilo neumorphism y la paleta perla, blanco, crema y gris claro.
- **Decisión de producto y canal**: WhatsApp como vía principal de acceso a Vania.
- **Hipótesis de impacto, a validar en la experiencia real**: la capacidad heroica, es decir que Vania use información real de Works y materialice un resultado en la HP Smart Tank.

Las etiquetas no aparecen en cada línea, pero la redacción sí conserva la diferencia. Si una frase describe una capacidad en presente, esa capacidad ya existe hoy. Si describe algo que se va a construir, está escrita como capacidad buscada o alcance decidido.

**Advertencia sobre los datos:** el Excel real de Works todavía no está disponible. Las categorías y campos que aparecen aquí sirven para definir la idea y **deberán contrastarse con los datos reales**. Toda función que dependa de información cuya existencia aún no está confirmada queda condicionada a que esa información exista o pueda obtenerse.

## La idea en palabras simples
Esta es la lectura que el usuario confirmó. Va literal.

David es dueño de un lugar donde se rentan oficinas y espacios de trabajo. Se llama Works. El edificio es de su papá, Don Fernando, que además es su socio. Grecia es la encargada y le ayuda con el día a día. Hay como 21 personas o empresas que tienen algo rentado. Si cuentas también a los empleados de ellos, la comunidad que usa Works llega a unas 70 personas.

La información administrativa relevante que se ha discutido, la de oficinas, inquilinos, contratos y pagos, se lleva hoy en una hoja de Excel. Esa hoja sí la usan, aunque puede estar desactualizada. El problema no es que el trabajo sea difícil. El trabajo es sencillo. El problema es que la herramienta es muy básica, y ellos no son personas de tecnología. Muchas tareas dependen de que Grecia las anote y les dé seguimiento a mano. Eso trae el riesgo de que algo se olvide o quede incompleto, aunque nadie ha contado un caso concreto.

Hoy no usan esa información para sacar conclusiones. Cosas como quién paga siempre a tiempo, quién se atrasa seguido, o qué se repite mes con mes. Eso no se está haciendo.

El usuario está haciendo a Vania. Vania es una ayudante a la que David y Grecia van a poder hablarle por WhatsApp, como a una persona. WhatsApp es solo la puerta por donde entran; Vania no vive ahí dentro.

Vania ya existe hoy. Ya es un perfil aparte dentro de Hermes y ya contesta por WhatsApp. Los teléfonos de David y Grecia ya están dados de alta. Lo que falta es especializarla para Works y conectarla con los datos reales, y hacerle su pantalla.

Esa pantalla se va a llamar Dashboard y todavía no existe. Cuando esté, la van a abrir en el teléfono. Lo primero que deberán ver no es un número ni una gráfica, sino una frase que les diga cómo está todo. Si no hay nada que de verdad necesite atención, la pantalla debe transmitir calma, dicho como lo diría una persona, sin llenarse de cosas para aparentar que pasa algo. Si sí hay algo, debe decir cuántas cosas necesitan atención y contarlas con palabras normales, como "a la oficina 204 se le acaba el contrato en 12 días". Si quieren ver más, que puedan entrar al detalle, pero que el detalle no les salte encima.

A propósito no va a haber un número principal. Todavía nadie sabe cuál sería el importante para David, así que no se inventa uno. Si más adelante aparece, entonces podrá subir de lugar.

En esa pantalla no solo van a mirar. También deberán poder cambiar cosas y guardarlas ellos mismos. Eso es a propósito: sirve para que conserven el control, para bajar la incertidumbre, y para que David o Grecia puedan comprobar o corregir algo directamente cuando lo necesiten.

La pantalla también deberá mostrar lo que Vania hizo. Porque Vania trabaja sin que la vean, y si su trabajo no se ve, parece que no hace nada. Todavía no se decide cómo se va a ver eso, solo que tiene que estar.

Vania también deberá poder escribir primero, sin que nadie le pregunte, cuando de verdad haya algo importante. Si hay varias cosas, que las junte en un solo mensaje. Si no hay nada, que no escriba. Y si sus avisos llegaran a molestar, ellos deberán poder decirle que le baje. Esa proactividad específica para Works todavía no está implementada ni configurada.

Lo que se vea en la pantalla y lo que avise por WhatsApp deben salir de la misma idea de cómo está Works, y no decir cosas distintas.

La apuesta más fuerte es ésta: que Vania pueda tomar la información real de Works, entenderla, hacer algo útil con ella, y mandarlo a imprimir a la impresora de la oficina. Que salga en papel. No es el truco de imprimir, que David ya vio una vez. La intención es que el papel sea la prueba de que Vania entendió lo que estaba pasando. Si eso de verdad lo impresiona, no se sabe. Para eso es la prueba.

Vania también deberá ayudarle a Grecia con el pizarrón de cada mes, el de cumpleaños y fechas especiales. Eso mete una utilidad de comunidad, que no tiene que ver con dinero y es distinta del núcleo de pagos y contratos. Pero necesita saber las fechas de cumpleaños de la gente, y todavía nadie sabe si ese dato existe.

Muchas cosas quedan fuera a propósito. Vania no le va a hablar a los inquilinos. No va a manejar al personal. No se va a conectar todavía con el sistema de entradas del edificio, aunque ese sistema sí existe, se llama ZKAccess, y más adelante sí está pensado conectarlo. Si aparece una idea buena que necesite construir todo un sistema nuevo, se apunta para después.

¿Para qué todo esto? Por dos cosas, y ninguna está asegurada. Que a Works de verdad le sirva, y eso se vería si, cuando aparece algo que Vania puede resolver, Grecia acude a ella en vez de regresar a como lo hacía antes. Y que David la quiera para él, y pase de "estoy probando lo tuyo" a "quiero la mía".

Al desarrollador también le interesa aprender qué partes de esto se pueden repetir con otros clientes, pero eso no es parte de la prueba de Works ni se mide durante esa semana.

Se las va a prestar como una semana, corriendo en el servidor del desarrollador, sin que él tenga que estarlos guiando todo el tiempo mientras la usan. Eso no quiere decir que no haya soporte ni mantenimiento. Esa semana no es una medida científica: es el tiempo que se decidió dar para poder mirar si la usan, cuánto, y qué les estorba. Si al final David decide comprarla, entonces se mudaría a un servidor de él.

## Por qué esto importa

El problema **no** es que la operación de Works sea compleja. Es una operación relativamente sencilla, con pocas personas.

El problema es que la herramienta que usan es muy rudimentaria para lo que necesitan, y ellos tienen poca facilidad tecnológica. Resultado: una administración que debería ser muy sencilla termina siendo manual, limitada y poco aprovechada.

Hoy el Excel guarda datos puntuales. Si el titular de una oficina paga, alguien lo registra. Pero la hoja no convierte esos datos en información útil.

**No existe hoy una capa real de análisis.** Actualmente no utilizan esa información para generar análisis como patrones de pago, puntualidad o recurrencia. Podría servir para saber qué inquilinos pagan siempre puntuales, cuáles se retrasan de forma recurrente, detectar patrones, incluso construir incentivos para premiar buenos historiales de pago.

Lo confirmado es que **hoy no existe una explotación significativa de esos datos para análisis**. No se sabe exactamente qué posibilidades han considerado, así que no se les atribuye ninguna creencia al respecto.

### Hipótesis descartada
No se confirma que el dolor principal sea "los pagos" o "las renovaciones", ni que se enteren tarde de contratos vencidos o pagos pendientes. El usuario no puede confirmarlo. El dolor es más general, el descrito arriba.

### El efecto que se busca, contado con un caso real
En una junta, David dijo que le encantaría que algún día un agente de IA pudiera recibir una instrucción por voz y mandar imprimir en su impresora HP Smart Tank. Para él sonaba futurista.

Esa integración ya estaba lista en Hermes. En ese momento, el usuario sacó su teléfono, le dio la instrucción por voz a Hermes, y Hermes mandó imprimir en la HP Smart Tank.

La reacción es la lección de diseño: **una función técnicamente sencilla puede sentirse extraordinaria si elimina una tarea que la persona percibía como complicada o futurista.**

Ese es el efecto buscado con Vania: que la tecnología haga cosas reales por ellos, sin obligarlos a entender lo que hay detrás.

## Para quién es

### David · dueño de Works
Toma las decisiones principales sobre inversiones, adquisiciones, remodelaciones, tecnología y cambios relevantes en la operación.

El inmueble donde opera Works pertenece a su papá, **Don Fernando Moreno**, que además es socio de David en Works. Para efectos de este proyecto, David se trata como el dueño y principal tomador de decisiones.

Conocimientos técnicos muy limitados.

**David es a quien principalmente se quiere cautivar.** El objetivo es que vea capacidades que hoy no espera de una herramienta administrativa, y que eso le genere el deseo de tener su propia Vania.

Uso probable: supervisión, consulta y descubrimiento. Ver rápido cómo está Works. Consultar sin tener que pedirle a Grecia que busque. Descubrir situaciones o patrones que hoy no son visibles. Pedirle acciones directamente a Vania. Experimentar capacidades que no espera de un agente.

### Grecia · administradora y encargada de Works, mano derecha de David
David le delega una parte importante de la operación cotidiana. Hoy se encarga de:
- atender a inquilinos y usuarios de Works
- recibir y registrar pagos
- dar seguimiento a cobros
- mantener actualizada la información administrativa
- administrar al personal operativo, incluyendo a su asistente y al guardia de seguridad
- parte de la organización cotidiana de la comunidad, por ejemplo un pizarrón mensual con cumpleaños y efemérides

Conocimientos técnicos muy limitados.

Uso probable: operativo. Registrar que alguien pagó, actualizar información, consultar un dato, pedirle a Vania una acción administrativa, mantener el día a día al corriente.

**El punto clave de diseño:** la operación de Works es relativamente sencilla, pero **muchas tareas administrativas dependen hoy del registro, el seguimiento y la memoria manual de Grecia**. Ese seguimiento manual **implica riesgo de olvidos, inconsistencias o seguimiento incompleto**. Esa es una inferencia razonable, no un acontecimiento documentado: no se han registrado casos concretos.

Ahí es donde se busca que Vania quite carga mental y administrativa.

Matiz explícito del usuario: no es correcto decir que "todo depende de que Grecia se acuerde". Es demasiado absoluto.

### Tamaño de la comunidad
- Alrededor de **21 titulares de renta**, entre oficinas y distintas modalidades de espacio.
- La comunidad que usa Works sube a unas **70 personas** contando a los empleados de esos titulares.

### Una regla sobre los dos
No se diseñan dos productos distintos. **Ambos deben poder usar las dos superficies**, Vania y Dashboard. La diferencia entre ellos es de hábito, no de capacidad. Esa diferencia no debe convertirse en una limitación del producto.

## Qué existe hoy
- **Una hoja de Excel.** La información administrativa relevante que se ha discutido, sobre oficinas, inquilinos, contratos y pagos, se gestiona actualmente ahí.
- No hay documentos impresos adicionales ni ningún otro sistema paralelo para esa administración.
- La hoja sí se usa de verdad, aunque puede estar desactualizada.
- El usuario **todavía no tiene acceso a ese archivo**. Cuando se lo compartan, servirá como punto de partida para trasladar la información a la nueva solución.
- Existe ya una integración funcionando en Hermes para mandar imprimir a una impresora HP Smart Tank por instrucción de voz.
- Alrededor de 21 titulares de renta y unas 70 personas en la comunidad. Ver "Para quién es".
- `ZKAccess 3.5` de ZKTeco es el control de acceso real de Works, en operación hoy. Que no entre en la primera versión es una decisión, no un hecho: ver "ZKTeco".
- Impresora HP Smart Tank disponible en Works, con la integración ya funcionando en Hermes.

### Vania ya existe y ya funciona
No es un nombre ni una idea futura. Hoy es un perfil independiente dentro de Hermes, con:
- ID técnico propio: `vania`
- directorio propio
- `SOUL.md` propio
- configuración propia
- selección de tools propia
- gateway propio
- sesión propia de WhatsApp
- bridge de WhatsApp levantado específicamente para ese perfil

**Vania ya responde por WhatsApp hoy.**

Los números de WhatsApp de **David y Grecia ya están configurados y autorizados**. Cuando llegue el momento de abrir la prueba, ese canal no se configura desde cero.

Modelo actual de Vania: `GPT-5.6 Terra`.

**Aislamiento:** perfil, gateway, configuración, tools, sesión y datos de Vania están aislados de otros perfiles. La única dependencia compartida relevante es que las credenciales OAuth de Codex se reutilizaron durante la configuración, así que esas **no** son totalmente independientes.

### Qué todavía no existe
Falta convertir esa Vania genérica en **Vania para Works**:
- el Dashboard terminado
- los datos reales de Works
- la estructura definitiva derivada del Excel real
- las capacidades administrativas específicas que se están definiendo
- las integraciones posteriores que puedan añadirse

En una frase: **Vania ya existe como agente funcional, pero todavía no está especializada ni conectada a los datos reales de Works.**

## Cómo se ve el éxito

Works es **cliente real** y a la vez **oportunidad comercial con David**. Esos son los dos niveles de éxito de esta prueba.

**Ambos son objetivos e hipótesis, no resultados conocidos.** Ninguno está garantizado. La prueba existe precisamente para observar si ocurren.

### Nivel 1 · Éxito operativo · objetivo
Que David y Grecia dejen de ver a Vania como una demostración y la usen porque de verdad les facilita la operación.

**No se mide uso diario.** Ni sesiones, ni aperturas, ni rachas de días consecutivos.

La señal de adopción es:

> **Cuando aparece una necesidad real que Vania o el Dashboard pueden resolver, Grecia recurre a ellos por iniciativa propia en lugar de volver automáticamente al método anterior.**

Lo que interesa es el **uso autónomo y recurrente ante necesidades reales**.

Criterio del usuario: si Vania se ve impresionante pero no resulta útil en el día a día, no funcionó.

### Nivel 2 · Éxito comercial inmediato · objetivo
El cambio que el usuario considera más importante observar: que después de probarla, **David quiera quedársela**.

Es decir, que pase de "estoy probando lo que construiste" a **"quiero mi propia Vania"**, y que quiera moverse de la prueba temporal en la infraestructura del desarrollador a una implementación propia para él y para Works.

Otra señal que sería fuerte: **que David empiece a pedir capacidades que no estaban contempladas.** Eso indicaría que dejó de verla como algo que le están mostrando y empezó a imaginarla como herramienta suya.

Nada de esto está garantizado. Es lo que la prueba busca averiguar.

**Los criterios de éxito de esta prueba son dos: el operativo y el comercial.** La transferibilidad a otros clientes **no** es un criterio de éxito de Works. Ver "Transferibilidad · interés interno posterior".

### Precisión importante
Works **no es un pretexto** ni un escenario inventado. Es el entorno real donde David puede experimentar qué significa tener un agente trabajando con su operación.

### Transferibilidad · interés interno posterior
Que los patrones de Vania y su Dashboard puedan repetirse con otros clientes es un **interés interno del desarrollador para una etapa posterior**, no un criterio de éxito de la prueba de Works.

Durante esta prueba, la transferibilidad **no** debe:
- medirse
- generar entregables para Works
- producir configuraciones adicionales
- ampliar el alcance
- provocar trabajo extra

El perfil del desarrollador es relevante solo para descartar un malentendido: no es su primer agente, ni su primer dashboard, ni su primer proyecto. Esto no trata de aprender a construir.

### Impacto inicial contra utilidad sostenida
No se elige uno. Se necesitan los dos.

> **Suficiente impacto para querer probar Vania y suficiente utilidad para querer conservarla.**

La primera impresión importa porque busca provocar curiosidad y deseo. Después viene una prueba real de varios días. Criterio del usuario: si sorprende cinco minutos y luego Grecia no quiere usarlo o David deja de abrirlo, no funcionó.

## Principio rector

> **Vania no sustituye el control de David y Grecia. Les da otra forma de ejercerlo.**

Debe quitarles trabajo sin quitarles la sensación de que pueden intervenir cuando quieran.

## El papel especial del Dashboard
Esta es una directriz de diseño, no un detalle.

Gran parte de lo que hace un agente **ocurre de forma invisible**. Para alguien que no vive en esta industria, explicarlo con palabras sigue siendo abstracto por más sencilla que sea la explicación.

El Dashboard **debe convertir parte de esa abstracción en algo visible**. Se busca que permita pasar de:

> "me están explicando lo que hace un agente"

a:

> "estoy viendo lo que está pasando y entiendo qué puedo hacer con esto"

Por eso no basta con una herramienta administrativa eficiente. El Dashboard debe ser:

**útil + fácil + visualmente deseable + capaz de revelar posibilidades.**

### Principio derivado
*Inferencia del asistente, construida a partir de las respuestas del usuario y no contradicha por él. No es una afirmación verificada sobre David ni sobre Grecia.*

Como no hay un dolor agudo que ellos sepan nombrar, la hipótesis es que **el valor no se pide, se revela**. No llegarán al Dashboard con una pregunta en la cabeza, porque no saben que la herramienta puede responderla. La primera pantalla no puede ser un buscador ni un menú esperando que sepan qué pedir. Tiene que mostrarles algo que no sabían que querían saber, igual que pasó con la impresora.

## Decisiones ya tomadas
El planificador no debe reabrir estas.

### Producto
- **Vania es un agente al que David y Grecia acceden principalmente por WhatsApp**, hablando de forma natural. WhatsApp es el canal, no el lugar donde Vania vive. Dónde corre técnicamente no se define en este handshake.
- En la primera versión se busca que Vania pueda **consultar información y ejecutar acciones reales** sobre la operación de Works. Esas capacidades todavía no están construidas.
- Vania debe trabajar con información real, sin inventar datos ni depender de lo recordado en una conversación. **Se busca que registre la información en el sistema y que esa información quede disponible para consulta y para el Dashboard.** Las garantías técnicas de persistencia y respaldo se definen después, en planificación, no aquí.
- El Dashboard web es **parte del producto Vania**, no una herramienta administrativa externa añadida después.
- El Dashboard se abrirá principalmente desde el teléfono.

### Información operativa, cuatro áreas iniciales
- **Oficinas**: tipo, número, piso, m², estatus.
- **Inquilinos**: titular, contacto.
- **Contratos**: inicio, fin, alerta de renovación.
- **Pagos**: precio, depósito en garantía o fianza, fecha de pago, forma de pago, estatus de pago.

### Dirección visual
- Estilo **neumorphism**, con el cuidado visual que el usuario asocia a productos Apple.
- Paleta: perla, blanco, crema, gris claro.
- Neumorphism **no dogmático**: los elementos importantes conservan jerarquía visual clara y pueden usar acentos de mayor contraste cuando haga falta.
- Se busca la sensación de profundidad: un control sobresale y se siente hundir al tocarlo.
- **Mobile-first**, funcionando también en escritorio.
- Sofisticado y muy cuidado. Fácil de usar no significa básico, infantil ni barato.

### Dos efectos simultáneos buscados
1. Romper con lo que se espera de una herramienta administrativa y generar sensación de tecnología avanzada, cuidada y especial.
2. Producir paz, claridad y muy baja carga mental al usarlo.

### Accesos y roles
Decidido: en esta primera etapa **David y Grecia ven exactamente la misma información operativa**. No se introduce una estructura compleja de permisos.

**La ausencia de autenticación no es una opción aceptada por defecto.** Antes de utilizar datos reales de Works debe existir algún mecanismo de acceso restringido. **No se asume que conocer la URL sea protección suficiente.**

Lo que queda pendiente para planificación es el **mecanismo concreto, las reglas finales y la implementación de roles**. Lo que no queda abierto es si hay o no control de acceso.

Si una estructura formal de cuentas y roles introdujera complejidad innecesaria para esta primera versión, esa estructura **no debe volverse un requisito que bloquee el proyecto**. El control de acceso mínimo sí es requisito.

Condicional: **si implementar autenticación y roles resulta razonablemente sencillo**, la estructura es:

- **`Admin`, David**: ve toda la información, registra y edita, usa todas las capacidades operativas, administra la cuenta `Editor`, puede eliminarla o desactivarla.
- **`Editor`, Grecia**: ve la misma información que David, registra y edita, usa las mismas capacidades operativas. Lo único que no puede es administrar, eliminar o modificar la cuenta de David.

`Editor` **no** significa que Grecia vea menos. Admin y Editor tienen la misma visibilidad y prácticamente las mismas facultades operativas. La única diferencia es la administración de cuentas.

**Acceso del desarrollador**: separado y distinto. No es otro rol operativo de Works. Es el acceso técnico de quien construye y mantiene el sistema, para mantenimiento, diagnóstico, correcciones, configuración, cambios sustanciales y evolución futura. No se mezcla con la relación `Admin / Editor`.

### Técnicas
- Arquitectura: `Vania → FastAPI → SQLite` y `Dashboard → FastAPI → SQLite`.
- **FastAPI es la única capa que toca SQLite directamente.**
- SQLite como base de datos inicial.
- Dashboard propio, con libertad total sobre HTML, CSS y JavaScript.
- Apache ECharts permitido solo si una visualización realmente lo necesita. Las gráficas no son el centro del producto.
- Desarrollo primero en local, manteniendo portabilidad.
- La prueba con David y Grecia corre en el **VPS actual del desarrollador**, no en uno de David. La migración a infraestructura propia de David ocurre después y **solo si decide adquirir Vania**. Ver "Dónde viven los datos durante la prueba", que es la versión correcta de esta secuencia.

## Decisiones todavía abiertas
Solo el usuario puede cerrarlas.

### Cómo entran al Dashboard
**Abierta.** No se escoge todavía entre enlace, acceso desde la propia Vania, PWA, acceso directo en la pantalla del teléfono u otra solución.

Lo que **sí está decidido a nivel de experiencia**: entrar al Dashboard debe ser **extremadamente sencillo y no depender de que el desarrollador tenga que guiarlos**. La solución concreta se decide después.

*Riesgo señalado por el asistente, no confirmado por el usuario:* si David tuviera que recordar una contraseña, o si el enlace se le perdiera en WhatsApp, podría no volver a abrirlo. Es una hipótesis sobre el comportamiento de David, no un hecho observado.

**El usuario declinó expresamente elegir una solución en este handshake.** No se registra ninguna recomendación por defecto. El planificador debe tratar esto como una decisión pendiente, no como algo ya resuelto.

### Otras abiertas
Ninguna de estas debe darse por resuelta al planificar.

- **Cómo se representa visualmente el rastro de Vania.** Solo está decidido que exista.
- **Qué documento o resumen concreto** produce la capacidad heroica. No está fijado que sea un reporte de pagos.
- **Qué campos son editables y cuáles no**, y si alguno requiere protección adicional. Depende de conocer los datos reales.
- **Qué información puede imprimirse** y cuál no.
- **Reglas detalladas de autenticación**, si es que se implementa autenticación.
- **Qué datos mínimos de personas** requiere la función de cumpleaños y efemérides, y si esa información existe o puede obtenerse.
- **Cómo se implementa la transferencia de contexto** del Dashboard hacia la conversación con Vania.
- **Cómo se configura técnicamente** que David y Grecia puedan reducir o silenciar avisos.
- **La cifra concreta de límites de uso** durante la prueba.
- **Qué eventos merecen realmente generar un aviso proactivo.** La lista actual es un primer conjunto, no una lista definitiva.
- **Si existe un indicador dominante** para Works. Hoy no hay evidencia para elegirlo.

## Tiempos y secuencia

### Una sola prueba oficial
Habrá **una sola prueba oficial con David y Grecia**. Comienza cuando se cumplan las tres condiciones:
1. el sistema esté preparado
2. existan los datos reales necesarios
3. David tenga disponibilidad razonable

Si, una vez presentada y autorizada Vania, Grecia termina usándola antes o con mayor intensidad que David, eso puede ocurrir de forma natural. **No se define como dos pruebas, ni dos lanzamientos, ni como una estrategia obligatoria de "Grecia primero, David después".**

### No hay fecha comprometida
El ritmo lo pone el desarrollador. No se enseña una parte solo por cumplir una fecha. Primero se termina todo lo que depende exclusivamente de él y se deja sólido, y después se abre la prueba.

**La pieza más importante en este momento es el Dashboard.**

### El Excel bloquea el lanzamiento, no el desarrollo
El Excel real de Works todavía no está en manos del desarrollador y depende de terceros.

- **No bloquea el desarrollo** de las partes que pueden construirse y probarse sin datos reales. Mientras no llegue, se sigue construyendo lo que depende del desarrollador.
- **Sí bloquea el inicio de la prueba operativa real** con David y Grecia.

Existe un **Google Sheet preliminar**, que es únicamente un placeholder y **no debe convertirse en fuente de verdad**. Tampoco se inventan datos.

**No queda aprobado ningún Plan B** de reconstrucción manual de datos. Si el retraso del Excel llegara a amenazar seriamente el lanzamiento, ese escenario se evaluará entonces.

**Requisito derivado:** el Dashboard se diseña desde ahora lo bastante sólido y adaptable para que, cuando llegue la información real del Excel, se pueda conectar o ajustar **sin rehacer el Dashboard desde cero**.

### Secuencia ideal
```text
construir bien lo que depende de mí
        ↓
Dashboard listo y probado
        ↓
Vania preparada para Works
        ↓
recibir información real de Works
        ↓
adaptar/importar los datos necesarios
        ↓
pruebas finales
        ↓
abrir acceso a David y Grecia
```

No hay fecha fija, pero sí un **criterio claro de preparación**.

### Horizonte deseado, no deadline
Objetivo personal: que antes de terminar **octubre de 2026** el proceso haya avanzado incluso más allá de la prueba inicial. No es un deadline.

Circunstancia relevante: **David se convierte en papá a finales de septiembre de 2026**, así que su disponibilidad puede cambiar y la prueba podría iniciar durante octubre. No se fuerza una fecha artificial por encima de eso.

### Duración de la prueba: aproximadamente 1 semana
Se refiere a la prueba única descrita arriba.
Es una **decisión de prueba**, no una afirmación de que siete días sean suficientes ni una garantía de adopción.

El propósito es permitir **uso repetido y autónomo durante varios días**, para observar:
- utilidad real
- frecuencia de uso
- comportamientos inesperados
- fricciones
- percepción de valor
- deseo o no de conservarla

**El criterio de fondo, aceptado:** no depender de una única gran demostración. Lo que interesa observar no es la reacción a una presentación, sino si aparece adopción. Por eso la prueba debe permitir que David y Grecia usen Vania y el Dashboard **sin que el desarrollador tenga que guiarlos constantemente durante el uso**. Eso no significa ausencia de soporte técnico ni de mantenimiento.

La hipótesis es que una semana de uso autónomo permita observar si Vania empieza a incorporarse a la rutina y si genera deseo de conservarla. No está confirmado que así ocurra.

## La experiencia del Dashboard
Esta es la parte que este handshake vino a definir. **Describe un Dashboard que todavía no está construido.** Todo lo que sigue es alcance decidido y comportamiento previsto, no comportamiento observado.

La jerarquía y los principios están cerrados. Siguen abiertos varios detalles, listados en "Decisiones todavía abiertas".

### La jerarquía, de arriba hacia abajo
```text
estado general
      ↓
qué necesita atención
      ↓
indicadores que lo explican
      ↓
actividad de Vania
      ↓
detalle cuando el usuario lo pide
```

### Nivel 1 · Estado general, los primeros tres segundos
Decidido: la primera respuesta del Dashboard debe ser una **lectura humana del estado de Works**, no una cifra.

> **Works está tranquilo.**

> **Hay 3 cosas que necesitan atención.**

Esas frases **no deben ser textos fijos de marketing**. Deben ser una conclusión producida a partir del estado real de la información.

Decisión real: **si no existe nada relevante que requiera atención, el Dashboard debe comunicar tranquilidad de forma humana y evitar llenar la interfaz con actividad artificial.**

Principio que gobierna esto:

> **No des la hora si no te la piden.**

El sistema **no debe fabricar actividad, novedades ni llamadas de atención para generar engagement**. Si no hay nada relevante, el silencio y la tranquilidad son el comportamiento correcto.

La actividad histórica puede existir y ser consultable, pero **no debe usarse artificialmente para conseguir que David o Grecia vuelvan al Dashboard**.

Lo que se busca evitar es que aprendan: *"el Dashboard está llamando mi atención otra vez, seguramente no es nada importante"*. La intención es la contraria: que cuando Vania o el sistema llamen su atención, haya una razón relevante.

Esto extiende al Dashboard el principio que ya gobierna los avisos de Vania: **relevancia antes que frecuencia**. La sensación que se busca con esto es **paz**.

`"Todo está bien"`, `"Works está tranquilo"` y `"Hay 3 cosas que necesitan atención"` son **ejemplos conceptuales**. El texto exacto queda abierto.

La mayor jerarquía visual debe tenerla esa conclusión. No `87%`. No `$42,350`. No una gráfica enorme.

La pregunta que responde el nivel 1 es: **¿hay algo que merezca mi atención o no?**

Para llegar a esa conclusión el sistema puede usar varias variables: pagos, ocupación, contratos, movimientos recientes, pendientes relevantes. Ninguna de ellas se convierte automáticamente en "el número de Works".

### No hay un KPI que gobierne
**Decisión:** la primera pantalla **no** está gobernada por un único KPI. Está gobernada por el **estado de atención de Works**. Los indicadores acompañan y explican ese estado.

Se rechazó explícitamente la propuesta de que "ocupación" fuera el número dominante. No por estar equivocada, sino porque **hoy no hay evidencia para escogerla por encima de cobranza del mes, pagos pendientes, contratos próximos a vencer o ingresos**. No se fabrica un KPI principal solo porque un Dashboard normalmente tiene uno.

Cuando existan los datos reales y se pueda observar qué consulta David, se podrá descubrir si hay un indicador dominante. Si aparece, puede ganar jerarquía entonces.

### Nivel 2 · Lo que merece atención
Aquí aparecen las cosas concretas que explican el estado general, escritas **como las comunicaría una persona**.

> **La oficina 204 vence en 12 días.**

y no `Fecha fin contrato: 02/10/2026`, que obliga a interpretar.

> **Hay 2 pagos pendientes este mes.**

y no una tabla completa de entrada.

La lógica es: **qué pasa → por qué importa → si quiero, entro al detalle.**

### Nivel 3 · El detalle
Aquí deben vivir las áreas completas: espacios, inquilinos, contratos, pagos. **Su estructura definitiva depende del Excel real, que todavía no está disponible.** Deben estar disponibles y poder explorarse bien.

Pero **esa estructura no saluda al usuario apenas entra**. El detalle está cuando se necesita, no compitiendo con lo importante.

### Capa transversal · El rastro de Vania
**Decidido: el Dashboard debe permitir percibir actividad de Vania.**

No solo porque sea útil saber qué ocurrió, sino porque cumple uno de los objetivos centrales del producto: **volver visible lo que el agente hace de forma invisible.**

Ejemplos del tipo de rastro que se busca mostrar, una vez construido:
- Vania registró un pago
- Vania actualizó un dato
- Vania detectó un próximo vencimiento
- Vania ejecutó una acción
- Vania encontró algo que necesita revisión

Todavía **no** está definido cómo se representa visualmente. Lo decidido es que exista.

Sin esta capa, el riesgo es terminar construyendo **únicamente una base de datos bonita**.

### Misma pantalla para los dos
Decidido para la primera versión:
- misma pantalla para David y Grecia
- misma información
- **mismo orden**, inicialmente

No se personaliza el orden de las alertas según quién inició sesión. Dos razones:

1. Primero hay que **observar cómo usan realmente el Dashboard** antes de decidir que sus prioridades visuales deben ser distintas.
2. Tener una **referencia compartida**. Si David y Grecia hablan del Dashboard, deberían estar viendo lo mismo. "Mira lo que aparece arriba" significaría lo mismo en ambos teléfonos.

Eso no significa que lleguen con la misma intención. David puede abrirlo preguntando **"¿cómo está Works?"** y Grecia **"¿qué necesita atención?"**. Una misma pantalla puede responder las dos preguntas.

Si durante la semana de prueba se descubre que la usan de formas consistentemente distintas, ahí habrá evidencia real para decidir si conviene personalizarla.

### Boceto conceptual
Solo ilustra la jerarquía. **No fija estos indicadores ni estos textos.**

```text
WORKS ESTÁ TRANQUILO

Todo lo importante está al día.

Pagos          Ocupación          Contratos
al día         estable            1 próximo

Vania
3 movimientos registrados hoy
```

## La proactividad de Vania
Decidido.

**Decisión: en la primera versión se busca que Vania pueda escribir primero cuando exista algo que realmente requiera atención.** Ese comportamiento todavía no está implementado.

No se quiere una Vania que solo espere a que alguien se acuerde de escribirle. Tampoco una que convierta WhatsApp en ruido.

### Comportamiento previsto
- Responde cuando David o Grecia le hablan. *Esto ya ocurre hoy.*
- Puede iniciar una conversación cuando detecta algo importante. *La proactividad específica para Works todavía no está implementada ni configurada.*
- Si no hay nada relevante, **permanece en silencio**. *Por construir.*

### Regla de gobierno: relevancia antes que frecuencia
**No** se fija una regla artificial tipo `máximo un mensaje al día`. Se rechazó explícitamente esa propuesta porque todavía no hay evidencia de que esa frecuencia sea la correcta. Puede haber días sin ningún aviso y días con varias cosas importantes de verdad.

### Agrupar antes que bombardear
Si hay varias cosas relacionadas, Vania debe agruparlas en un solo mensaje claro en vez de mandar mensajes separados. Por ejemplo:

> Hay tres cosas que requieren atención hoy:
> - un pago pendiente
> - un contrato próximo a vencer
> - una inconsistencia que necesito que revisen

El objetivo es que un aviso de Vania se sienta como **"esto merece que lo sepas"**, no como una notificación automática más. Si eso se logra o no es algo que solo la prueba puede mostrar.

### De qué puede avisar, primer conjunto
No es una lista definitiva. Cuando existan los datos reales de Works se podrá determinar qué eventos merecen de verdad un aviso.

- **Pagos**: un pago pendiente o una situación de cobranza que requiera atención.
- **Contratos**: cuando uno se acerque a una fecha que merezca revisión o renovación.
- **Anomalías o inconsistencias**: información contradictoria, incompleta, o algo que necesite intervención humana.
- **Acciones automáticas importantes**: si más adelante Vania ejecuta acciones relevantes por sí misma, puede tener sentido informar que las realizó.

### Distinción que no se debe confundir
**Aviso proactivo** no es lo mismo que **confirmación de una acción solicitada.**

Si Grecia dijera "ya pagó el titular de la oficina 204" y Vania respondiera "listo, registré el pago", eso **no** sería proactividad. Es la confirmación normal de algo que Grecia pidió.

La proactividad empieza cuando Vania detecta algo y decide comunicarlo **sin que nadie haya preguntado primero**.

### Un solo cerebro, dos superficies
Principio de producto decidido:

> **El Dashboard y Vania deben reflejar el mismo estado de Works y compartir una lógica coherente.**

Esto es un principio de diseño, no una garantía técnica de consistencia.

**Dónde vive la lógica que interpreta el estado de atención queda pendiente para planificación.** Que FastAPI sea la única capa con acceso directo a SQLite **no implica** que FastAPI deba ser quien interprete el estado de Works. El planner propondrá dónde ubicar esa lógica y lo justificará, sin alterar la arquitectura de acceso a datos ya decidida.

El principio de producto que sí queda fijo: **Vania y el Dashboard deben trabajar sobre un estado operativo coherente de Works.**

```text
Estado real de Works
        │
        ├── Dashboard → lo hace visible
        │
        └── Vania → interviene si merece atención
```

- Si el estado no requiere atención: el Dashboard debería comunicar tranquilidad y Vania no escribir.
- Si aparece algo importante: el Dashboard debería mostrarlo y Vania podría avisarlo por WhatsApp.

### Control de las personas
David y Grecia deben poder pedirle que reduzca, silencie o deje de avisar sobre cierto tipo de eventos si algo resulta molesto. **No** se decide todavía cómo se configura técnicamente. El principio sí queda fijo:

> **La proactividad de Vania debe ser útil, limitada y controlable por las personas que la usan.**

## El reparto entre WhatsApp y el Dashboard
Decidido.

**No habrá un chat completo duplicado dentro del Dashboard.** La conversación con Vania seguirá viviendo principalmente en WhatsApp.

El Dashboard **no debe ser una pantalla pasiva de solo consulta**. Debe ser una herramienta operativa real.

El reparto correcto **no** es este:
```text
WhatsApp = hacer
Dashboard = mirar
```

Es este:
```text
WhatsApp
= conversar con Vania y pedir acciones en lenguaje natural

Dashboard
= entender, administrar, modificar y actuar visualmente
```

### En WhatsApp
Ahí David y Grecia deben hablar con Vania, hacer preguntas, dar instrucciones en lenguaje natural, recibir avisos proactivos y continuar una conversación sobre algo que esté ocurriendo en Works.

*Hoy ya pueden conversar con Vania por WhatsApp. Las instrucciones sobre la operación de Works y los avisos proactivos están por construir.*

### En el Dashboard
Ahí deben poder ver qué está pasando, entender el estado de Works, navegar la información, revisar detalle, **modificar información, ejecutar acciones operativas y comprobar el resultado**.

*Todo esto está por construir.*

### El Dashboard no es read-only
**Decidido.** La lectura es una parte de la experiencia, no su límite.

Principio: **la información administrativa de Works debería poder gestionarse desde el Dashboard cuando tenga sentido hacerlo.** Por defecto se puede gestionar, salvo que después exista una razón concreta para restringir alguna parte.

**No** se define todavía una lista de campos editables, campos bloqueados, permisos especiales ni excepciones. Eso se decide cuando se conozca la estructura real de los datos de Works.

Se busca que Grecia pueda registrar un pago por dos caminos, y que ambos terminen reflejándose en el mismo estado de Works:
- **Por Vania**: "Vania, registra que la oficina 204 pagó septiembre por transferencia."
- **Por el Dashboard**: entrar al registro, modificar la información y guardar.

Ninguno de los dos caminos está construido todavía.

### Por qué importa el control manual
No es solo una función administrativa, es parte de la experiencia.

La razón del control manual es **preservar control, reducir incertidumbre y permitir que David o Grecia puedan comprobar o corregir directamente una acción cuando lo necesiten**. No se predice que vayan a desconfiar de Vania.

La intención es que, al encontrar algo, modificarlo, guardarlo y ver que quedó resuelto, obtengan una sensación de **control + certeza + avance**. Eso importa especialmente mientras desarrollan confianza en Vania.

### Saltar del Dashboard a Vania
Principio decidido:

> **Desde un elemento del Dashboard debe ser posible continuar la conversación con Vania sobre ese mismo contexto.**

Ejemplo previsto: David ve "la oficina 204 vence en 12 días", toca ese elemento, y puede seguir el tema con Vania sin empezar de cero explicando qué estaba viendo. **No** se define todavía cómo se implementa esa transferencia de contexto.

### Los dos caminos
```text
Veo algo en el Dashboard
        │
        ├── lo resuelvo directamente ahí
        │
        └── quiero preguntarlo, delegarlo o hacer algo más
                         ↓
                       Vania
                    por WhatsApp
```

## La capacidad heroica de la primera prueba
Decidida como apuesta, no como resultado conocido.

**No se sabe cuál será objetivamente lo más impresionante para David.** Lo que sí está decidido es una capacidad elegida para **intentar producir** ese efecto:

> **Que Vania pueda utilizar información real de Works, generar un resultado útil, y materializarlo mediante una acción física en la HP Smart Tank.**

Esa capacidad todavía no está construida. Que produzca o no el efecto buscado es precisamente lo que la prueba debe mostrar.

### La secuencia que importa
```text
datos reales → comprensión → resultado útil → acción física
```

Ejemplo, **no fijado como requisito**:
```text
David:
"Vania, dame el estado de pagos de este mes
y déjamelo impreso."
        ↓
Vania consulta los datos reales de Works
        ↓
interpreta la información
        ↓
genera un resumen útil
        ↓
lo manda a la HP Smart Tank
        ↓
el resultado aparece físicamente en Works
```

No se fija todavía que tenga que ser un reporte de pagos. Cuando existan los datos reales se decidirá qué documento o resumen resulta más útil.

### Por qué no se busca repetir el truco anterior
David ya vio a Hermes recibir una instrucción y mandar algo a imprimir. Valoración del usuario: **repetir ese truco exacto probablemente ya no produzca el mismo efecto.**

Lo que vio antes:
```text
agente → impresora
```

Lo que se busca que experimente ahora:
```text
Vania → entiende Works → usa información real de Works → produce algo útil → actúa físicamente en Works
```

**La intención es que la impresora deje de ser el truco y se convierta en la evidencia física de que Vania entendió lo que estaba ocurriendo y actuó sobre ello.**

## ZKTeco · confirmado, pero para después
`ZKAccess 3.5` de ZKTeco **es el control de acceso real de Works**. Existe la intención de que Vania se integre con él.

**No es requisito para esta primera prueba.** Pertenece a una evolución posterior.

Si se llega a esa etapa, Vania podría usar información que no depende de que Grecia o David se la introduzcan manualmente, por ejemplo registros reales de acceso. Ese sería otro salto:

```text
Vania administra lo que le contamos
        ↓
Vania empieza a percibir lo que ocurre
en el espacio físico
```

El usuario considera esa evolución muy potente. Aun así, la primera prueba **no debe depender de tenerla lista**. Nada de esa integración está construido ni especificado.

### Dirección de crecimiento
No se cierra en este handshake qué hará exactamente cada integración futura. Lo que sí queda claro: **Vania está pensada para crecer más allá de la administración de datos**, hacia la infraestructura física real de Works.

## Alcance de la primera versión
Cerrado.

### Criterio de frontera
> **Una capacidad entra en esta primera versión solo si fortalece directamente la utilidad diaria de David o Grecia, la comprensión de Works o la experiencia de Vania, sin convertir el proyecto en otro sistema administrativo mucho más grande.**

Si aparece una buena idea durante la construcción pero necesita **nuevas entidades, nuevos usuarios o una nueva operación completa**, se documenta para una fase posterior en lugar de meterla automáticamente.

### Dentro · núcleo operativo
- espacios
- inquilinos
- contratos
- pagos
- estado de atención
- edición directa
- actividad de Vania
- avisos relevantes

### Dentro · experiencia Vania
- conversación por WhatsApp
- proactividad controlada
- continuidad desde el Dashboard hacia una conversación contextual con Vania
- confirmación visible de acciones
- mismo estado de Works reflejado en Dashboard y en Vania

### Dentro · capacidad física
- generación de un resultado útil a partir de información real de Works
- posibilidad de enviarlo a la HP Smart Tank

### Dentro · capacidad complementaria: pizarrón mensual
Hecho actual: Grecia prepara hoy manualmente un pizarrón mensual con cumpleaños de la comunidad y efemérides.

Decisión: incluir en la primera versión que Vania **pueda ayudarle a prepararlo**. Por construir.

```text
"Vania, prepara el pizarrón de octubre."
        ↓
Vania reúne la información disponible
        ↓
genera la composición correspondiente
        ↓
puede dejarla lista o mandarla a imprimir
```

Por qué entra: **introduce una utilidad comunitaria y no financiera, distinta del núcleo administrativo de pagos y contratos.** La hipótesis es que **pueda generar adopción de Grecia por gusto y conveniencia, no solo por obligación administrativa**. No está comprobado.

**Precisión explícita del usuario:** esto **sí toca información adicional**. Necesita datos mínimos de las personas cuyos cumpleaños se consideren. No es correcto decir que "no toca el modelo de datos". Lo toca, de forma limitada.

**Condición pendiente:** no se sabe todavía si esa información existe en el Excel de Works ni cómo podría obtenerse. La función queda condicionada a que esos datos estén disponibles o se puedan capturar.

Decisión: **incluir la función de cumpleaños y efemérides sin convertir esta versión en un sistema completo de gestión de comunidad.**

### Fuera de alcance por ahora
No porque no puedan tener valor. Porque todavía no hay evidencia de que sean necesarias para esta primera prueba.

- administración de personal operativo, incluidos la asistente de Grecia y el guardia
- gestión completa de las aproximadamente 70 personas de la comunidad
- cobranza automatizada hacia inquilinos
- contacto directo de Vania con inquilinos
- integración con ZKTeco
- otras integraciones físicas posteriores

## Dónde viven los datos durante la prueba
Corrección importante. La prueba **no** corre en una máquina local de Works.

```text
desarrollo inicial en local
        ↓
despliegue en el VPS actual del desarrollador
        ↓
prueba real con David y Grecia
        ↓
si David adquiere Vania
        ↓
migración a infraestructura o VPS propio de David
```

La prueba corre desde la infraestructura actual del desarrollador. La migración al VPS de David ocurre después, **solo si decide adquirir Vania**.

## Datos sensibles y restricciones
**No se registra que "no hay reglas duras especiales".** Eso convertiría una ausencia de decisión en una decisión.

Todavía no se conoce la estructura real completa del Excel ni todos los datos que se van a manejar.

> **Las restricciones específicas sobre qué datos pueden editarse, imprimirse, exponerse o requerir protección adicional siguen abiertas y deberán definirse al conocer la información real de Works.**

Principios que sí quedan fijos desde ahora:
- el acceso debe estar limitado a personas autorizadas
- **no** se asume que todo dato puede imprimirse
- **no** se asume que todo campo puede modificarse
- no se comparte información operativa de Works con terceros
- **Vania no contactará inquilinos en esta primera versión**

### Acceso durante la prueba
No se registra "solo dos números autorizados" como regla absoluta del producto.

> **David y Grecia son los usuarios operativos de la prueba, y el desarrollador conserva el acceso técnico y administrativo necesario para mantenerla.**

## Límites y reglas que no se rompen
- Ni David ni Grecia deben aprender configuraciones, APIs, infraestructura ni procesos técnicos.
- Nada de ERP tradicional, Excel convertido en web, ni dashboard SaaS genérico lleno de gráficas, tarjetas y controles porque sí.
- **No se resuelve mejorando el Excel.** Nada de una hoja más sofisticada, fórmulas ni automatizaciones dentro de Excel. La intención es sacar la operación de ahí y llevarla a Vania y su Dashboard. El Excel solo sirve como origen de los datos existentes.
- Durante la prueba, Vania corre sobre la infraestructura y los recursos del desarrollador, así que **habrá límites razonables de uso**. La cifra exacta de mensajes, llamadas o tokens **todavía no está definida**; se estimará después tomando como referencia el consumo real de Codex/OpenAI del propio desarrollador.
- Ver "Datos sensibles y restricciones" y "Alcance de la primera versión" para lo que sí está cerrado.

## Fuera de alcance
- Este handshake **no** produce un plan de construcción.
- **No toda actividad de Grecia se convierte en un módulo.** Grecia hace otras actividades administrativas pequeñas y seguramente aparecerán más oportunidades para que Vania la ayude. Eso no significa que entren ahora. El handshake debe descubrir cuáles pertenecen de verdad a la primera experiencia.
- El foco se mantiene en: Vania + Dashboard + información operativa de Works + acciones reales que produzcan utilidad y sorpresa.
- Ver la lista completa en "Alcance de la primera versión · Fuera de alcance por ahora".

## Resultado del grilling · 2026-09-20
El documento fue sometido a presión después de cerrarse. Se expusieron 12 hallazgos y el usuario cerró 8 decisiones, ya incorporadas arriba: una sola prueba con tres condiciones de arranque, el principio "no des la hora si no te la piden", la señal de adopción reformulada, el control de acceso como requisito no negociable, el Excel como bloqueante de lanzamiento, la ubicación del juicio enviada a planificación, la transferibilidad degradada a interés posterior, y la clasificación de decisiones por tipo.

**Regla que rige de aquí en adelante:** encontrar una posible mejora no autoriza a convertirla en requisito. Antes de abrir una decisión nueva hay que pasar este filtro: *¿este punto impide construir o planificar correctamente la idea ya definida?* Si la respuesta es no, se deja para planificación, UX o implementación, y no se convierte en decisión del handshake.

### Observaciones enviadas a etapas posteriores
No son decisiones pendientes del producto. Se anotan para que quien llegue a esa etapa las tenga presentes.

- **UX:** posición exacta del rastro de Vania en la interfaz. El boceto conceptual del nivel 1 muestra un contador de movimientos; conviene revisarlo contra el principio "no des la hora si no te la piden". El boceto ya está marcado como no vinculante.
- **UX:** cómo se produce visualmente el efecto de sorpresa, dado que el Dashboard se inclina hacia la calma.
- **UX:** tratamiento visual de las correcciones humanas sobre acciones de Vania.
- **Planificación:** cómo se observará la señal de adopción de Grecia al cierre de la semana.
- **Riesgo conocido:** una ventana de prueba que caiga en un tramo tranquilo del ciclo mensual puede producir poca señal, sin que eso signifique que el producto falló.
- **Riesgo conocido:** un error de Vania que nadie note durante la semana puede costar más que la ausencia de la función.

## Cómo se construyó este documento
Registro de la entrevista, para que quien lo lea sepa qué peso tiene cada parte.

Se hicieron 10 preguntas, una por turno. Hubo dos lecturas de vuelta en lenguaje simple. El usuario corrigió la primera en 4 puntos y la segunda en 9 formulaciones. Entre ambas pidió una auditoría de rigor completa, que encontró 19 problemas, todos corregidos.

**Correcciones de fondo que hizo el usuario, y que no deben revertirse:**
1. Se descartó la hipótesis de que el dolor fuera "enterarse tarde" de pagos o renovaciones. No hay un dolor agudo que ellos sepan nombrar.
2. Vania no "vive en el teléfono". WhatsApp es el canal de acceso.
3. Los roles `Admin` y `Editor` son condicionales, no un requisito que pueda bloquear el proyecto.
4. No escribir garantías de persistencia que nadie acordó.
5. La prueba corre en el VPS del desarrollador, no en local ni en el VPS de David.
6. No registrar "no hay reglas duras especiales" sobre datos sensibles. Eso convertiría una ausencia de decisión en una decisión.
7. No registrar "solo dos números autorizados" como regla absoluta del producto.
8. Se rechazó inventar un KPI dominante por falta de evidencia.
9. Se rechazó fijar una frecuencia máxima de avisos por falta de evidencia.
10. No describir al desarrollador como si estuviera aprendiendo a construir agentes o dashboards. No es su primer agente, ni su primer dashboard, ni su primer proyecto.

**Regla de redacción permanente para este documento:** distinguir siempre entre hecho actual, decisión, objetivo o hipótesis, y pendiente. No usar presente para capacidades que todavía no existen. No convertir ausencia de decisión en permiso general. No atribuir creencias a David o a Grecia que no se hayan confirmado.

## Preguntas abiertas para investigación
Lo que el investigador debe averiguar, y por qué importa cada respuesta.

1. **¿Qué contiene realmente el Excel de Works?** Columnas, completitud, y sobre todo cuánto historial de pagos guarda. *Por qué importa:* determina si la "capa de análisis" que el usuario echa de menos es posible en la primera versión o necesita historial que no existe.
2. **¿Existen fechas de nacimiento u otros datos mínimos de personas de la comunidad?** *Por qué importa:* de eso depende que la función de cumpleaños y efemérides sea viable, y ya está dentro del alcance.
3. **¿Qué formatos y qué flujo admite la integración con la HP Smart Tank ya construida en Hermes?** *Por qué importa:* la capacidad heroica termina en esa impresora. Si el flujo solo admite ciertos formatos, eso condiciona qué documento puede generar Vania.
4. **¿Qué expone `ZKAccess 3.5` y por qué vía?** *Por qué importa:* no es requisito de la primera versión, pero sí es la evolución declarada. Saberlo ahora evita decisiones de arquitectura que la bloqueen después. Existe documentación previa generada en otro trabajo del usuario.
5. **¿Cuál es el consumo real de referencia de Codex/OpenAI del desarrollador?** *Por qué importa:* es la base que el usuario definió para estimar los límites de uso de la prueba, que siguen sin cifra.
6. **¿Qué niveles de contraste sostiene el neumorphism sin perder legibilidad en móvil?** *Por qué importa:* el usuario ya identificó el bajo contraste como el riesgo principal de ese estilo, y decidió aplicarlo de forma no dogmática. Hace falta saber dónde está el límite real.
7. **¿Qué opciones existen para entrar al Dashboard sin fricción, y qué implica cada una?** *Por qué importa:* el usuario declinó elegir en este handshake. Necesita las opciones descritas, con sus consecuencias, para poder decidir.

## Notas para el planificador

**Objetivo declarado de este handshake:** definir con precisión qué experiencia debe ofrecer el Dashboard, qué información merece ocupar cada nivel de atención, y cómo debe sentirse Vania a través de esa interfaz. No define arquitectura ni plan de construcción.

### Lo que no se debe reabrir
Las secciones marcadas como decididas. En particular: que no haya un KPI dominante, que el Dashboard no sea de solo lectura, que no haya chat duplicado dentro del Dashboard, que los dos usuarios vean lo mismo en el mismo orden, y el criterio de frontera del alcance.

### Lo que no se debe dar por resuelto
Todo lo que está en "Decisiones todavía abiertas". En especial, **cómo entran al Dashboard**: el usuario declinó elegir y no dejó una opción por defecto.

### Dependencias y orden sugerido
- El Dashboard es la pieza declarada como más importante en este momento.
- El Excel real no está disponible y depende de terceros. **No debe bloquear.** El requisito derivado es que el Dashboard se pueda conectar o ajustar a los datos reales sin rehacerse desde cero.
- La capacidad heroica depende de dos cosas que ya existen por separado: datos de Works, que faltan, y la integración con la HP Smart Tank, que ya funciona en Hermes.
- La prueba corre en el VPS actual del desarrollador. La migración al VPS de David es posterior y condicional.

### Riesgo de diseño que conviene tener presente
El estilo elegido, neumorphism de bajo contraste, entra en tensión directa con el requisito de jerarquía visual clara y legibilidad en móvil. El usuario ya lo identificó y decidió aplicarlo de forma no dogmática, con acentos de mayor contraste donde haga falta. No es un problema sin resolver, pero sí un punto donde el plan debe ser explícito.
