const mensaje = document.querySelector("[data-acceso-mensaje]");
const token = new URLSearchParams(window.location.search).get("token");
const MENSAJE_ENLACE_INVALIDO =
  "Este enlace ya no sirve. Pídele a Vania uno nuevo.";

function mostrarEnlaceInvalido() {
  mensaje.textContent = MENSAJE_ENLACE_INVALIDO;
  mensaje.classList.add("acceso__mensaje-error");
}

async function entrar() {
  if (!token) {
    mostrarEnlaceInvalido();
    return;
  }

  try {
    const respuesta = await fetch(
      `/api/acceso/entrar?token=${encodeURIComponent(token)}`,
      { credentials: "same-origin" },
    );
    if (!respuesta.ok) {
      mostrarEnlaceInvalido();
      return;
    }
    mensaje.textContent = "Listo, ya puedes entrar.";
    window.location.replace("/");
  } catch {
    mostrarEnlaceInvalido();
  }
}

entrar();
