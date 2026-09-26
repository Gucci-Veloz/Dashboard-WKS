# Contrato de uso de la API para Vania

Este documento es para quien conecta el perfil `vania` de Hermes al servicio
de Works (MAN-01). Cubre qué endpoint usar según la intención, cómo
autenticarse, las reglas que Vania debe respetar y qué hacer con un error.
No reabre el handshake: solo describe lo que ya existe.

## Cómo se autentica

Toda petición de Vania lleva el encabezado:

```
Authorization: Bearer <WORKS_TOKEN_VANIA>
```

`WORKS_TOKEN_VANIA` es una variable de entorno del servicio (la define
MAN-06 en el VPS). Sin ese encabezado, o con un valor que no coincide, el
servicio identifica a quien llama como `dashboard`, nunca como `vania` — y
los endpoints que exigen credencial de servicio responden `401`.

Para **crear, modificar, borrar o confirmar** un cambio, Vania también
manda `X-Works-Solicitante: <número de WhatsApp>`. El servicio resuelve ese
número en la configuración local del servidor; los números no se escriben
en este repositorio. La persona de ese encabezado debe tener su propia
sesión vigente: una sesión de David no autoriza una instrucción de Grecia,
ni al revés. Un número desconocido o el del desarrollador responde `403`.
Si falta la sesión correcta, responde `401` con `codigo: "sin_sesion"`.

## Endpoints por intención

| Intención de la persona | Ejemplo | Endpoint |
|---|---|---|
| Saber cómo está Works en general | "¿cómo está Works?" | `GET /api/estado` |
| Obtener el resumen de avisos ya agrupado, para redactar el mensaje de WhatsApp | (lo arma Hermes antes de escribirle a alguien) | `GET /api/vania/avisos` |
| Confirmar que un contrato pagó | "Registra que la 204 pagó septiembre por transferencia" | `POST /api/pagos/registrar` |
| Consultar un pago puntual | "¿cuánto debe la 204?" | `GET /api/pagos/{pago_id}` |
| Consultar oficinas | "¿qué oficinas están libres?" | `GET /api/oficinas` |
| Consultar inquilinos | "¿quién ocupa la 204?" | `GET /api/inquilinos` |
| Consultar contratos | "¿cuándo vence el contrato de la 204?" | `GET /api/contratos` |
| Consultar el rastro de lo que ya se hizo | "¿qué registraste hoy?" | `GET /api/actividad` |

## Reglas del handshake que Vania debe respetar

- **No inventa datos.** Si no hay una fila que sostenga la respuesta, dice
  que no sabe; no completa huecos con una suposición.
- **Confirma lo que se le pidió**, no actúa por iniciativa propia. La única
  excepción es `GET /api/vania/avisos`, que le entrega ya calculado lo que
  Vania debe avisar por su cuenta (los asuntos que el motor de estado
  detectó, ver DAT-07).
- **No contacta inquilinos.** Ningún endpoint de este contrato envía nada a
  un tercero; eso lo hace Vania desde Hermes, fuera de esta API.
- **Primero revisa la sesión de quien lo pidió.** Cuando alguien le pide un
  cambio, Vania manda su número en `X-Works-Solicitante`. Si recibe
  `401 sin_sesion`, pide un link; le explica que vence en 10 minutos y espera
  a que la persona entre. No ejecuta el cambio hasta que la sesión correcta
  esté vigente.
- **Crea un pendiente, no el cambio oficial.** Cuando ya existe la sesión,
  Vania crea el pre-registro y pregunta por WhatsApp: "¿Sí o No?". Con un
  "Sí" confirma el pendiente; con "No" lo deja pendiente para que pueda
  confirmarse durante las siguientes 24 horas. Pregunta si hay observaciones
  y las incluye si la persona se las da.
- **Registra solicitante y ejecutor.** Una escritura de Vania conserva a
  David o Grecia como solicitante y guarda `vania` como ejecutor. El reporte
  del día incluye ambos campos y las observaciones; Vania lo consulta y lo
  manda solo cuando se lo piden.

## `origen_dato`: no significa lo mismo en todas las tablas

- En `actividad` (INT-01), `origen_dato` distingue **de dónde salió el
  movimiento registrado**: `sintetico` para los movimientos de demostración
  (`app/fuentes/actividad_sintetica.py`) y `real` para los que dejan las
  APIs de las cuatro áreas al escribir sobre datos reales.
- En `oficinas`, `inquilinos`, `contratos` y `pagos` (001_areas.sql),
  `origen_dato` distingue **de dónde salió el registro de esa área**:
  `sintetico` (generado), `excel` (cargado del Excel de Works, fase 9) o
  `manual` (creado o editado a través de una API, sin importar si quien
  llamó fue el Dashboard o Vania).

## El caso de error

Un endpoint que falla responde con el código HTTP que corresponde
(`401` sin credencial válida, `404` si lo referido no existe, `400` si el
dato de entrada no tiene sentido, por ejemplo un `contrato_id` inexistente)
y un cuerpo `{"detail": "<mensaje>"}` en español. Vania debe decir, con sus
palabras, que no pudo hacerlo y por qué — nunca inventar que sí funcionó.
