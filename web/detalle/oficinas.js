// Detalle de oficinas. UI-10.
// Sin id: lista de oficinas, cada una enlaza a su ficha. Con id:
// ficha editable contra la API real (app/api/oficinas.py, DAT-09).

import { crearAccionEliminar, crearFormulario } from "/componentes/formulario.js";
import { mostrarPendientes } from "/componentes/confirmacion.js";

const CAMPOS = [
  { nombre: "tipo", etiqueta: "Tipo" },
  { nombre: "numero", etiqueta: "Número" },
  { nombre: "piso", etiqueta: "Piso" },
  { nombre: "m2", etiqueta: "Metros cuadrados" },
  { nombre: "estatus", etiqueta: "Estatus" },
];

async function renderLista(contenedor) {
  const respuesta = await fetch("/api/oficinas");
  const oficinas = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.textContent = "Oficinas";
  contenedor.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "detalle-lista";

  for (const oficina of oficinas) {
    const item = document.createElement("li");
    const enlace = document.createElement("a");
    enlace.href = `#oficina-${oficina.id}`;
    enlace.className = "enlace-discreto";
    enlace.dataset.oficinaId = String(oficina.id);
    enlace.textContent = `Oficina ${oficina.numero ?? oficina.id}`;
    item.appendChild(enlace);
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
}

function valorNumerico(texto) {
  return texto === "" || texto === undefined || texto === null ? null : Number(texto);
}

async function renderFicha(contenedor, id) {
  const respuesta = await fetch(`/api/oficinas/${id}`);
  if (!respuesta.ok) {
    const mensaje = document.createElement("p");
    mensaje.className = "navegacion__mensaje";
    mensaje.textContent = "No se pudo cargar esta oficina.";
    contenedor.appendChild(mensaje);
    return;
  }
  const oficina = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.dataset.tituloDetalle = "true";
  titulo.textContent = `Oficina ${oficina.numero ?? oficina.id}`;
  contenedor.appendChild(titulo);

  const zonaFormulario = document.createElement("div");
  contenedor.appendChild(zonaFormulario);
  const zonaPendientes = document.createElement("div");
  contenedor.appendChild(zonaPendientes);

  crearFormulario({
    contenedor: zonaFormulario,
    campos: CAMPOS.map((campo) => ({
      ...campo,
      valor: oficina[campo.nombre] ?? "",
    })),
    guardar: async (datos) => {
      const cuerpo = {
        tipo: datos.tipo,
        numero: datos.numero,
        piso: datos.piso,
        m2: valorNumerico(datos.m2),
        estatus: datos.estatus,
        extras: oficina.extras,
      };

      const respuestaGuardar = await fetch(`/api/oficinas/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cuerpo),
      });

      if (!respuestaGuardar.ok) {
        const error = await respuestaGuardar.json().catch(() => ({}));
        throw new Error(error.detail || "No se pudo guardar la oficina.");
      }

      return respuestaGuardar.json();
    },
    alConfirmar: () => window.location.reload(),
    alPendiente: () => window.location.reload(),
  });
  crearAccionEliminar({ contenedor: zonaFormulario, url: `/api/oficinas/${id}`, alConfirmar: () => window.location.hash = "#oficinas" });
  await mostrarPendientes({ contenedor: zonaPendientes, area: "oficinas", registroId: id, alConfirmar: () => window.location.reload() });
}

export async function renderDetalle(contenedor, id) {
  if (id) {
    await renderFicha(contenedor, id);
  } else {
    await renderLista(contenedor);
  }
}
