const NOMBRES_PERMITIDOS = new Set([
  "arrow-right",
  "check",
  "circle-alert",
  "circle-x",
  "info",
  "lock-keyhole",
  "loader-circle",
  "wallet",
  "x",
]);

/** Inserta un SVG Lucide local, con el tamaño y grosor del sistema visual. */
export async function ponerIcono(elemento, nombre, opciones = {}) {
  if (!NOMBRES_PERMITIDOS.has(nombre))
    throw new Error(`Ícono no permitido: ${nombre}`);
  const { tamano = 24, grosor = 2.5, etiqueta = "" } = opciones;
  const respuesta = await fetch(`/iconos/${nombre}.svg`);
  if (!respuesta.ok) throw new Error(`No se pudo cargar el ícono: ${nombre}`);
  const documento = new DOMParser().parseFromString(
    await respuesta.text(),
    "image/svg+xml",
  );
  const svg = documento.documentElement;
  svg.setAttribute("width", String(tamano));
  svg.setAttribute("height", String(tamano));
  svg.setAttribute("stroke-width", String(grosor));
  svg.setAttribute("aria-hidden", etiqueta ? "false" : "true");
  svg.setAttribute("focusable", "false");
  if (etiqueta) svg.setAttribute("aria-label", etiqueta);
  elemento.replaceChildren(document.importNode(svg, true));
  elemento.classList.add("icono");
  return elemento;
}
