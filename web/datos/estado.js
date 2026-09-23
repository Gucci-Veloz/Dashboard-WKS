// Único punto de lectura del estado de atención para todo el
// Dashboard. Sin argumento, lee GET /api/estado (UI-07). Con un
// nombre de escenario ("tranquilo" o "con_atencion") devuelve el
// ejemplo correspondiente del contrato, copiado aquí porque
// contratos/ no se sirve por HTTP: lo usan las muestras y sus
// pruebas (UI-04, UI-05, UI-06), que no dependen del servicio.

const EJEMPLOS = {
  tranquilo: {
    conclusion: {
      tipo: "tranquilo",
      frase: "Todo está en orden en Works.",
      cantidad: 0,
    },
    asuntos: [],
    indicadores: [
      { area: "oficinas", frase_corta: "Oficinas · sin novedad" },
      { area: "inquilinos", frase_corta: "Inquilinos · sin novedad" },
      { area: "contratos", frase_corta: "Contratos · al día" },
      { area: "pagos", frase_corta: "Pagos · al día" },
    ],
    origen_datos: "sintetico",
    generado_en: "2026-09-23T09:00:00-06:00",
  },
  con_atencion: {
    conclusion: {
      tipo: "atencion",
      frase: "Hay tres cosas que requieren atención hoy.",
      cantidad: 3,
    },
    asuntos: [
      {
        id: "asunto-001",
        area: "contratos",
        frase: "La oficina 204 vence en 12 días.",
        por_que_importa:
          "El contrato de la oficina 204 entra en su ventana de renovación y todavía no hay respuesta del inquilino.",
        referencia: { tipo: "contrato", id: "contrato-sintetico-014" },
        orden: 0,
      },
      {
        id: "asunto-002",
        area: "pagos",
        frase: "El pago de septiembre de la oficina 108 sigue pendiente.",
        por_que_importa:
          "Ya pasó la fecha esperada de pago y no hay registro de que se haya cubierto.",
        referencia: { tipo: "pago", id: "pago-sintetico-037" },
        orden: 1,
      },
      {
        id: "asunto-003",
        area: "inquilinos",
        frase: "El contacto del Titular Sintético 09 quedó incompleto.",
        por_que_importa:
          "Falta un dato de contacto y eso impide avisarle si algo de su contrato cambia.",
        referencia: { tipo: "inquilino", id: "inquilino-sintetico-009" },
        orden: 2,
      },
    ],
    indicadores: [
      { area: "oficinas", frase_corta: "Oficinas · sin novedad" },
      { area: "inquilinos", frase_corta: "Inquilinos · un dato incompleto" },
      { area: "contratos", frase_corta: "Contratos · una renovación cerca" },
      { area: "pagos", frase_corta: "Pagos · un pendiente" },
    ],
    origen_datos: "sintetico",
    generado_en: "2026-09-23T09:00:00-06:00",
  },
};

export async function obtenerEstado(escenario) {
  if (escenario) {
    const estado = EJEMPLOS[escenario];
    if (!estado) {
      throw new Error(`escenario desconocido: ${escenario}`);
    }
    return estado;
  }

  const respuesta = await fetch("/api/estado");
  if (!respuesta.ok) {
    throw new Error("no se pudo obtener el estado de Works");
  }
  return await respuesta.json();
}
