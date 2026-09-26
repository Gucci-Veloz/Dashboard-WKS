// Detalle de pagos y registrar pago. UI-13. Mismo patrón que UI-10
// a UI-12, contra app/api/pagos.py (DAT-12). Cuando el pago está
// pendiente, la ficha destaca la acción "Registrar pago" arriba del
// formulario general de edición: es a donde llega directo un asunto
// de pago pendiente del nivel 2.

import { crearAccionEliminar, crearFormulario } from "/componentes/formulario.js";
import { mostrarPendientes } from "/componentes/confirmacion.js";
import { lanzarSiDuplicado } from "/componentes/duplicado.js";

const CAMPOS_EDICION = [
  { nombre: "precio", etiqueta: "Precio" },
  { nombre: "deposito_garantia", etiqueta: "Depósito en garantía" },
  { nombre: "fecha_pago", etiqueta: "Fecha de pago (AAAA-MM-DD)" },
  { nombre: "forma_pago", etiqueta: "Forma de pago" },
  { nombre: "estatus_pago", etiqueta: "Estatus de pago" },
];

async function renderLista(contenedor) {
  const respuesta = await fetch("/api/pagos");
  const pagos = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.textContent = "Pagos";
  contenedor.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "detalle-lista";

  for (const pago of pagos) {
    const item = document.createElement("li");
    const enlace = document.createElement("a");
    enlace.href = `#pago-${pago.id}`;
    enlace.className = "enlace-discreto";
    enlace.dataset.pagoId = String(pago.id);
    enlace.textContent = `Pago ${pago.id} · ${pago.estatus_pago ?? "sin estatus"}`;
    item.appendChild(enlace);
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
}

function valorNumerico(texto) {
  return texto === "" || texto === undefined || texto === null ? null : Number(texto);
}

function renderAccionRegistrarPago(contenedor, pago, alRegistrar) {
  const zona = document.createElement("div");
  zona.dataset.accionRegistrarPago = "true";
  contenedor.appendChild(zona);

  // Nombre de campo distinto al del formulario de edición general
  // (que también tiene "forma_pago"): dos formularios en la misma
  // pantalla no pueden compartir el mismo id de campo.
  crearFormulario({
    contenedor: zona,
    campos: [{ nombre: "forma_pago_registro", etiqueta: "Forma de pago" }],
    guardar: async (datos) => {
      const respuesta = await fetch("/api/pagos/registrar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contrato_id: pago.contrato_id,
          forma_pago: datos.forma_pago_registro,
        }),
      });

      if (!respuesta.ok) {
        const error = await respuesta.json().catch(() => ({}));
        throw new Error(error.detail || "No se pudo registrar el pago.");
      }

      return respuesta.json();
    },
    alConfirmar: () => window.location.reload(),
    alPendiente: () => window.location.reload(),
  });
}

async function renderFicha(contenedor, id) {
  const respuesta = await fetch(`/api/pagos/${id}`);
  if (!respuesta.ok) {
    const mensaje = document.createElement("p");
    mensaje.className = "navegacion__mensaje";
    mensaje.textContent = "No se pudo cargar este pago.";
    contenedor.appendChild(mensaje);
    return;
  }
  const pago = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.dataset.tituloDetalle = "true";
  titulo.textContent = `Pago ${pago.id}`;
  contenedor.appendChild(titulo);

  const zonaAccion = document.createElement("div");
  contenedor.appendChild(zonaAccion);

  const zonaEdicion = document.createElement("div");
  contenedor.appendChild(zonaEdicion);
  const zonaPendientes = document.createElement("div");
  contenedor.appendChild(zonaPendientes);

  function renderEdicion(pagoActual) {
    crearFormulario({
      contenedor: zonaEdicion,
      campos: CAMPOS_EDICION.map((campo) => ({
        ...campo,
        valor: pagoActual[campo.nombre] ?? "",
      })),
      guardar: async (datos, { forzar, duplicado: dup } = {}) => {
        const cuerpo = {
          contrato_id: pagoActual.contrato_id,
          precio: valorNumerico(datos.precio),
          deposito_garantia: valorNumerico(datos.deposito_garantia),
          fecha_pago: datos.fecha_pago,
          forma_pago: datos.forma_pago,
          estatus_pago: datos.estatus_pago,
          extras: pagoActual.extras,
        };

        const urlGuardar = forzar && dup ? `/api/pagos/${dup.id}` : `/api/pagos/${id}`;
        const respuestaGuardar = await fetch(urlGuardar, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(cuerpo),
        });

        await lanzarSiDuplicado(respuestaGuardar);
        if (!respuestaGuardar.ok) {
          const error = await respuestaGuardar.json().catch(() => ({}));
          throw new Error(error.detail || "No se pudo guardar el pago.");
        }

        return respuestaGuardar.json();
      },
      alConfirmar: () => window.location.reload(),
      alPendiente: () => window.location.reload(),
    });
  }

  renderEdicion(pago);
  crearAccionEliminar({ contenedor: zonaEdicion, url: `/api/pagos/${id}`, alConfirmar: () => window.location.hash = "#pagos" });

  if (pago.estatus_pago === "pendiente") {
    renderAccionRegistrarPago(zonaAccion, pago);
  }
  await mostrarPendientes({ contenedor: zonaPendientes, area: "pagos", registroId: id, alConfirmar: () => window.location.reload() });
}

export async function renderDetalle(contenedor, id) {
  if (id) {
    await renderFicha(contenedor, id);
  } else {
    await renderLista(contenedor);
  }
}
