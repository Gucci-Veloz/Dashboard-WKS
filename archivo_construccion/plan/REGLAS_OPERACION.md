# Reglas de operación · acceso, sesiones, cambios y reporte

Las dictó el usuario el 2026-09-26. Las aclaraciones que dio en la misma conversación están al final. Estas reglas son **fuente de verdad**, al mismo nivel que el handshake. KISS aplica, pero **no autoriza a eliminar, reinterpretar ni debilitar** ningún comportamiento. Si una regla necesita una definición más para poder implementarse, se reporta como vacío a la sesión maestra, no se supone.

## Acceso y autenticación
- El acceso se inicia solo bajo demanda de David o Grecia. Vania genera el acceso únicamente cuando la persona lo pide.
- El acceso es un **link con token de un solo uso**, asociado a la persona que lo pidió.
- El token expira **10 minutos** después de emitirse. Al entregarlo, Vania le dice a la persona que tiene 10 minutos para usarlo.
- El primer uso válido lo invalida, aunque le quede tiempo. Un token usado, vencido o inválido no se reutiliza. Si vence, la persona pide otro a Vania.
- Vania reconoce a la persona por su número de WhatsApp. Los números viven en la configuración del servidor, **nunca en git**. El número del desarrollador no recibe links: su acceso es el técnico (INT-16).

## Sesiones
- Una autenticación válida crea una sesión ligada a la persona y al dispositivo o navegador. Cada dispositivo tiene su propia sesión.
- Una sesión pertenece solo a su persona y no autoriza acciones de la otra.
- David y Grecia pueden tener sesiones válidas al mismo tiempo en varios dispositivos. Una sesión nueva no invalida las otras.
- Las sesiones vencen a las **18:00, hora de Querétaro** (`America/Mexico_City`), del mismo día en que se crearon. **Una sesión creada a las 18:00 o después vence a las 23:59 de ese día.**
- Mientras la sesión siga vigente, la persona puede cerrar y volver a abrir el Dashboard sin pedir otro token.
- No hay ícono en la pantalla de inicio.

## Varios dispositivos
- Todos los dispositivos trabajan sobre el mismo estado guardado.
- Una operación empezada en un dispositivo puede seguir en otro cuando el flujo lo permita.
- Usar varios dispositivos no crea copias del mismo registro. Al volver a consultar un registro, se ve su estado vigente.

## Captura manual y pre-registro
1. Lo que la persona escribe antes de pedir el cambio es **entrada no registrada**. Si cierra sin presionar Enter o el botón, **se pierde**, y eso es correcto.
2. Pedir el cambio (Enter, o un botón equivalente) lo convierte en **pre-registro**, y sale la ventana "**[Nombre], ¿deseas confirmar el cambio?**" con **Sí** y **No**.
3. Con **Sí**, el cambio se vuelve oficial y termina el proceso.
4. Con **No**, o si la persona sale o se descuida, el pre-registro **no se pierde**: queda como "**Cambio pendiente de confirmar**", visible desde cualquier dispositivo y se puede confirmar durante **24 horas**. Después se borra.
5. Un pre-registro sin confirmar **no modifica el dato oficial**. Uno vencido nunca puede modificarlo.
6. **Crear, modificar y borrar** siguen este mismo ciclo.
7. Al pedir un cambio hay una casilla opcional **"Observaciones"**. Su texto aparece en el reporte del día.

## Modificar registros existentes
- Solo un cambio confirmado modifica el valor oficial. El último cambio confirmado es el valor vigente.
- El valor anterior se conserva en el historial: valor anterior, valor nuevo, cuándo y quién.
- Cada registro tiene un solo estado vigente. Las versiones anteriores son solo trazabilidad.

## Posibles duplicados
- Al crear, si el registro nuevo podría ser uno que ya existe, el sistema no reemplaza el anterior ni crea el nuevo sin avisar. Dice: "**Ya existe un registro similar. ¿Quieres revisarlo antes de crear otro?**", con las opciones **revisar**, **cancelar** y **crear de todos modos**.
- Criterios aprobados:
  - **Inquilino:** mismo `titular`, sin contar mayúsculas, acentos ni espacios de más; o mismo `contacto` (teléfono).
  - **Oficina:** mismo `numero`.
  - **Contrato:** misma oficina, mismo inquilino y fechas que se enciman.
  - **Pago:** mismo contrato, mismo mes de `fecha_pago` y mismo `precio`.
- Estos criterios se revisan cuando llegue el Excel real (U-1).

## Cambios hechos por Vania
- **Sin una sesión activa de la persona que da la instrucción, Vania no puede modificar datos en su nombre.** La sesión de Grecia no autoriza instrucciones de David, ni al revés.
- El flujo:
  1. La persona le pide un cambio a Vania.
  2. Vania revisa si esa persona tiene una sesión válida.
  3. Si no la tiene, le manda el link.
  4. La persona entra.
  5. Vania ejecuta el cambio.
- El cambio pasa por las mismas reglas de pre-registro, confirmación, duplicados y trazabilidad. La confirmación se da en WhatsApp con un "**Sí**" o "**No**" por texto, sin botones, porque es WhatsApp Web.
- *Para la configuración de Vania (SOUL.md), no bloquea nada aquí:* Vania pregunta si hay alguna observación que registrar.

## Solicitante y ejecutor
- Todo cambio confirmado registra por separado al **solicitante** (quien decidió y pidió el cambio) y al **ejecutor** (quien lo hizo materialmente).
- Casos válidos:
  - Grecia pide, Grecia ejecuta.
  - Grecia pide, Vania ejecuta.
  - David pide, David ejecuta.
  - David pide, Vania ejecuta.
- El solicitante sale solo de la sesión, o de la persona que dio la instrucción a Vania. No es editable. Vania nunca aparece como solicitante.

## Reporte del día
- Tiene una fila por cada cambio **confirmado** del día, en hora de Querétaro. Los pendientes no aparecen.
- Columnas: ID del cambio, Fecha, Inquilino, Concepto, Observaciones, Solicitante, Ejecutor.
  - **Inquilino:** el relacionado, o "—" si no aplica.
  - **Concepto:** en pagos, el estatus (por ejemplo "Pagado" o "Moroso"). En lo demás, una frase corta como "Cambio de m²" o "Alta de inquilino".
- Se puede consultar cualquier día pasado. El historial crece cada día que hay cambios.
- Se abre con el botón "**Reporte del día**", junto a las áreas del detalle. Vania lo manda cuando se lo piden.
- La información se limita a esas columnas.
