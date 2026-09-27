// Detalle de inquilinos. UI-11. Igual patrón que UI-10 (oficinas),
// contra app/api/inquilinos.py (DAT-10).

import { crearAccionEliminar, crearFormulario } from "/componentes/formulario.js";
import { mostrarPendientes } from "/componentes/confirmacion.js";
import { lanzarSiDuplicado } from "/componentes/duplicado.js";
import { ponerIcono } from "/componentes/icono.js";

const CAMPOS = [
  { nombre: "titular", etiqueta: "Titular" },
  { nombre: "contacto", etiqueta: "Contacto" },
];

async function renderLista(contenedor) {
  const respuesta = await fetch("/api/inquilinos");
  const inquilinos = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.textContent = "Inquilinos";
  contenedor.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "detalle-lista";

  for (const inquilino of inquilinos) {
    const item = document.createElement("li");
    const enlace = document.createElement("a");
    enlace.href = `#inquilino-${inquilino.id}`;
    enlace.className = "enlace-discreto detalle-lista__enlace c-tarjeta-tocable";
    enlace.dataset.inquilinoId = String(inquilino.id);
    const icono = document.createElement("span");
    icono.dataset.icono = "arrow-right";
    void ponerIcono(icono, "arrow-right", { tamano: 26, grosor: 2.8 });
    const texto = document.createElement("span");
    texto.className = "detalle-lista__texto";
    texto.textContent = inquilino.titular ?? `Inquilino ${inquilino.id}`;
    enlace.append(icono, texto);
    item.appendChild(enlace);
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
}

async function renderFicha(contenedor, id) {
  const respuesta = await fetch(`/api/inquilinos/${id}`);
  if (!respuesta.ok) {
    const mensaje = document.createElement("p");
    mensaje.className = "navegacion__mensaje";
    mensaje.textContent = "No se pudo cargar este inquilino.";
    contenedor.appendChild(mensaje);
    return;
  }
  const inquilino = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.dataset.tituloDetalle = "true";
  titulo.textContent = inquilino.titular ?? `Inquilino ${inquilino.id}`;
  contenedor.appendChild(titulo);

  const zonaFormulario = document.createElement("div");
  contenedor.appendChild(zonaFormulario);
  const zonaPendientes = document.createElement("div");
  contenedor.appendChild(zonaPendientes);

  crearFormulario({
    contenedor: zonaFormulario,
    campos: CAMPOS.map((campo) => ({
      ...campo,
      valor: inquilino[campo.nombre] ?? "",
    })),
    guardar: async (datos, { forzar, duplicado: dup } = {}) => {
      const cuerpo = {
        titular: datos.titular,
        contacto: datos.contacto,
        extras: inquilino.extras,
      };

      const urlGuardar = forzar && dup ? `/api/inquilinos/${dup.id}` : `/api/inquilinos/${id}`;
      const respuestaGuardar = await fetch(urlGuardar, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cuerpo),
      });

      await lanzarSiDuplicado(respuestaGuardar);
      if (!respuestaGuardar.ok) {
        const error = await respuestaGuardar.json().catch(() => ({}));
        throw new Error(error.detail || "No se pudo guardar el inquilino.");
      }

      return respuestaGuardar.json();
    },
    alConfirmar: () => window.location.reload(),
    alPendiente: () => window.location.reload(),
  });
  crearAccionEliminar({ contenedor: zonaFormulario, url: `/api/inquilinos/${id}`, alConfirmar: () => window.location.hash = "#inquilinos" });
  await mostrarPendientes({ contenedor: zonaPendientes, area: "inquilinos", registroId: id, alConfirmar: () => window.location.reload() });
}

export async function renderDetalle(contenedor, id) {
  if (id) {
    await renderFicha(contenedor, id);
  } else {
    await renderLista(contenedor);
  }
}
