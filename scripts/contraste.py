#!/usr/bin/env python3
"""Verificador de contraste WCAG para tokens.css. UI-02.

Lee variables CSS (`--nombre: #rrggbb;`) y pares declarados en
comentarios (`/* par: --a sobre --b N */`), calcula el ratio de
contraste WCAG entre cada par y termina con código 1 si alguno no
alcanza su umbral N.

Solo usa la biblioteca estándar.
"""

import re
import sys

VAR_RE = re.compile(
    r"(--[a-zA-Z0-9-]+)\s*:\s*(#[0-9a-fA-F]{3,8}|[a-zA-Z-]+\([^)]*\))\s*;"
)
PAR_RE = re.compile(
    r"/\*\s*par:\s*(--[a-zA-Z0-9-]+)\s+sobre\s+(--[a-zA-Z0-9-]+)\s+([0-9.]+)\s*\*/"
)


def _hex_a_rgb(valor):
    valor = valor.lstrip("#")
    if len(valor) == 3:
        valor = "".join(c * 2 for c in valor)
    if len(valor) != 6:
        return None
    try:
        return tuple(int(valor[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def _canal_lineal(c):
    c = c / 255
    if c <= 0.03928:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def luminancia_relativa(rgb):
    r, g, b = (_canal_lineal(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio_contraste(rgb1, rgb2):
    l1, l2 = luminancia_relativa(rgb1), luminancia_relativa(rgb2)
    claro, oscuro = max(l1, l2), min(l1, l2)
    return (claro + 0.05) / (oscuro + 0.05)


def resolver_variable(nombre, variables, vistos=None):
    """Resuelve --nombre a un color hexadecimal, siguiendo var(--otro)."""
    if vistos is None:
        vistos = set()
    if nombre in vistos:
        return None
    vistos.add(nombre)

    valor = variables.get(nombre)
    if valor is None:
        return None

    m = re.match(r"var\((--[a-zA-Z0-9-]+)\)", valor)
    if m:
        return resolver_variable(m.group(1), variables, vistos)

    if valor.startswith("#"):
        return valor

    return None


def leer_variables_y_pares(ruta):
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()

    variables = {}
    for nombre, valor in VAR_RE.findall(texto):
        if nombre not in variables:
            variables[nombre] = valor.strip()

    pares = [(a, b, float(n)) for a, b, n in PAR_RE.findall(texto)]
    return variables, pares


def main(argv):
    if len(argv) < 2:
        print("uso: contraste.py <archivo.css> [otro.css ...]", file=sys.stderr)
        return 2

    hubo_fallo = False

    for ruta in argv[1:]:
        variables, pares = leer_variables_y_pares(ruta)

        if not pares:
            print(f"{ruta}: no se encontraron pares declarados (/* par: ... */)")
            hubo_fallo = True
            continue

        print(f"\n{ruta}")
        print(f"{'par':45} {'ratio':>8} {'minimo':>8}  resultado")
        print("-" * 75)

        for nombre_a, nombre_b, minimo in pares:
            hex_a = resolver_variable(nombre_a, variables)
            hex_b = resolver_variable(nombre_b, variables)

            etiqueta = f"{nombre_a} sobre {nombre_b}"

            if hex_a is None or hex_b is None:
                print(f"{etiqueta:45} {'--':>8} {minimo:>8}  ERROR (variable no resuelta)")
                hubo_fallo = True
                continue

            rgb_a, rgb_b = _hex_a_rgb(hex_a), _hex_a_rgb(hex_b)
            if rgb_a is None or rgb_b is None:
                print(f"{etiqueta:45} {'--':>8} {minimo:>8}  ERROR (color no hexadecimal)")
                hubo_fallo = True
                continue

            ratio = ratio_contraste(rgb_a, rgb_b)
            pasa = ratio >= minimo
            estado = "PASA" if pasa else "FALLA"
            if not pasa:
                hubo_fallo = True

            print(f"{etiqueta:45} {ratio:8.2f} {minimo:8.2f}  {estado}")

    print()
    return 1 if hubo_fallo else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
