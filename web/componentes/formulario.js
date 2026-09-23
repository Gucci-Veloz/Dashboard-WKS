// Formulario editable y guardado. UI-09.
// Al guardar con éxito, muestra confirmación y deja el dato
// actualizado a la vista. Si hay un error, lo dice en palabras
// normales y conserva lo que la persona escribió: los campos nunca
// se limpian ni se revierten cuando falla el guardado.

import { mostrarConfirmacion } from "/componentes/confirmacion.js";

export function crearFormulario({ contenedor, campos, guardar }) {
  contenedor.innerHTML = "";

  const form = document.createElement("form");
  form.className = "formulario";
  form.noValidate = true;

  const inputsPorNombre = {};

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

    grupo.appendChild(etiqueta);
    grupo.appendChild(input);
    form.appendChild(grupo);

    inputsPorNombre[campo.nombre] = input;
  }

  const mensajeError = document.createElement("p");
  mensajeError.className = "formulario__mensaje-error";
  mensajeError.dataset.errorGuardar = "true";
  mensajeError.hidden = true;

  const boton = document.createElement("button");
  boton.type = "submit";
  boton.className = "boton";
  boton.textContent = "Guardar";

  form.appendChild(mensajeError);
  form.appendChild(boton);

  form.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    mensajeError.hidden = true;
    boton.disabled = true;

    const datos = {};
    for (const [nombre, input] of Object.entries(inputsPorNombre)) {
      datos[nombre] = input.value;
    }

    try {
      const actualizado = await guardar(datos);
      if (actualizado) {
        for (const [nombre, input] of Object.entries(inputsPorNombre)) {
          if (nombre in actualizado) {
            input.value = actualizado[nombre];
          }
        }
      }
      mostrarConfirmacion(form, "Guardado. Los datos ya están actualizados.");
    } catch (error) {
      mensajeError.textContent =
        (error && error.message) || "No se pudo guardar. Intenta de nuevo.";
      mensajeError.hidden = false;
      // Los campos no se tocan: conservan lo que la persona escribió.
    } finally {
      boton.disabled = false;
    }
  });

  contenedor.appendChild(form);
  return form;
}
