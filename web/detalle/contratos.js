// Detalle de contratos. UI-12. Mismo patrón que UI-10 (oficinas),
// contra app/api/contratos.py (DAT-11). Las fechas también se
// muestran en forma humana ("vence en 12 días").

import { crearAccionEliminar, crearFormulario } from "/componentes/formulario.js";
import { mostrarPendientes } from "/componentes/confirmacion.js";

const CAMPOS = [
  { nombre: "oficina_id", etiqueta: "Oficina (id)" },
  { nombre: "inquilino_id", etiqueta: "Inquilino (id)" },
  { nombre: "inicio", etiqueta: "Inicio (AAAA-MM-DD)" },
  { nombre: "fin", etiqueta: "Fin (AAAA-MM-DD)" },
  { nombre: "alerta_renovacion", etiqueta: "Alerta de renovación" },
];

export function fraseVencimiento(fechaFin, hoy = new Date()) {
  if (!fechaFin) return "Sin fecha de fin registrada.";

  const fin = new Date(`${fechaFin}T00:00:00`);
  if (Number.isNaN(fin.getTime())) return "Sin fecha de fin registrada.";

  const inicioHoy = new Date(hoy.getFullYear(), hoy.getMonth(), hoy.getDate());
  const dias = Math.round((fin - inicioHoy) / 86400000);

  if (dias > 0) return `Vence en ${dias} días.`;
  if (dias === 0) return "Vence hoy.";
  return `Venció hace ${Math.abs(dias)} días.`;
}

async function renderLista(contenedor) {
  const respuesta = await fetch("/api/contratos");
  const contratos = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.textContent = "Contratos";
  contenedor.appendChild(titulo);

  const lista = document.createElement("ul");
  lista.className = "detalle-lista";

  for (const contrato of contratos) {
    const item = document.createElement("li");
    const enlace = document.createElement("a");
    enlace.href = `#contrato-${contrato.id}`;
    enlace.className = "enlace-discreto";
    enlace.dataset.contratoId = String(contrato.id);
    enlace.textContent = `Contrato ${contrato.id} · ${fraseVencimiento(contrato.fin)}`;
    item.appendChild(enlace);
    lista.appendChild(item);
  }

  contenedor.appendChild(lista);
}

function valorEntero(texto) {
  return texto === "" || texto === undefined || texto === null
    ? null
    : parseInt(texto, 10);
}

async function renderFicha(contenedor, id) {
  const respuesta = await fetch(`/api/contratos/${id}`);
  if (!respuesta.ok) {
    const mensaje = document.createElement("p");
    mensaje.className = "navegacion__mensaje";
    mensaje.textContent = "No se pudo cargar este contrato.";
    contenedor.appendChild(mensaje);
    return;
  }
  const contrato = await respuesta.json();

  const titulo = document.createElement("h2");
  titulo.dataset.tituloDetalle = "true";
  titulo.textContent = `Contrato ${contrato.id}`;
  contenedor.appendChild(titulo);

  const vencimiento = document.createElement("p");
  vencimiento.className = "tarjeta__texto-secundario";
  vencimiento.dataset.vencimiento = "true";
  vencimiento.textContent = fraseVencimiento(contrato.fin);
  contenedor.appendChild(vencimiento);

  const zonaFormulario = document.createElement("div");
  contenedor.appendChild(zonaFormulario);
  const zonaPendientes = document.createElement("div");
  contenedor.appendChild(zonaPendientes);

  crearFormulario({
    contenedor: zonaFormulario,
    campos: CAMPOS.map((campo) => ({
      ...campo,
      valor: contrato[campo.nombre] ?? "",
    })),
    guardar: async (datos) => {
      const cuerpo = {
        oficina_id: valorEntero(datos.oficina_id),
        inquilino_id: valorEntero(datos.inquilino_id),
        inicio: datos.inicio,
        fin: datos.fin,
        alerta_renovacion: datos.alerta_renovacion,
        extras: contrato.extras,
      };

      const respuestaGuardar = await fetch(`/api/contratos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cuerpo),
      });

      if (!respuestaGuardar.ok) {
        const error = await respuestaGuardar.json().catch(() => ({}));
        throw new Error(error.detail || "No se pudo guardar el contrato.");
      }

      return respuestaGuardar.json();
    },
    alConfirmar: () => window.location.reload(),
    alPendiente: () => window.location.reload(),
  });
  crearAccionEliminar({ contenedor: zonaFormulario, url: `/api/contratos/${id}`, alConfirmar: () => window.location.hash = "#contratos" });
  await mostrarPendientes({ contenedor: zonaPendientes, area: "contratos", registroId: id, alConfirmar: () => window.location.reload() });
}

export async function renderDetalle(contenedor, id) {
  if (id) {
    await renderFicha(contenedor, id);
  } else {
    await renderLista(contenedor);
  }
}
