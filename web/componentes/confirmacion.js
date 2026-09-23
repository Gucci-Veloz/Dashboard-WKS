// Confirmación de guardado. UI-09.
// Muestra un aviso claro cuando un formulario guarda con éxito.

export function mostrarConfirmacion(contenedor, texto) {
  let elemento = contenedor.querySelector(".confirmacion");
  if (!elemento) {
    elemento = document.createElement("p");
    elemento.className = "confirmacion";
    elemento.dataset.confirmacion = "true";
    contenedor.appendChild(elemento);
  }
  elemento.textContent = texto;
  elemento.hidden = false;
  return elemento;
}
