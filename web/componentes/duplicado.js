// Aviso de posible duplicado cuando el servidor responde 409. UI-19.

import { ponerIcono } from "/componentes/icono.js";

export class ErrorDuplicado extends Error {
  constructor(cuerpo) {
    super(cuerpo.mensaje || "Ya existe un registro similar.");
    this.duplicado = cuerpo.posible_duplicado;
  }
}

// Las pantallas la llaman con la respuesta de guardar antes de revisar !ok.
export async function lanzarSiDuplicado(respuesta) {
  if (respuesta.status !== 409) return;
  const cuerpo = await respuesta.json().catch(() => ({}));
  if (cuerpo.posible_duplicado) throw new ErrorDuplicado(cuerpo);
}

export function abrirDuplicado({ error, alRevisar, alCancelar, alForzar }) {
  const { duplicado } = error;
  const fondo = document.createElement("div");
  fondo.className = "ventana-confirmacion c-overlay";
  fondo.dataset.ventanaDuplicado = "true";
  fondo.setAttribute("role", "dialog");
  fondo.setAttribute("aria-modal", "true");
  const contenido = document.createElement("div");
  contenido.className = "ventana-confirmacion__contenido c-modal";
  const encabezado = document.createElement("div");
  encabezado.className = "ventana-confirmacion__encabezado";
  const icono = document.createElement("span");
  icono.className = "ventana-confirmacion__icono ventana-confirmacion__icono--atencion";
  icono.dataset.iconoEstado = "circle-alert";
  void ponerIcono(icono, "circle-alert", { tamano: 28, grosor: 2.8 });
  const texto = document.createElement("p");
  texto.textContent = error.message;
  encabezado.append(icono, texto);
  const resumen = document.createElement("p");
  resumen.className = "ventana-duplicado__resumen";
  resumen.textContent = duplicado.resumen || "";
  const revisar = document.createElement("button");
  revisar.type = "button";
  revisar.className = "boton";
  revisar.dataset.duplicadoRevisar = "true";
  revisar.textContent = "Revisar";
  const cancelar = document.createElement("button");
  cancelar.type = "button";
  cancelar.className = "boton boton--secundario";
  cancelar.dataset.duplicadoCancelar = "true";
  cancelar.textContent = "Cancelar";
  const forzar = document.createElement("button");
  forzar.type = "button";
  forzar.className = "boton boton--secundario";
  forzar.dataset.duplicadoForzar = "true";
  forzar.textContent = "Reemplazar el existente";
  contenido.append(encabezado, resumen, revisar, cancelar, forzar);
  fondo.appendChild(contenido);
  document.body.appendChild(fondo);
  const cerrar = () => fondo.remove();
  revisar.addEventListener("click", () => {
    cerrar();
    const tipo = duplicado.area.replace(/s$/, "");
    window.location.hash = `#${tipo}-${duplicado.id}`;
    alRevisar?.(duplicado);
  });
  cancelar.addEventListener("click", () => { cerrar(); alCancelar?.(); });
  forzar.addEventListener("click", () => { cerrar(); alForzar?.(); });
  fondo.addEventListener("keydown", (evento) => { if (evento.key === "Escape") { cerrar(); alCancelar?.(); } });
  revisar.focus();
  return fondo;
}
