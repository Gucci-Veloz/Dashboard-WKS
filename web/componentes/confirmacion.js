// Ventana y tarjetas para cambios pendientes. UI-18.

function nombreVisible(persona) {
  return persona ? `${persona[0].toUpperCase()}${persona.slice(1)}` : "¿Deseas";
}

async function respuestaJson(respuesta, mensaje) {
  if (!respuesta.ok) {
    const error = await respuesta.json().catch(() => ({}));
    throw new Error(error.detail || mensaje);
  }
  return respuesta.json();
}

export function abrirConfirmacion({ cambio, alConfirmar, alCerrar }) {
  const fondo = document.createElement("div");
  fondo.className = "ventana-confirmacion";
  fondo.dataset.ventanaConfirmacion = "true";
  fondo.setAttribute("role", "dialog");
  fondo.setAttribute("aria-modal", "true");
  const contenido = document.createElement("div");
  contenido.className = "ventana-confirmacion__contenido";
  const texto = document.createElement("p");
  texto.textContent = `${nombreVisible(cambio.solicitante)}, ¿deseas confirmar el cambio?`;
  const si = document.createElement("button");
  si.type = "button";
  si.className = "boton";
  si.dataset.confirmarCambio = String(cambio.id);
  si.textContent = "Sí";
  const no = document.createElement("button");
  no.type = "button";
  no.className = "boton boton--secundario";
  no.dataset.noConfirmarCambio = String(cambio.id);
  no.textContent = "No";
  const error = document.createElement("p");
  error.className = "formulario__mensaje-error";
  error.hidden = true;
  contenido.append(texto, si, no, error);
  fondo.appendChild(contenido);
  document.body.appendChild(fondo);
  const cerrar = () => { fondo.remove(); alCerrar?.(); };
  no.addEventListener("click", cerrar);
  fondo.addEventListener("keydown", (evento) => { if (evento.key === "Escape") cerrar(); });
  si.addEventListener("click", async () => {
    si.disabled = true;
    try {
      const confirmado = await respuestaJson(await fetch(`/api/cambios/${cambio.id}/confirmar`, { method: "POST" }), "No se pudo confirmar el cambio.");
      fondo.remove();
      await alConfirmar?.(confirmado);
    } catch (causa) {
      error.textContent = causa.message;
      error.hidden = false;
      si.disabled = false;
    }
  });
  si.focus();
  return fondo;
}

export async function buscarPendiente(id) {
  const cambios = await respuestaJson(await fetch("/api/cambios?estado=pendiente"), "No se pudieron consultar los cambios pendientes.");
  const cambio = cambios.find((candidato) => candidato.id === id);
  if (!cambio) throw new Error("No se encontró el cambio pendiente.");
  return cambio;
}

export async function mostrarPendientes({ contenedor, area, registroId, alConfirmar }) {
  const ruta = new URLSearchParams({ area, estado: "pendiente" });
  if (registroId != null) ruta.set("registro_id", String(registroId));
  const cambios = await respuestaJson(await fetch(`/api/cambios?${ruta}`), "No se pudieron consultar los cambios pendientes.");
  for (const cambio of cambios) {
    const tarjeta = document.createElement("section");
    tarjeta.className = "cambio-pendiente";
    tarjeta.dataset.cambioPendiente = String(cambio.id);
    const texto = document.createElement("p");
    texto.textContent = "Cambio pendiente de confirmar";
    const confirmar = document.createElement("button");
    confirmar.type = "button";
    confirmar.className = "boton";
    confirmar.textContent = "Confirmar";
    const descartar = document.createElement("button");
    descartar.type = "button";
    descartar.className = "boton boton--secundario";
    descartar.textContent = "Descartar";
    const error = document.createElement("p");
    error.className = "formulario__mensaje-error";
    error.hidden = true;
    confirmar.addEventListener("click", () => abrirConfirmacion({ cambio, alConfirmar: async (confirmado) => { tarjeta.remove(); await alConfirmar?.(confirmado); } }));
    descartar.addEventListener("click", async () => {
      descartar.disabled = true;
      try {
        await respuestaJson(await fetch(`/api/cambios/${cambio.id}/descartar`, { method: "POST" }), "No se pudo descartar el cambio.");
        tarjeta.remove();
      } catch (causa) {
        error.textContent = causa.message;
        error.hidden = false;
        descartar.disabled = false;
      }
    });
    tarjeta.append(texto, confirmar, descartar, error);
    contenedor.appendChild(tarjeta);
  }
}
