// Punto de entrada del Dashboard.
import { obtenerEstado } from "/datos/estado.js";
import { renderNivel1 } from "/nivel1/nivel1.js";
import { renderNivel2 } from "/nivel2/nivel2.js";
import { renderIndicadores } from "/indicadores/indicadores.js";
import { analizarHash, cargarPantallaDetalle } from "/navegacion/rutas.js";
import { renderReporte } from "/reporte/reporte.js";

const contenedor = document.getElementById("app");

function renderVolver() {
  const volver = document.createElement("a");
  volver.href = "#";
  volver.className = "navegacion__volver";
  volver.textContent = "Volver";
  contenedor.appendChild(volver);
}

function renderMensajeDeError() {
  const mensaje = document.createElement("p");
  mensaje.className = "navegacion__mensaje";
  mensaje.dataset.errorEstado = "true";
  mensaje.textContent =
    "No se pudo cargar la información de Works en este momento. Intenta de nuevo en unos minutos.";
  contenedor.appendChild(mensaje);
}

async function renderPrincipal() {
  let estado;
  try {
    estado = await obtenerEstado();
  } catch (error) {
    renderMensajeDeError();
    return;
  }

  renderNivel1(contenedor, estado);
  renderNivel2(contenedor, estado);
  renderIndicadores(contenedor, estado);

  const verTodo = document.createElement("a");
  verTodo.href = "#detalle";
  verTodo.className = "enlace-discreto navegacion__ver-todo";
  verTodo.dataset.verTodo = "true";
  verTodo.textContent = "ver todo";
  contenedor.appendChild(verTodo);
}

function renderDetalleGeneral() {
  const titulo = document.createElement("h2");
  titulo.textContent = "Detalle";
  contenedor.appendChild(titulo);

  const areas = document.createElement("nav");
  areas.className = "detalle-general__areas";
  areas.setAttribute("aria-label", "Áreas del detalle");
  for (const [ruta, etiqueta] of Object.entries({
    oficinas: "Oficinas",
    inquilinos: "Inquilinos",
    contratos: "Contratos",
    pagos: "Pagos",
  })) {
    const enlace = document.createElement("a");
    enlace.href = `#${ruta}`;
    enlace.className = "enlace-discreto";
    enlace.textContent = etiqueta;
    areas.appendChild(enlace);
  }
  const reporte = document.createElement("a");
  reporte.href = "#reporte";
  reporte.className = "enlace-discreto detalle-general__reporte";
  reporte.dataset.abrirReporte = "true";
  reporte.textContent = "Reporte del día";
  areas.appendChild(reporte);
  contenedor.appendChild(areas);
  renderVolver();
}

async function renderRegistro(area, id) {
  const modulo = await cargarPantallaDetalle(area);

  if (modulo && typeof modulo.renderDetalle === "function") {
    await modulo.renderDetalle(contenedor, id);
  } else {
    const mensaje = document.createElement("p");
    mensaje.className = "navegacion__mensaje";
    mensaje.textContent = "Este detalle todavía no está disponible.";
    contenedor.appendChild(mensaje);
  }

  renderVolver();
}

async function renderRuta() {
  contenedor.innerHTML = "";
  const ruta = analizarHash(window.location.hash);

  if (ruta.vista === "detalle-general") {
    renderDetalleGeneral();
    return;
  }

  if (ruta.vista === "registro") {
    await renderRegistro(ruta.area, ruta.id);
    return;
  }

  if (ruta.vista === "reporte") {
    await renderReporte(contenedor);
    renderVolver();
    return;
  }

  await renderPrincipal();
}

window.addEventListener("hashchange", renderRuta);
renderRuta();
