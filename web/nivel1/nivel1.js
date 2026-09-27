// Nivel 1: estado general. UI-04.
// En estado tranquilo transmite calma y no rellena la pantalla. En
// estado de atención, la frase de la conclusión ya dice cuántas
// cosas hay (la redacta app/estado en el servicio). Este módulo no
// agrega listas: eso es trabajo de nivel 2 (UI-05).

import { ponerIcono } from "/componentes/icono.js";

export function renderNivel1(contenedor, estado) {
  contenedor.innerHTML = "";

  const seccion = document.createElement("section");
  const requiereAtencion = estado.conclusion.tipo === "atencion";
  seccion.className = requiereAtencion
    ? "nivel1 nivel1--atencion"
    : "nivel1 nivel1--tranquilo";

  if (estado.origen_datos === "sintetico") {
    const aviso = document.createElement("p");
    aviso.className = "nivel1__aviso";
    aviso.dataset.avisoDatosSinteticos = "true";
    aviso.textContent = "Datos sintéticos";
    seccion.appendChild(aviso);
  }

  const bloqueEstado = document.createElement("div");
  bloqueEstado.className = "nivel1__estado";
  bloqueEstado.dataset.bloqueInformativo = "true";

  const icono = document.createElement("span");
  icono.className = requiereAtencion
    ? "nivel1__icono nivel1__icono--atencion"
    : "nivel1__icono nivel1__icono--bien";
  icono.dataset.iconoEstado = requiereAtencion ? "atencion" : "tranquilo";
  void ponerIcono(icono, requiereAtencion ? "circle-alert" : "check", {
    tamano: 30,
    grosor: 2.8,
  });
  bloqueEstado.appendChild(icono);

  const conclusion = document.createElement("p");
  conclusion.className = "nivel1__conclusion";
  conclusion.dataset.conclusion = "true";
  conclusion.textContent = estado.conclusion.frase;
  bloqueEstado.appendChild(conclusion);
  seccion.appendChild(bloqueEstado);

  contenedor.appendChild(seccion);
  return seccion;
}
