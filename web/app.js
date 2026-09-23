// Punto de entrada del Dashboard.
import { obtenerEstado } from "/datos/estado.js";
import { renderNivel1 } from "/nivel1/nivel1.js";
import { renderNivel2 } from "/nivel2/nivel2.js";
import { renderIndicadores } from "/indicadores/indicadores.js";
import { analizarHash, cargarPantallaDetalle } from "/navegacion/rutas.js";

const contenedor = document.getElementById("app");

// Provisional: hasta UI-07, obtenerEstado() solo conoce estos
// ejemplos del contrato. Se usa "con_atencion" por defecto para que
// nivel 2 y la navegación a un registro tengan algo que mostrar.
const ESCENARIO_PROVISIONAL = "con_atencion";

function renderVolver() {
  const volver = document.createElement("a");
  volver.href = "#";
  volver.className = "navegacion__volver";
  volver.textContent = "Volver";
  contenedor.appendChild(volver);
}

async function renderPrincipal() {
  const estado = await obtenerEstado(ESCENARIO_PROVISIONAL);
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
  renderVolver();
}

async function renderRegistro(area, id) {
  const modulo = await cargarPantallaDetalle(area);

  if (modulo && typeof modulo.renderDetalle === "function") {
    modulo.renderDetalle(contenedor, id);
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

  await renderPrincipal();
}

window.addEventListener("hashchange", renderRuta);
renderRuta();
