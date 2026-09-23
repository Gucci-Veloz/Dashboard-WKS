// Nivel 1: estado general. UI-04.
// En estado tranquilo transmite calma y no rellena la pantalla. En
// estado de atención, la frase de la conclusión ya dice cuántas
// cosas hay (la redacta app/estado en el servicio). Este módulo no
// agrega listas: eso es trabajo de nivel 2 (UI-05).

export function renderNivel1(contenedor, estado) {
  contenedor.innerHTML = "";

  const seccion = document.createElement("section");
  seccion.className = "nivel1";

  if (estado.origen_datos === "sintetico") {
    const aviso = document.createElement("p");
    aviso.className = "nivel1__aviso";
    aviso.dataset.avisoDatosSinteticos = "true";
    aviso.textContent = "Datos sintéticos";
    seccion.appendChild(aviso);
  }

  const conclusion = document.createElement("p");
  conclusion.className = "nivel1__conclusion";
  conclusion.dataset.conclusion = "true";
  conclusion.textContent = estado.conclusion.frase;
  seccion.appendChild(conclusion);

  contenedor.appendChild(seccion);
  return seccion;
}
