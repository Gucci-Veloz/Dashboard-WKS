// Indicadores textuales por área. UI-06.
// Frases cortas, todas con el mismo estilo y menor jerarquía que la
// conclusión del nivel 1. Ninguna se marca como principal.

import { ponerIcono } from "/componentes/icono.js";

export function renderIndicadores(contenedor, estado) {
  const anterior = contenedor.querySelector(".indicadores");
  if (anterior) anterior.remove();

  const lista = document.createElement("ul");
  lista.className = "indicadores";

  for (const indicador of estado.indicadores) {
    const item = document.createElement("li");
    const estaBien = /sin novedad|al día/i.test(indicador.frase_corta);
    item.className = estaBien
      ? "indicadores__item c-indicador c-indicador--bien"
      : "indicadores__item c-indicador c-indicador--atencion";
    item.dataset.area = indicador.area;

    const icono = document.createElement("span");
    icono.dataset.iconoEstado = estaBien ? "bien" : "atencion";
    void ponerIcono(icono, estaBien ? "check" : "circle-alert", {
      tamano: 24,
      grosor: 2.8,
    });

    const texto = document.createElement("span");
    texto.textContent = indicador.frase_corta;
    item.append(icono, texto);
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
  return lista;
}
