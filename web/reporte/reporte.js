// Reporte del día. UI-20.

function fechaDeQueretaro() {
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "America/Mexico_City",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());
}

function textoPersona(valor) {
  return valor === "vania" ? "Vania" : valor || "—";
}

function crearFila(fila) {
  const tr = document.createElement("tr");
  const columnas = [
    ["id", fila.id], ["fecha", fila.fecha], ["inquilino", fila.inquilino],
    ["concepto", fila.concepto], ["observaciones", fila.observaciones || "—"],
    ["solicitante", textoPersona(fila.solicitante)], ["ejecutor", textoPersona(fila.ejecutor)],
  ];
  for (const [nombre, valor] of columnas) {
    const td = document.createElement("td");
    td.dataset.columnaReporte = nombre;
    td.textContent = String(valor ?? "—");
    if (nombre === "ejecutor") {
      td.dataset.ejecutor = fila.ejecutor || "";
      td.className = fila.ejecutor === "vania" ? "reporte__ejecutor reporte__ejecutor--vania" : "reporte__ejecutor";
    }
    tr.appendChild(td);
  }
  return tr;
}

async function cargarReporte(cuerpo, fecha) {
  cuerpo.innerHTML = "";
  const respuesta = await fetch(`/api/reporte?fecha=${encodeURIComponent(fecha)}`);
  if (!respuesta.ok) {
    const error = document.createElement("p");
    error.className = "navegacion__mensaje";
    error.textContent = "No se pudo cargar el reporte del día.";
    cuerpo.appendChild(error);
    return;
  }
  const filas = await respuesta.json();
  if (filas.length === 0) {
    const vacio = document.createElement("p");
    vacio.dataset.reporteVacio = "true";
    vacio.textContent = "No hubo cambios confirmados este día.";
    cuerpo.appendChild(vacio);
    return;
  }
  const tabla = document.createElement("table");
  tabla.className = "c-tabla";
  tabla.dataset.tablaReporte = "true";
  tabla.innerHTML = "<thead><tr><th>ID</th><th>Fecha</th><th>Inquilino</th><th>Concepto</th><th>Observaciones</th><th>Solicitante</th><th>Ejecutor</th></tr></thead>";
  const tbody = document.createElement("tbody");
  for (const fila of filas) tbody.appendChild(crearFila(fila));
  tabla.appendChild(tbody);
  cuerpo.appendChild(tabla);
}

export async function renderReporte(contenedor) {
  if (!document.querySelector('link[href="/reporte/reporte.css"]')) {
    const estilos = document.createElement("link");
    estilos.rel = "stylesheet";
    estilos.href = "/reporte/reporte.css";
    document.head.appendChild(estilos);
  }
  contenedor.classList.add("reporte");
  const titulo = document.createElement("h2");
  titulo.textContent = "Reporte del día";
  contenedor.appendChild(titulo);
  const etiqueta = document.createElement("label");
  etiqueta.className = "reporte__fecha campo-texto";
  etiqueta.htmlFor = "reporte-fecha";
  etiqueta.textContent = "Fecha";
  const fecha = document.createElement("input");
  fecha.className = "campo-texto__control c-campo";
  fecha.id = "reporte-fecha";
  fecha.type = "date";
  fecha.value = fechaDeQueretaro();
  fecha.dataset.fechaReporte = "true";
  etiqueta.appendChild(fecha);
  contenedor.appendChild(etiqueta);
  const envoltura = document.createElement("div");
  envoltura.className = "reporte__tabla c-tabla-contenedor";
  contenedor.appendChild(envoltura);
  const desliza = document.createElement("span");
  desliza.className = "reporte__desliza";
  desliza.setAttribute("aria-hidden", "true");
  desliza.textContent = "Desliza →";
  contenedor.appendChild(desliza);
  await cargarReporte(envoltura, fecha.value);
  fecha.addEventListener("change", () => cargarReporte(envoltura, fecha.value));
}
