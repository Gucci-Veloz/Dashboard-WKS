// Indicadores textuales por área. UI-06.
// Frases cortas, todas con el mismo estilo y menor jerarquía que la
// conclusión del nivel 1. Ninguna se marca como principal.

export function renderIndicadores(contenedor, estado) {
  const anterior = contenedor.querySelector(".indicadores");
  if (anterior) anterior.remove();

  const lista = document.createElement("ul");
  lista.className = "indicadores";

  for (const indicador of estado.indicadores) {
    const item = document.createElement("li");
    item.className = "indicadores__item";
    item.dataset.area = indicador.area;
    item.textContent = indicador.frase_corta;
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
  return lista;
}
