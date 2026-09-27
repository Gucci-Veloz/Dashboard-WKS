// Nivel 2: lo que merece atención. UI-05.
// Los asuntos en frases humanas, cada uno con su "por qué importa",
// en el orden que trae el contrato. Cada elemento se puede tocar; su
// destino real (el registro exacto) lo define UI-08. En estado
// tranquilo no se renderiza nada.

import { ponerIcono } from "/componentes/icono.js";

export function renderNivel2(contenedor, estado) {
  const anterior = contenedor.querySelector(".nivel2");
  if (anterior) anterior.remove();

  const asuntos = [...estado.asuntos].sort((a, b) => a.orden - b.orden);
  if (asuntos.length === 0) {
    return null;
  }

  const lista = document.createElement("ul");
  lista.className = "nivel2";

  for (const asunto of asuntos) {
    const item = document.createElement("li");

    const enlace = document.createElement("a");
    enlace.className = "nivel2__asunto c-tarjeta-tocable";
    enlace.dataset.asuntoId = asunto.id;
    enlace.dataset.orden = String(asunto.orden);
    // Destino provisional: UI-08 define la navegación real al registro.
    enlace.href = `#${asunto.referencia.tipo}-${asunto.referencia.id}`;

    const icono = document.createElement("span");
    icono.className = "nivel2__icono";
    icono.dataset.iconoEstado = "atencion";
    void ponerIcono(icono, "circle-alert", { tamano: 28, grosor: 2.8 });
    enlace.appendChild(icono);

    const contenido = document.createElement("span");
    contenido.className = "nivel2__contenido";

    const frase = document.createElement("span");
    frase.className = "nivel2__frase";
    frase.textContent = asunto.frase;
    contenido.appendChild(frase);

    const porQueImporta = document.createElement("span");
    porQueImporta.className = "nivel2__por-que-importa";
    porQueImporta.textContent = asunto.por_que_importa;
    contenido.appendChild(porQueImporta);
    enlace.appendChild(contenido);

    item.appendChild(enlace);
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
  return lista;
}
