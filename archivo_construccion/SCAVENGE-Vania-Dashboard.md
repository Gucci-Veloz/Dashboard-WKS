# Scavenge · Vania y el Dashboard de Works

Fecha: 2026-09-23
Fuente de las preguntas: `handshake_vania_dashboard.md`, sección "Preguntas abiertas para investigación".
Etapa: 02 — Scavenge (Handshake → **Scavenge** → Mapping → Aprobación).

Este documento reúne sin reinterpretar los cuatro reportes de investigación. Cada reporte se copió tal cual desde `scavenge/`. Solo contiene hechos con fuente y vacíos; no contiene recomendaciones ni plan.

Reglas que siguió la investigación: solo información pública verificable más los documentos del proyecto que el usuario entregó; nada del VPS; sin suponer el contenido del Excel de Works, que todavía no se ha entregado.

## Índice

| Pregunta | Tema | Investigador | Archivo fuente |
|---|---|---|---|
| P3 | HP Smart Tank 750: formatos y flujos | Researcher_1 | `scavenge/R1_hp.md` |
| P4 | ZKAccess 3.5 y PullSDK: qué expone y por qué vía | Researcher_2 | `scavenge/R2_zkaccess.md` |
| P6 | Neumorphism y contraste en móvil | Researcher_3 | `scavenge/R3_contraste.md` |
| P7 | Opciones de entrada sin fricción | Researcher_4 | `scavenge/R4_acceso.md` |

## Vacíos declarados fuera del Scavenge

Estas preguntas del handshake no se pueden investigar en la web porque dependen de información privada o de terceros. Pasan a Mapping como vacíos.

- **P1 · Qué contiene el Excel de Works.** El Excel todavía no se ha entregado. Se resuelve cuando el usuario lo reciba.
- **P2 · Si existen fechas de nacimiento u otros datos mínimos de personas de la comunidad.** Depende del mismo Excel.
- **P5 · Consumo real de referencia de Codex/OpenAI del desarrollador.** Dato que solo tiene el usuario. Sigue sin cifra.

## Notas de revisión

La revisión de la sesión maestra encontró estos puntos. No se modificó el texto de los investigadores; N1 y N2 además se marcan en línea con `[Revisión Nx]`. Los originales sin marcas están en `scavenge/`.

- **N1 · R2 H10 no está verificado.** Que ZKAccess 3.5 esté descontinuado y lo haya reemplazado "ZKBio CVAccess" viene solo de un resumen de búsqueda (el propio reporte lo dice en C2 y V2). Se trata como **vacío**, no como hecho.
- **N2 · R4 usa "inferencia directa" como fuente** en la fricción de "Sesión de larga duración" y de "PIN local en el dispositivo". Una inferencia no es un hecho con fuente, así que esas dos líneas se tratan como **vacíos**.
- **N3 · Aplicabilidad web o app nativa (R4).** El Dashboard es web. Algunas opciones descritas dependen de una app nativa instalada: el PIN local con Keystore/Keychain (OWASP MASTG trata apps móviles) y las variantes One-Tap (solo Android) y Zero-Tap de las plantillas de autenticación de WhatsApp. Los hechos son correctos en su contexto, pero en Mapping no deben darse por disponibles para un dashboard web sin confirmarlo.
- **N4 · R1 H9 (resolución en dpi) viene de distribuidores**, no de HP. El reporte ya lo advierte; no requiere acción.
- **N5 · R4 cita en el texto fuentes que no están en su lista** (securityboulevard, authgear, oloid, alflokken). Es un detalle de forma; las URLs están en el texto de cada hecho.

---

## R1 · HP Smart Tank 750: formatos y flujos

### Fuentes consultadas
- Local: `vinculacion-hp-smart-tank-750-ubuntu.md` (documento de vinculación manual de la impresora en Ubuntu 24.04)
- https://www.hp.com/emea_africa-en/products/printers/product-details/product-specifications/2100178990 (especificaciones oficiales HP)
- https://h20195.www2.hp.com/v2/GetPDF.aspx/c07767566.pdf (data sheet oficial HP, no se pudo procesar el contenido — ver Vacíos)
- https://support.hp.com/us-en/product/details/hp-smart-tank-750-series/2100043635 (portal de soporte HP, no se pudo cargar — ver Vacíos)
- https://sourceforge.net/p/hplip/news/2021/09/hplip-3218-release-notes/ (notas de versión HPLIP 3.21.8)
- https://developers.hp.com/hp-linux-imaging-and-printing/supported_devices/index (índice oficial de dispositivos soportados por HPLIP, no se pudo cargar — ver Vacíos)
- Búsquedas web generales sobre OpenPrinting/IPP Everywhere y el modelo Smart Tank 750 (sin entrada específica confirmada — ver Vacíos)

