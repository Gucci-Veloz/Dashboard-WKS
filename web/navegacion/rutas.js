// Navegación por hash. UI-08.
// Las pantallas de detalle se registran por convención en
// web/detalle/<area>.js (cada módulo exporta renderDetalle(contenedor, id));
// este archivo nunca se edita para agregar una nueva área.

const TIPO_A_AREA = {
  oficina: "oficinas",
  inquilino: "inquilinos",
  contrato: "contratos",
  pago: "pagos",
};

const AREAS = new Set(Object.values(TIPO_A_AREA));

export function analizarHash(hash) {
  const limpio = (hash || "").replace(/^#/, "");

  if (!limpio) {
    return { vista: "principal" };
  }

  if (limpio === "detalle") {
    return { vista: "detalle-general" };
  }

  if (limpio === "reporte") {
    return { vista: "reporte" };
  }

  if (AREAS.has(limpio)) {
    return { vista: "registro", area: limpio, id: undefined };
  }

  const separador = limpio.indexOf("-");
  if (separador === -1) {
    return { vista: "desconocida" };
  }

  const tipo = limpio.slice(0, separador);
  const id = limpio.slice(separador + 1);
  const area = TIPO_A_AREA[tipo];
  if (!area || !id) {
    return { vista: "desconocida" };
  }

  return { vista: "registro", area, tipo, id };
}

export async function cargarPantallaDetalle(area) {
  try {
    return await import(`/detalle/${area}.js`);
  } catch (error) {
    return null;
  }
}
