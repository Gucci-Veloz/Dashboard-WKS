// Formulario que convierte la entrada en un pre-registro. UI-18.

import { abrirConfirmacion, buscarPendiente } from "/componentes/confirmacion.js";
import { abrirDuplicado } from "/componentes/duplicado.js";

export function crearFormulario({ contenedor, campos, guardar, alConfirmar, alPendiente }) {
  contenedor.innerHTML = "";
  const form = document.createElement("form");
  form.className = "formulario";
  form.noValidate = true;
  const inputs = {};
  for (const campo of campos) {
    const grupo = document.createElement("div");
    grupo.className = "campo-texto";
    const etiqueta = document.createElement("label");
    etiqueta.className = "campo-texto__etiqueta";
    etiqueta.htmlFor = `campo-${campo.nombre}`;
    etiqueta.textContent = campo.etiqueta;
    const input = document.createElement("input");
    input.className = "campo-texto__control";
    input.id = `campo-${campo.nombre}`;
    input.name = campo.nombre;
    input.type = "text";
    input.value = campo.valor ?? "";
    input.dataset.campo = campo.nombre;
    grupo.append(etiqueta, input);
    form.appendChild(grupo);
    inputs[campo.nombre] = input;
  }
  const grupoObservaciones = document.createElement("div");
  grupoObservaciones.className = "campo-texto";
  const etiquetaObservaciones = document.createElement("label");
  etiquetaObservaciones.className = "campo-texto__etiqueta";
  etiquetaObservaciones.htmlFor = "campo-observaciones";
  etiquetaObservaciones.textContent = "Observaciones (opcional)";
  const observaciones = document.createElement("textarea");
  observaciones.className = "campo-texto__control";
  observaciones.id = "campo-observaciones";
  observaciones.name = "observaciones";
  grupoObservaciones.append(etiquetaObservaciones, observaciones);
  const mensajeError = document.createElement("p");
  mensajeError.className = "formulario__mensaje-error";
  mensajeError.dataset.errorGuardar = "true";
  mensajeError.hidden = true;
  const boton = document.createElement("button");
  boton.type = "submit";
  boton.className = "boton";
  boton.textContent = "Guardar";
  form.append(grupoObservaciones, mensajeError, boton);
  const enviar = async (forzar) => {
    mensajeError.hidden = true;
    boton.disabled = true;
    const datos = Object.fromEntries(Object.entries(inputs).map(([nombre, input]) => [nombre, input.value]));
    datos.observaciones = observaciones.value || null;
    try {
      const creado = await guardar(datos, { forzar });
      // La muestra aislada de UI-09 no usa la API de cambios; se conserva
      // como verificación del componente sin servicio.
      if (!creado || !creado.id) {
        for (const [nombre, input] of Object.entries(inputs)) {
          if (nombre in (creado || {})) input.value = creado[nombre];
        }
        const aviso = document.createElement("p");
        aviso.className = "confirmacion";
        aviso.dataset.confirmacion = "true";
        aviso.textContent = "Guardado. Los datos ya están actualizados.";
        form.appendChild(aviso);
        return;
      }
      const cambio = await buscarPendiente(creado.id);
      abrirConfirmacion({
        cambio,
        alConfirmar: async (confirmado) => alConfirmar?.(confirmado),
        alCerrar: () => alPendiente?.(cambio),
      });
    } catch (causa) {
      if (causa.duplicado) {
        abrirDuplicado({ error: causa, alForzar: () => enviar(true) });
        return;
      }
      mensajeError.textContent = causa.message || "No se pudo pedir el cambio. Intenta de nuevo.";
      mensajeError.hidden = false;
    } finally {
      boton.disabled = false;
    }
  };
  form.addEventListener("submit", (evento) => {
    evento.preventDefault();
    return enviar(false);
  });
  contenedor.appendChild(form);
  return form;
}

export function crearAccionEliminar({ contenedor, url, alConfirmar }) {
  const boton = document.createElement("button");
  boton.type = "button";
  boton.className = "boton boton--secundario";
  boton.dataset.eliminarRegistro = "true";
  boton.textContent = "Borrar";
  boton.addEventListener("click", async () => {
    boton.disabled = true;
    try {
      const respuesta = await fetch(url, { method: "DELETE" });
      if (!respuesta.ok) throw new Error("No se pudo pedir que se borre el registro.");
      const cambio = await buscarPendiente((await respuesta.json()).id);
      abrirConfirmacion({ cambio, alConfirmar });
    } finally {
      boton.disabled = false;
    }
  });
  contenedor.appendChild(boton);
  return boton;
}