### Hechos
- H1: El lenguaje de impresión nativo documentado por HP es **HP PCL 3 GUI**. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H2: La impresora es compatible con **Apple AirPrint**, **Mopria Print Service** (certificado), **HP Print Service Plugin** (impresión desde Android), **HP Smart app** y **Wi-Fi Direct Printing**. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H3: Soporta **impresión dúplex automática** (dos caras). Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H4: Tamaños de papel soportados: A4, A5, A6, B5 (JIS), sobres (DL, C5, C6, Chou #3, Chou #4), tarjetas (Hagaki, Ofuku Hagaki), y tamaños personalizados de 88.9 x 127 mm a 215.9 x 355.6 mm. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H5: Soporta impresión a **color y monocromo**, hasta 15 ppm en negro y 9 ppm en color (ISO). Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H6: Conectividad: USB 2.0 de alta velocidad, Wi-Fi (2.4/5G dual band), Wi-Fi Direct, LAN, y Bluetooth low energy (mencionado en otras fichas técnicas, ver H9). Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H7: La memoria del dispositivo es fija en **256 MB**, no ampliable. Fuente: hp.com/emea_africa-en, especificaciones del producto.
- H8: **HPLIP 3.21.8** (septiembre 2021) agregó soporte para modelos de la serie Smart Tank, incluyendo referencias a Smart Tank 750 en las notas de la versión. Fuente: sourceforge.net/p/hplip/news/2021/09/hplip-3218-release-notes/.
- H9: Resolución de impresión: hasta 1200 x 1200 dpi renderizados en negro, hasta 4800 x 1200 dpi optimizados en color. Fuente: búsqueda web con snippets de fichas técnicas de distribuidores (jarcomputers.com, tmt.my) que replican datos de la hoja de especificaciones oficial de HP — no verificado directamente contra el PDF oficial de HP (ver Vacíos).
- H10: El documento local confirma en la práctica que la vinculación en Ubuntu 24.04 se logró vía **IPP** (`ipp://<ip>/ipp/print`), con el driver detectado automáticamente como **IPP Everywhere** — sin necesidad de HPLIP ni driver propietario HP. Fuente: archivo local `vinculacion-hp-smart-tank-750-ubuntu.md`, secciones 3 y "Resultado".

### Contradicciones
- Ninguna detectada entre el documento local y las fuentes web consultadas. El documento local afirma que la impresora fue detectada vía IPP Everywhere en CUPS sin necesidad de HPLIP; esto es consistente con el hecho de que HP declara Mopria y AirPrint (ambos estándares construidos sobre IPP) como protocolos soportados, aunque ninguna fuente web pública consultada confirma explícitamente el término "IPP Everywhere" para este modelo (ver Vacíos V1).

### Vacíos
- V1: No se pudo confirmar en una fuente oficial de HP o de IPP Everywhere/Mopria.org que el Smart Tank 750 esté listado formalmente como certificado "IPP Everywhere". La evidencia de esto proviene únicamente del documento local (detección automática en CUPS), no de una fuente pública verificable.
- V2: No se pudo leer el contenido del data sheet oficial en PDF (h20195.www2.hp.com/v2/GetPDF.aspx/c07767566.pdf) — la herramienta de lectura no pudo procesar el binario. No se confirmaron directamente desde el PDF oficial: formatos nativos exactos aceptados por el motor de impresión (p. ej. si acepta PDF y/o PWG-Raster/URF de forma nativa vía IPP), ni el detalle completo de "HP PCL 3 GUI" como único lenguaje soportado.
- V3: No se pudo cargar la página de soporte oficial de HP (support.hp.com) por timeout, ni el índice oficial de dispositivos soportados de HPLIP (developers.hp.com) por error 403. No se confirmó directamente en fuente oficial de HP el nivel exacto de soporte HPLIP (hpcups, hpaio, fax) para este modelo específico, más allá de la mención en las notas de versión de HPLIP 3.21.8.
- V4: No se encontró una entrada específica y verificable del Smart Tank 750 en la base de datos pública de OpenPrinting (openprinting.org) que confirme su clasificación como impresora "driverless".
- V5: No se pudo verificar si la impresora acepta JPEG directamente vía IPP (formato común en impresión driverless) — ninguna fuente consultada lo menciona explícitamente para este modelo.
- V6: No se pudo confirmar si hay contraseña de administrador configurada por defecto en el servidor web embebido (Embedded Web Server), ni límites documentados de la interfaz IPP/API para consulta de estado (niveles de tinta, atascos, cola) — esto requiere acceso directo al dispositivo, fuera del alcance permitido para esta investigación.

---

## R2 · ZKAccess 3.5 y PullSDK: qué expone y por qué vía

### Fuentes consultadas
- Archivo local: `ZKAccess3.5-Security-System-user-manual-V3.1.1.md` (manual de usuario ZKAccess 3.5, versión de software 3.5.3 Build0001+, referencia Pull SDK V2.2.0.205+ y Standalone SDK V6.2.5.31+).
- Archivo local: `PullSDK-User-Guide-EN-V2-0-201201-1-doc.md` (guía de PullSDK versión 2.0, enero 2012, soporta PullSDK 2.2.0.169 y superior).
- Web pública: https://www.zkteco.com/en/ZKAccess_3/ZKAccess3.5 (página oficial del producto ZKAccess3.5).
- Web pública: https://github.com/hmojicag/ZKTecoStandAlonePullSDK (repositorio con Standalone SDK 6.3.1.37, que incluye Pull SDK 2.2.0.219).
- Web pública: https://www.nuget.org/packages/ZKTecoStandAlonePullSDKx64 (paquete NuGet, versión 6.3.1.37).
- Web pública: https://www.zkteco.com/en/download_catgory/46.html (centro de descargas oficial ZKTeco, referenciado en resultados de búsqueda; no se navegó el contenido interno, solo su existencia como referencia).

### Hechos

#### Software ZKAccess 3.5

- H1: ZKAccess 3.5 es un sistema de gestión C/S (cliente-servidor) para control de acceso, que también puede generar reportes de asistencia usando los mismos datos del panel de acceso, para no duplicar recursos del dispositivo. Fuente: manual local, sección 1.1 "Functions Instruction" y sección "6.1 Work principle" (línea 407).
- H2: Bases de datos soportadas oficialmente por el software: **Microsoft Access** (por defecto) y **MS SQL Server 2005**. El manual no menciona MySQL, Firebird u otro motor. Fuente: manual local, línea 141 y sección 9.2.1 "Set Database" (línea 984).
- H3: El sistema requiere Windows XP/2003/Vista/7/8/8.1 como sistema operativo. No se menciona compatibilidad con Linux ni macOS en ningún punto del manual. Fuente: manual local, línea 141.
- H4: Configuración de hardware recomendada: CPU 2.0GHz+, RAM 1GB+, 10GB+ de espacio disponible, partición NTFS recomendada. Fuente: manual local, línea 141.
- H5: El software gestiona hasta 30,000 personas y soporta la conexión de hasta 100 dispositivos en configuración estándar. Fuente: manual local, línea 137.
- H6: Módulos del sistema: Personnel System (departamentos y personal), Device System (comunicación y gestión de dispositivos), Access Control System (niveles y horarios de apertura de puertas), System Settings (usuarios del sistema, roles, respaldo/inicialización de base de datos), y Time & Attendance. Fuente: manual local, línea 141 y sección 8 (línea 820).
- H7: Gestión de base de datos desde la interfaz: respaldo (Backup Database), restauración (Restore Database), configuración de ruta de respaldo, e inicialización (borrado y reseteo de tablas seleccionadas). No se documenta ningún mecanismo de acceso directo a la base de datos vía API HTTP/REST; el acceso es a través de la interfaz de escritorio del software o directamente contra el motor de base de datos (Access/SQL Server) si el integrador conoce su esquema. Fuente: manual local, sección 9.2-9.3 (líneas 978-1016).
- H8: Exportación de datos disponible desde la interfaz de usuario: los reportes de acceso ([Events Today], [Events the latest three days], [Events This week], [Events Last week], [Exception Events], y "custom report") se pueden exportar; también existe exportación de contenidos de dispositivo (formato EXCEL, PDF o TXT) vía [Device] > [More] > [Export]. Fuente: manual local, sección 7 "Access Control Reports" (línea 786) y línea 376.
- H9: No se documenta en el manual ninguna API web, servicio REST, ni mecanismo de integración oficial distinto de: (a) el motor de base de datos subyacente (Access/SQL Server), (b) exportación manual a Excel/PDF/TXT, y (c) el propio PullSDK que opera contra el dispositivo (no contra el software ZKAccess). No se encontró en la búsqueda pública ninguna mención de "API" o "web service" oficial para ZKAccess 3.5.
- H10 [Revisión N1: no verificado, se trata como vacío; ver V2]: ZKAccess3.5 aparece descrito por fuentes de reventa/distribución (no la página oficial directamente revisada en detalle) como discontinuado y reemplazado por "ZKBio CVAccess" en el catálogo actual de ZKTeco. Esto no fue verificado contra la página oficial de ZKTeco en detalle; se anota como hallazgo de búsqueda, no como hecho confirmado de primera fuente. Fuente: resultado de búsqueda web sobre https://www.zkteco.com/en/ZKAccess_3/ZKAccess3.5.

#### Dispositivo vía PullSDK

- H11: PullSDK es un conjunto de funciones en C que permiten acceder a los datos de los paneles de control de acceso **C3 y C4** directamente (es decir, al dispositivo, no al software ZKAccess). Fuente: guía PullSDK local, sección 1 "Overview" (línea 148).
- H12: Protocolos de comunicación soportados: **TCP/IP** y **RS485**. Para TCP/IP el puerto por defecto es **4370**. Para RS485 se especifica puerto serial (ej. COM1) y baudrate. Fuente: guía PullSDK local, función `Connect` (sección 4.1).
- H13: La conexión se realiza mediante la función `Connect(params)`, que recibe una cadena con protocolo, IP/puerto o puerto serial/baudrate, ID de dispositivo, timeout y contraseña de comunicación opcional. Retorna un handle si es exitosa. Fuente: guía PullSDK local, sección 4.1.
- H14: Funciones principales del SDK: `Connect`/`Disconnect` (conexión), `SetDeviceParam`/`GetDeviceParam` (parámetros del controlador, ej. ID de dispositivo, tipo de sensor de puerta, tiempo de accionamiento de cerradura), `ControlDevice` (control de acciones: abrir/cerrar salida de puerta, cancelar alarma, reiniciar dispositivo, habilitar/deshabilitar estado de apertura normal), `SetDeviceData`/`GetDeviceData`/`GetDeviceDataCount`/`DeleteDeviceData` (lectura, escritura y borrado de registros en tablas del dispositivo), `GetRTLog` (eventos en tiempo real y estado de puertas/alarmas), `SearchDevice`/`ModifyIPAddress` (búsqueda y configuración de red vía broadcast UDP), `PullLastError` (código de error), `SetDeviceFileData`/`GetDeviceFileData` (transferencia de archivos, ej. firmware, archivos de usuario/registro), `ProcessBackupData` (procesamiento de archivos de respaldo, ej. desde SD card). Fuente: guía PullSDK local, sección 4 completa (líneas 166-268).
- H15: Tablas de datos accesibles vía `GetDeviceData`/`SetDeviceData`/`DeleteDeviceData` (Attached Table 4): `user` (información de tarjetas/personas: CardNo, Pin, Password, Group, StartTime, EndTime), `userauthorize` (privilegios de acceso: Pin, AuthorizeTimezoneId, AuthorizeDoorId), `holiday` (días festivos), `timezone` (franjas horarias), `transaction` (**tabla de eventos de control de acceso**: Cardno, Pin, Verified, DoorID, EventType, InOutState, Time_second), `firstcard` (apertura por primera tarjeta), `multicard` (apertura por múltiples tarjetas), `inoutfun` (tabla de control de linkage/E-S auxiliar), `templatev10` (plantillas biométricas: Size, UID, PIN, FingerID, Valid, Template, Resverd, EndTag). Fuente: guía PullSDK local, sección 5.4 "Attached Table 4" (líneas 417-536).
- H16: `GetRTLog` obtiene eventos en tiempo real generados por el equipo (hasta 30 registros en caché del dispositivo) y también el estado de puertas/alarmas cuando no hay eventos pendientes. El formato de datos distingue entre registros de "evento en tiempo real" y registros de "estado de puerta/alarma" según un bit específico en la respuesta. Fuente: guía PullSDK local, sección 4.10 y 5.7 (líneas 216-218, 623-653).
- H17: La tabla `transaction` (eventos de acceso) usa códigos `EventType` documentados en la Tabla 6 (Attached Table 6), con más de 40 tipos de eventos normales y anómalos: apertura normal, apertura por horario, contraseña de emergencia/duress, tarjeta no registrada, tarjeta expirada, error de contraseña, anti-passback, interlock, apertura forzada, puerta abierta/cerrada correctamente, inicio de dispositivo, entre otros. Fuente: guía PullSDK local, sección 5.6 (líneas 583-611).
- H18: Instalación del SDK: los archivos DLL necesarios (`plcommpro.dll` y sus dependencias `plcomms.dll`, `plrscomm.dll`, `pltcpcomm.dll`, `rscagent.dll`) se instalan en el directorio de sistema de **Windows** (`windows/system32`). No se documenta versión para Linux en esta guía. Fuente: guía PullSDK local, sección 3 "Installation" (línea 156) y Tabla 1 (línea 274).
- H19: Los ejemplos de código de la guía están en Python (usando `windll.LoadLibrary` — específico de Windows) y C#. Esto refuerza que la guía asume un entorno Windows nativo (DLLs de 32/64 bits cargadas vía `ctypes.windll`, exclusivo de Windows). Fuente: guía PullSDK local, ejemplos en sección 4.1 y siguientes.
- H20: Existe un "Standalone SDK", distinto de PullSDK, para dispositivos de tipo "Standalone SDK Machine" (equipos independientes, identificados con fondo amarillo en la interfaz), que usa su propio protocolo de comunicación y no depende de si el dispositivo está en red. El manual de ZKAccess 3.5 distingue explícitamente entre dispositivos "Pull" (paneles de acceso, controlados por PullSDK) y dispositivos "Standalone SDK". Fuente: manual local, línea 5 y línea 282.
- H21: Según fuentes públicas (GitHub, NuGet), existe una versión más reciente del Standalone SDK, **6.3.1.37**, que incluye **PullSDK 2.2.0.219** — más nueva que la versión 2.2.0.169+ referenciada en la guía local de 2012 y que la versión 2.2.0.205+ referenciada en el manual de ZKAccess 3.5. Hay paquetes NuGet (`ZKTecoStandAlonePullSDKx64`) que empaquetan esta versión para desarrollo en .NET/Windows. Fuente: https://github.com/hmojicag/ZKTecoStandAlonePullSDK, https://www.nuget.org/packages/ZKTecoStandAlonePullSDKx64.

### Contradicciones o desactualización

- C1: La guía de PullSDK es de 2012 (versión 2.0, soporta PullSDK 2.2.0.169+) y el manual de ZKAccess 3.5 es v3.1.1 (referencia PullSDK 2.2.0.205+). La búsqueda pública muestra una versión aún más nueva del SDK (2.2.0.219, empaquetada en Standalone SDK 6.3.1.37) disponible vía terceros (GitHub/NuGet), no vía un documento oficial actualizado de ZKTeco que se haya podido leer en detalle en esta investigación. No se pudo confirmar si la interfaz de funciones (`Connect`, `GetDeviceData`, tablas disponibles, etc.) cambió entre 2.2.0.169/2.2.0.205 y 2.2.0.219, porque no se tuvo acceso a un changelog oficial.
- C2: Fuentes de reventa/distribución indican que ZKAccess3.5 está discontinuado y reemplazado por "ZKBio CVAccess" en el catálogo actual de ZKTeco. Esto no se contrastó directamente leyendo el contenido completo de la página oficial (solo aparece en el resumen de búsqueda), por lo que se marca como hallazgo no verificado de primera mano.

### Vacíos

- V1: No se pudo verificar si existe una versión de PullSDK o de sus DLLs para Linux; tanto la guía local como los ejemplos de código (Python vía `windll`, C# vía P/Invoke de DLL) apuntan exclusivamente a Windows, y no se encontró documentación pública oficial que mencione soporte Linux para PullSDK.
- V2: No se pudo confirmar con una fuente oficial de ZKTeco (no de terceros/revendedores) si ZKAccess3.5 está efectivamente discontinuado y cuál es el estado actual de soporte; solo se cuenta con un resumen de búsqueda sobre la página oficial, no una lectura directa y completa de su contenido actual.
- V3: No se encontró documentación pública ni en los archivos locales sobre una API REST/HTTP oficial de ZKAccess 3.5 o de PullSDK. La única vía de integración documentada es (a) acceso directo al motor de base de datos del software (Access/SQL Server) si se conoce su esquema interno —esquema que **no** está documentado en el manual de usuario consultado—, (b) exportación manual de reportes (Excel/PDF/TXT), y (c) PullSDK contra el dispositivo físico. No se pudo determinar el esquema de tablas interno de la base de datos del software ZKAccess3.5 (distinto de las tablas del dispositivo vía PullSDK, que sí están documentadas en H15) porque el manual de usuario no lo detalla; sería necesario el script `sqlserver.sql` mencionado en el manual (línea 984), que no está disponible en las fuentes consultadas.
- V4: No se pudo verificar si la versión 2.2.0.219 de PullSDK (hallada vía terceros) agrega, quita o modifica tablas/funciones respecto a las documentadas en la guía v2.0 de 2012, por falta de un changelog oficial accesible en esta investigación.

---

## R3 · Neumorphism y contraste en móvil

### Fuentes consultadas
- W3C WCAG 2.2 — Understanding SC 1.4.11 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C WCAG 2.2 — Understanding SC 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C WCAG 2.2 — Understanding SC 1.4.6 Contrast (Enhanced): https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html
- W3C WCAG 2.2 — Understanding SC 2.4.11 Focus Not Obscured (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- W3C WCAG 2.2 — Understanding SC 2.4.13 Focus Appearance: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- Medium (Xurxe Toivo García) — "For a more accessible Neumorphism (Soft UI)": https://medium.com/@xurxe/accessible-neumorphism-soft-ui-992286900bfa
- UX Collective (Michael J. Fordham) — "Neumorphism: can we make it more accessible?": https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28
- Built In — "What Neumorphism Style Says About the State of UI Design": https://builtin.com/articles/neumorphism-accessibility
- CodeFronts — "Accessible Neumorphism That Passes Contrast": https://codefronts.com/design-styles/css-neumorphism/accessible-neumorphism-that-passes-contrast/
- WebAIM — Contrast Checker: https://webaim.org/resources/contrastchecker/

### Hechos

**Contraste de texto (WCAG 2.2)**
- H1: SC 1.4.3 (Contrast Minimum, nivel AA) exige contraste mínimo de **4.5:1** para texto normal, y **3:1** para texto grande (definido como 18pt / ~24px, o 14pt/~18.67px en negrita). Texto decorativo, inactivo, de logotipo o no visible queda exento. Fuente: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- H2: SC 1.4.6 (Contrast Enhanced, nivel AAA) exige **7:1** para texto normal y **4.5:1** para texto grande. Es un nivel más estricto que AA, pensado para compensar pérdida de sensibilidad al contraste equivalente a visión 20/80. Fuente: https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html

**Contraste no textual — el criterio más relevante para neumorphism**
- H3: SC 1.4.11 (Non-text Contrast, nivel AA) exige contraste de al menos **3:1 contra el color adyacente** para: (a) la información visual necesaria para identificar componentes de interfaz y sus estados (bordes de botones/inputs, indicador de foco, estado marcado de un checkbox, posición de un toggle), y (b) objetos gráficos necesarios para entender el contenido. No se exige que todo el componente cumpla el ratio, solo las partes que identifican su límite o estado. Componentes inactivos quedan exentos. Cita textual: "The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s): User Interface Components... Graphical Objects...". Fuente: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

**Foco de teclado**
- H4: SC 2.4.11 (Focus Not Obscured Minimum, nivel AA, nuevo en WCAG 2.2) exige que el indicador de foco de teclado no quede completamente oculto por contenido creado por el autor (headers pegajosos, banners, chats). Ocultamiento parcial se tolera en AA; ocultamiento total es una falla. Fuente: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- H5: SC 2.4.13 (Focus Appearance, nivel AAA, nuevo en WCAG 2.2) exige que el indicador de foco cubra un área al menos equivalente a un perímetro de 2px CSS alrededor del componente sin foco, Y tenga un contraste de al menos **3:1** entre los mismos píxeles en estado con foco y sin foco. Cita textual: "is at least as large as the area of a 2 CSS pixel thick perimeter of the unfocused component" y "has a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states". Fuente: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html

**Por qué el neumorphism suele fallar estos criterios**
- H6: El rasgo definitorio del neumorphism —elementos extruidos con el mismo color que el fondo, diferenciados solo por sombras claras/oscuras de bajo contraste— hace que no exista contraste real en el límite del componente, por lo que falla 1.4.11 (3:1 contra color adyacente) de forma sistemática. Fuente: https://medium.com/@xurxe/accessible-neumorphism-soft-ui-992286900bfa
- H7: Los estados de botones (presionado/activo) en neumorphism suelen distinguirse únicamente invirtiendo la dirección de la sombra (de extruido a hundido/inset), sin cambio de color ni borde, lo cual no aporta la información de estado exigida por 1.4.11 para usuarios con baja visión. Fuente: https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28
- H8: El texto colocado directamente sobre la superficie neumórfica (mismo tono que el fondo) frecuentemente cae por debajo del mínimo 4.5:1 de 1.4.3, dejando a usuarios de baja visión sin poder identificar qué es interactivo. Fuente: https://builtin.com/articles/neumorphism-accessibility

**Técnicas documentadas para mantener accesible un diseño neumórfico**
- H9: Añadir un borde sutil (frecuentemente 1px) en un tono más claro u oscuro, alineado con la dirección de la sombra, para reforzar visualmente el límite del componente sin abandonar el aspecto suave. Fuente: https://codefronts.com/design-styles/css-neumorphism/accessible-neumorphism-that-passes-contrast/
- H10: Usar colores de acento (mayor contraste que el resto de la paleta) de forma selectiva en elementos interactivos importantes, y para indicar cambios de estado (activo/hover/seleccionado), en vez de depender solo de la sombra. Fuente: https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28
- H11: Colocar el texto sobre una superficie de mayor contraste (no directamente sobre el panel neumórfico de bajo contraste) como técnica de mitigación documentada. Fuente: https://builtin.com/articles/neumorphism-accessibility
- H12: Para el estado presionado, invertir ambas sombras a "inset" (hundido) como metáfora física de pulsado — técnica documentada, pero por sí sola no basta para cumplir 1.4.11 si no hay además cambio de color o borde (ver H7). Fuente: https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28

**Herramientas públicas para medir contraste**
- H13: WebAIM Contrast Checker es una herramienta gratuita que muestra el ratio de contraste exacto y si pasa/falla los niveles AA y AAA para texto normal, texto grande, y también los requisitos de contraste no textual de WCAG 2.1/2.2 (1.4.11). Fuente: https://webaim.org/resources/contrastchecker/

### Vacíos
- V1: No se encontró una fuente pública oficial que dé un valor numérico específico de "compensación de brillo" o un ratio de contraste ajustado recomendado para uso bajo luz solar directa en móvil. Los artículos consultados mencionan cualitativamente que el brillo/reflejo reduce el contraste percibido, pero WCAG 2.2 no define un ratio distinto para condiciones de luz solar — los ratios de 1.4.3/1.4.11/1.4.6 son los mismos independientemente del entorno de visualización.
- V2: No se pudo verificar con una fuente primaria (W3C o estudio citable) un umbral cuantitativo específico de "cuánto" se degrada un ratio de contraste en exteriores (ej. "3.8:1 baja a 2.5:1"); esa cifra apareció solo en contenido de blog sin cita primaria, así que no se incluye como hecho verificado.
- V3: No se encontró guía específica de W3C/WCAG dedicada exclusivamente a "tamaño de pantalla móvil" como factor de contraste; los criterios de contraste son agnósticos al tamaño de pantalla o dispositivo.
- V4: No se investigó ni se afirma nada sobre paletas de color, valores hexadecimales o diseño específico de la interfaz de Works — está fuera del alcance de esta pregunta.

---

## R4 · Opciones de entrada sin fricción

### Fuentes consultadas
- NIST SP 800-63B / 800-63B-4 (Digital Identity Guidelines): https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ y https://pages.nist.gov/800-63-3/sp800-63b.html
- NIST SP 800-63B-4 (PDF oficial): https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63B-4.pdf
- NIST SP 800-63-4 gestión de sesión: https://pages.nist.gov/800-63-4/sp800-63b/session
- FIDO Alliance, Passkeys: https://fidoalliance.org/passkeys/
- OWASP Mobile Application Security (MASTG/MASVS), autenticación local: https://mas.owasp.org/MASTG/0x06f-Testing-Local-Authentication/ , https://mas.owasp.org/MASVS/controls/MASVS-AUTH-2/
- OWASP Session Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- Meta for Developers, precios de la WhatsApp Business Platform: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing
- Meta for Developers, plantillas de autenticación: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates/
- Google for Developers, Sign in with Google: https://developers.google.com/identity/siwg y https://developers.google.com/identity/openid-connect/openid-connect
- WorkOS, guía de magic links: https://workos.com/blog/a-guide-to-magic-links
- Postmark, guía de magic links: https://postmarkapp.com/blog/magic-links
- TypingDNA, análisis de NIST 800-63B Rev.4 sobre SMS OTP: https://blog.typingdna.com/nist-sp-800-63b-rev-4-sms-otp-is-now-a-restricted-authenticator-but-we-have-the-fix/
- Vectra AI, riesgos de MFA por SMS: https://www.vectra.ai/blog/the-hidden-risks-of-sms-based-multi-factor-authentication
- OneUpTime, email OTP como segundo factor y límites de 800-63B: https://oneuptime.com/blog/post/2026-08-29-is-email-otp-really-a-second-factor-how-to-keep-authentication-channels-independent/view
- Corbado, problemas de passkeys después del lanzamiento: https://www.corbado.com/blog/passkey-day-2-problems
- guptadeepak.com, playbook de despliegue de passkeys 2026: https://guptadeepak.com/passkeys-at-scale-the-complete-enterprise-deployment-playbook-2026/
- Wati.io, categorías de plantillas de WhatsApp: https://support.wati.io/en/articles/11463465-whatsapp-template-categories-explained-utility-authentication-and-marketing
- Wati.io, prerrequisitos de la API de WhatsApp: https://www.wati.io/en/blog/whatsapp-api-prerequisites/
- 360dialog, plantillas de autenticación zero-tap: https://docs.360dialog.com/docs/resources/authentication-messages/zero-tap-authentication-templates

### Hechos por opción

#### Magic link por correo
- Cómo funciona: el servidor genera una URL de un solo uso con un token embebido y la envía al correo del usuario; al hacer clic, el servidor valida el token y otorga acceso sin contraseña. Fuente: https://workos.com/blog/a-guide-to-magic-links
- Fricción: reemplaza "algo que sabes" (contraseña) por "algo que tienes" (acceso al correo), reduce fricción de recordar contraseñas, pero depende de que el usuario cambie de app a su cliente de correo y regrese. Los escáneres de seguridad corporativos (p. ej. en Outlook empresarial) pueden "hacer clic" en el enlace automáticamente e invalidar el token antes de que el usuario lo use. Fuente: https://securityboulevard.com/2026/05/are-magic-links-secure-a-technical-deep-dive-into-email-based-authentication/
- Seguridad y riesgos: NIST SP 800-63B no permite el correo electrónico como canal de autenticación fuera de banda ("out-of-band"): la sección 5.1.3.1 establece que métodos que no prueban posesión de un dispositivo específico, como VOIP o correo, NO deben usarse para autenticación fuera de banda. Un magic link enviado a una cuenta protegida solo por contraseña (o por SMS OTP) hereda la debilidad de esa cuenta: un solo SIM swap puede desbloquear tanto el correo como cualquier código enviado a él. Riesgos adicionales: phishing (el atacante inicia el flujo de magic link con el correo de la víctima y la engaña para que reenvíe o confirme el enlace) y reenvío/uso compartido del enlace. Mitigación reportada: un solo uso y expiración corta (p. ej. 15 minutos). Fuente: https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63B-4.pdf ; https://oneuptime.com/blog/post/2026-08-29-is-email-otp-really-a-second-factor-how-to-keep-authentication-channels-independent/view ; https://securityboulevard.com/2026/05/are-magic-links-secure-a-technical-deep-dive-into-email-based-authentication/
- Dependencias y costos: depende de un proveedor de correo transaccional (envío confiable, no marcado como spam) y de la seguridad de la cuenta de correo del usuario. No se encontró fuente pública con un costo estándar de envío de magic links (varía por proveedor de email transaccional; no verificado aquí).

#### Passkeys (WebAuthn/FIDO2)
- Cómo funciona: usa un par de llaves criptográficas; la llave privada permanece en el dispositivo o llave de seguridad del usuario y el sitio solo guarda la llave pública. El navegador muestra la UI nativa del sistema operativo, el usuario se verifica localmente (Face ID, Touch ID, PIN de Windows Hello), el autenticador firma un desafío con la llave privada y el servidor verifica la firma contra la llave pública registrada. WebAuthn es la API del navegador; FIDO2 combina WebAuthn con el protocolo CTAP2 usado por llaves de seguridad físicas. Fuente: https://fidoalliance.org/passkeys/ ; https://alflokken.github.io/posts/understanding-fido2-passkeys/
- Fricción: en el "día 1" (primer registro y uso) la fricción es baja en dispositivos compatibles. En el "día 2" aparecen los problemas: dispositivo nuevo sin sincronización, teléfono perdido con sincronización desactivada, computadoras compartidas (PC familiar, kiosco) donde la biometría personal no aplica, y usuarios empresariales que rechazan guardar credenciales de trabajo en su iCloud personal. El comportamiento de sincronización difiere entre ecosistemas (Apple usa iCloud Keychain, Google usa Google Password Manager, Microsoft tiene su propia implementación), lo que genera fricción al moverse entre ecosistemas: una passkey creada en el ecosistema de Apple no puede usarse en un navegador no-Apple sin sincronizar antes vía iCloud. Se reportaron fallas graves en dispositivos Android no-Pixel con Android 14 (códigos de error opacos sin guía de recuperación). Fuente: https://www.corbado.com/blog/passkey-day-2-problems ; https://guptadeepak.com/passkeys-at-scale-the-complete-enterprise-deployment-playbook-2026/
- Seguridad y riesgos: se consideran resistentes a phishing porque nada reutilizable cruza la red y la credencial está atada al origen real del sitio web (origin binding); el navegador se niega a usar la credencial en un dominio distinto al registrado, incluso si el usuario es engañado para visitar un sitio falso. Riesgo principal reportado: la recuperación de cuenta es "el problema no resuelto más difícil" — al no haber un secreto que resetear (la credencial está atada al dispositivo), si el usuario pierde todos los dispositivos con la passkey se necesita una ruta de respaldo diseñada de antemano (contraseñas durante la transición, magic links verificados, una segunda passkey en otro dispositivo, o recuperación de la plataforma). Fuente: https://www.oloid.com/blog/fido-2-webauthn ; https://www.corbado.com/blog/passkey-day-2-problems
- Dependencias y costos: depende de que el navegador/sistema operativo del usuario soporte WebAuthn/FIDO2 y de un proveedor de sincronización de passkeys (iCloud Keychain, Google Password Manager, etc.). No se encontró un costo público directo de implementar passkeys per se (el costo depende del proveedor de identidad/backend usado); las empresas con baja estrategia de despliegue reportan menos de 5% de adopción real pese a implementaciones técnicamente correctas. Fuente: https://guptadeepak.com/passkeys-at-scale-the-complete-enterprise-deployment-playbook-2026/

#### OTP por SMS
- Cómo funciona: se envía un código temporal de un solo uso por mensaje de texto a un número de teléfono pre-registrado; el usuario lo ingresa manualmente en la app. Fuente: https://www.authgear.com/post/sms-otp-vulnerabilities-and-alternatives/
- Fricción: requiere que el usuario cambie de app para leer el SMS y regrese a escribir el código manualmente; se describe explícitamente como generador de "fricción en la experiencia de usuario" además de los riesgos de seguridad. Fuente: https://www.authgear.com/post/sms-otp-vulnerabilities-and-alternatives/
- Seguridad y riesgos: NIST SP 800-63B-4 formalmente clasifica los OTP por SMS/PSTN como "autenticador restringido" (restricted authenticator) — la primera vez que NIST crea esta categoría explícita, lo que implica obligaciones adicionales: evaluación de riesgo documentada, ruta de migración y notificación al usuario. Si se usa la PSTN para verificación fuera de banda, el verificador DEBE confirmar que el número de teléfono pre-registrado está asociado a un dispositivo físico específico, y DEBERÍA considerar indicadores de riesgo como cambio de dispositivo, cambio de SIM o portabilidad numérica. Riesgos conocidos: SIM swapping (el atacante asume la identidad del cliente ante la operadora o soborna a un empleado para recibir los mensajes del número objetivo, incluyendo los OTP), vulnerabilidades de protocolo SS7, e interceptación tipo MITM/relay. Los autenticadores fuera de banda/OTP de entrada manual NO se consideran resistentes a suplantación del verificador porque la entrada manual no ata la salida del autenticador a la sesión específica que se autentica. Fuente: https://blog.typingdna.com/nist-sp-800-63b-rev-4-sms-otp-is-now-a-restricted-authenticator-but-we-have-the-fix/ ; https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63B-4.pdf ; https://www.vectra.ai/blog/the-hidden-risks-of-sms-based-multi-factor-authentication
- Dependencias y costos: depende de un proveedor de SMS/carrier (operadora telefónica) y de un gateway de envío de SMS transaccional. No se encontró en las fuentes consultadas un precio público estándar por SMS OTP fuera del contexto de WhatsApp (varía por proveedor y país; no verificado aquí).

#### OTP por WhatsApp (plantillas de autenticación de WhatsApp Business)
- Cómo funciona: las plantillas de autenticación de la WhatsApp Business Platform envían un código (OTP) para autenticar usuarios en inicio de sesión, registro o recuperación de cuenta, sin que el usuario inicie la conversación en WhatsApp. Existen tres variantes de botón: "Copy Code" (el usuario copia el código y lo pega manualmente en la app), "One-Tap Autofill" (el botón carga automáticamente el código en la app; solo disponible en Android, requiere cambios de código en la app y un "handshake" con el hash de la llave de firma de la app) y "Zero-Tap" (el usuario recibe el código sin salir de la app; el cliente de WhatsApp transmite el código y la app lo captura con un receptor de difusión, sin ningún botón). El componente de plantilla incluye texto fijo tipo "<CÓDIGO> es tu código de verificación", un descargo de seguridad opcional y una advertencia de expiración opcional; el TTL por defecto de estas plantillas es de 10 minutos. Fuente: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates/ ; https://docs.360dialog.com/docs/resources/authentication-messages/zero-tap-authentication-templates
- Fricción: menor que SMS en el mejor caso (zero-tap: cero interacción manual) pero zero-tap y one-tap dependen de integración técnica específica en la app y, en el caso de one-tap, solo funcionan en Android. Copy-code tiene fricción similar a SMS (cambiar de app y pegar el código manualmente). Fuente: https://docs.360dialog.com/docs/resources/authentication-messages/zero-tap-authentication-templates
- Seguridad y riesgos: no se encontró en las fuentes consultadas una postura específica de NIST 800-63B sobre OTP entregado vía WhatsApp. Al ser un OTP de entrada manual (en las variantes copy-code) comparte la limitación general de NIST sobre autenticadores fuera de banda de entrada manual (no resistentes a suplantación del verificador, ver sección SMS). Vacío: no se encontró un análisis público específico de riesgos de intercepción o SIM-binding para OTP vía WhatsApp equivalente al de SMS.
- Dependencias y costos: requiere una WhatsApp Business Account (WABA) verificada en Meta Business Manager, un número de teléfono dedicado no vinculado previamente a una cuenta de WhatsApp personal, aprobación de plantilla por Meta (revisión automatizada en horas o manual de 2 a 4 días hábiles), y opcionalmente un proveedor BSP (Business Solution Provider). El costo se cobra por mensaje de plantilla entregado: los mensajes de autenticación (OTP) van desde aproximadamente $0.0014 USD por mensaje en India hasta más de $0.05 USD en algunos mercados europeos; en general las tarifas de utilidad y autenticación van de $0.0008 USD (Colombia) a $0.0550 USD (Alemania). Desde el 1 de julio de 2025 existen descuentos por volumen para plantillas de utilidad y autenticación. Existe una tarifa "Authentication-International" más alta cuando el OTP se envía a un país distinto al registrado en la WABA del remitente. Fuente: https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing ; https://www.wati.io/en/blog/whatsapp-api-prerequisites/

#### Enlace de acceso enviado por WhatsApp
- Cómo funciona: no se encontró documentación pública de Meta que describa explícitamente un "enlace de acceso" (login link, distinto de un código OTP) como tipo de contenido soportado dentro de una plantilla de autenticación. Las plantillas de autenticación de Meta están diseñadas específicamente para códigos/passcodes, no para URLs de sesión. Fuente: https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates/
- Fricción: un enlace enviado por una plantilla de Utilidad (utility) podría, en principio, funcionar como los magic links por correo (clic para entrar), pero no se encontró fuente pública que documente esta variante ni su fricción real en la práctica.
- Seguridad y riesgos: vacío — no se encontró fuente pública que analice riesgos de seguridad específicos de un enlace de acceso (magic link) entregado vía WhatsApp, a diferencia del caso de correo (NIST 800-63B) o del OTP por WhatsApp (arriba).
- Dependencias y costos: las mismas dependencias de infraestructura que el OTP por WhatsApp (WABA verificada, número dedicado, aprobación de plantilla), pero bajo la categoría de plantilla "Utility" en vez de "Authentication", ya que Meta reserva la categoría Authentication para passcodes. Las plantillas de utilidad deben ser estrictamente transaccionales y no pueden incluir contenido promocional. Fuente: https://support.wati.io/en/articles/11463465-whatsapp-template-categories-explained-utility-authentication-and-marketing

#### Sesión de larga duración / "recordar dispositivo"
- Cómo funciona: el servidor emite una cookie de sesión (u otro token) que se mantiene vigente por un periodo extendido para evitar que el usuario vuelva a autenticarse en cada visita. Las cookies del navegador son el mecanismo predominante para crear y rastrear una sesión. Fuente: https://pages.nist.gov/800-63-4/sp800-63b/session
- Fricción [Revisión N2: inferencia sin fuente, se trata como vacío]: es la opción de menor fricción posible una vez configurada (el usuario no interactúa en absoluto en visitas subsecuentes). Fuente: inferencia directa del mecanismo descrito; no hay una cita textual específica sobre "fricción cero" en las fuentes consultadas.
- Seguridad y riesgos: NIST SP 800-63-4 indica que las cookies no son autenticadores pero son adecuadas como secretos de corto plazo para la duración de una sesión, y que las cookies y funciones tipo "recordar mi navegador" NO DEBEN usarse en lugar de la autenticación, excepto como reautenticación cuando se excedió el límite de inactividad pero no el límite de tiempo total. Una cookie de sesión robada permite a un atacante suplantar al usuario sin volver a ingresar credenciales ni completar MFA; las aplicaciones que emiten cookies de larga duración sin invalidación por sesión ni telemetría no pueden revocarlas selectivamente. Atributos recomendados: Secure (solo HTTPS), HttpOnly (inaccesible vía JavaScript) y SameSite (protección CSRF). OWASP recomienda tiempos de inactividad cortos (2-5 minutos) para aplicaciones de datos de alto riesgo y más largos (15-30 minutos) para aplicaciones de bajo riesgo. Fuente: https://pages.nist.gov/800-63-4/sp800-63b/session ; https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
- Dependencias y costos: no depende de servicios externos más allá de la propia infraestructura del servidor/backend que emite y valida la cookie/token. No se encontró un costo asociado, al ser un mecanismo propio de la aplicación.

#### PIN local en el dispositivo
- Cómo funciona: la app autentica al usuario contra credenciales almacenadas localmente en el dispositivo mediante un PIN, contraseña o características biométricas (rostro, huella). En Android existen dos mecanismos soportados por el runtime: el flujo "Confirm Credential" (disponible desde Android 6.0, evita que el usuario tenga que ingresar contraseñas específicas de la app además del bloqueo de pantalla, y puede usarse para desbloquear material criptográfico del AndroidKeystore) y el flujo de autenticación biométrica. Fuente: https://mas.owasp.org/MASTG/0x05f-Testing-Local-Authentication/
- Fricción [Revisión N2: inferencia sin fuente, se trata como vacío]: baja — es un gesto rápido (PIN corto o biometría) en el propio dispositivo, sin depender de red ni de canales externos (SMS, correo, WhatsApp). Fuente: inferencia directa del mecanismo descrito.
- Seguridad y riesgos: OWASP recomienda que la autenticación local siempre se refuerce en un endpoint remoto o se base en un primitivo criptográfico, ya que un atacante puede evadir fácilmente la autenticación local si no se retorna ningún dato del proceso de autenticación. Recomienda usar mecanismos de almacenamiento seguro específicos de la plataforma (Keychain en iOS, Keystore en Android) y métodos de autenticación biométrica soportados por la plataforma con un PIN como respaldo. Indica explícitamente no permitir PINs cortos como de 4 dígitos. La autenticación biométrica mediante CryptoObject no puede evadirse, incluso en dispositivos con rooteo, porque la llave del KeyStore solo puede usarse tras una autenticación biométrica exitosa. Fuente: https://mas.owasp.org/MASTG/0x05f-Testing-Local-Authentication/ ; https://mas.owasp.org/MASVS/controls/MASVS-AUTH-2/
- Dependencias y costos: depende de las capacidades nativas del sistema operativo del dispositivo (Keychain/iOS, Keystore/Android) y no de un proveedor externo. No implica costos de envío de mensajes. Es un mecanismo de re-autenticación local, no reemplaza necesariamente una autenticación inicial contra el servidor (vacío: las fuentes no aclaran si por sí solo basta como único factor de acceso remoto).

#### Inicio de sesión con Google u otro proveedor
- Cómo funciona: se construye sobre los estándares OAuth 2.0 y OpenID Connect (OIDC). OAuth 2.0 otorga permiso de acceso a recursos; OIDC es la capa de identidad sobre OAuth 2.0 que verifica quién es el usuario mediante un "ID token". El primer paso es crear un token de estado único que se mantiene entre la app y el cliente del usuario, el cual luego se coteja con la respuesta de autenticación para verificar que la solicitud proviene del usuario legítimo y no de un atacante. Fuente: https://developers.google.com/identity/siwg ; https://developers.google.com/identity/openid-connect/openid-connect
- Fricción: baja para usuarios que ya tienen sesión iniciada en su cuenta de Google en el dispositivo (flujo de pocos clics, sin crear ni recordar credenciales nuevas). No se encontró en las fuentes consultadas una cuantificación específica de fricción en móvil.
- Seguridad y riesgos: al delegar en la seguridad de la cuenta de Google, se reduce la dependencia de contraseñas propias y el riesgo de brechas basadas en credenciales, ya que la organización no almacena contraseñas directamente. El riesgo de seguridad queda entonces ligado a la seguridad de la cuenta del proveedor externo (Google) y a la correcta implementación del token de estado (anti-CSRF) en la app cliente. Fuente: https://developers.google.com/identity/siwg
- Dependencias y costos: depende de un proveedor de identidad externo (Google u otro) y de registrar la app en su consola de desarrolladores (Google Cloud / Google Identity). No se encontró en las fuentes consultadas un costo público asociado a "Sign in with Google" para el volumen de uso de un negocio pequeño (el servicio de autenticación en sí es gratuito según la documentación revisada, aunque no se verificó exhaustivamente para todos los escenarios).

### Vacíos
- V1: No se encontró documentación pública de Meta que confirme si un "enlace de acceso" (login link) puede enviarse mediante una plantilla de autenticación de WhatsApp, o si necesariamente debe canalizarse por una plantilla de Utilidad. Meta documenta las plantillas de Authentication exclusivamente para passcodes/OTP.
- V2: No se encontró un análisis de seguridad específico (tipo NIST o académico) sobre riesgos de interceptación, suplantación o SIM-binding para OTP o enlaces entregados vía WhatsApp, equivalente al que existe para SMS o correo.
- V3: No se encontró un costo público estándar de envío de SMS OTP fuera del contexto de plantillas de WhatsApp (depende del proveedor de SMS transaccional y del país; no verificado).
- V4: No se encontró en las fuentes consultadas un costo público específico de "Sign in with Google" para negocios pequeños con bajo volumen de usuarios.
- V5: No se encontró fuente pública que documente si un PIN local por sí solo (sin verificación remota) es suficiente como único mecanismo de entrada a un dashboard web, o si siempre debe combinarse con una autenticación inicial contra el servidor.

---

