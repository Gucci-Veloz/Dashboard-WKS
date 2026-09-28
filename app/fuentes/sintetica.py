from datetime import date, timedelta
from typing import Optional

from app.fuentes.base import FuenteDatos

N_TITULARES = 21
ESCENARIOS = ("tranquilo", "con_atencion")

# Índices (1-based) usados por el escenario con_atencion, elegidos para
# reproducir los tres asuntos de contratos/ejemplos/estado-atencion.json:
# un contrato cerca de vencer, un pago pendiente y un contacto incompleto.
INDICE_CONTRATO_CERCA_DE_VENCER = 4
INDICE_PAGO_PENDIENTE = 8
INDICE_CONTACTO_INCOMPLETO = 9


class FuenteSintetica(FuenteDatos):
    """Genera ~21 titulares sintéticos, deterministas, en dos escenarios."""

    def __init__(self, fecha_hoy: Optional[date] = None):
        self.fecha_hoy = fecha_hoy or date.today()

    def obtener_registros(self, escenario: Optional[str] = None) -> dict:
        escenario = escenario or "tranquilo"
        if escenario not in ESCENARIOS:
            raise ValueError(f"escenario desconocido: {escenario}")

        oficinas = []
        inquilinos = []
        contratos = []
        pagos = []

        for i in range(1, N_TITULARES + 1):
            numero = str(100 + i)

            oficinas.append(
                {
                    "id": i,
                    "tipo": "privada" if i % 2 == 0 else "compartida",
                    "numero": numero,
                    "piso": str((i - 1) // 5 + 1),
                    "m2": 12.0 + i,
                    "estatus": "ocupada",
                    "origen_dato": "sintetico",
                }
            )

            contacto = f"contacto{i:02d}@works.sintetico.example"
            if escenario == "con_atencion" and i == INDICE_CONTACTO_INCOMPLETO:
                contacto = ""

            inquilinos.append(
                {
                    "id": i,
                    "titular": f"Titular Sintético {i:02d}",
                    "contacto": contacto,
                    "origen_dato": "sintetico",
                }
            )

            inicio = self.fecha_hoy - timedelta(days=300)
            fin = self.fecha_hoy + timedelta(days=200)
            alerta_renovacion = "normal"
            if escenario == "con_atencion" and i == INDICE_CONTRATO_CERCA_DE_VENCER:
                fin = self.fecha_hoy + timedelta(days=12)
                alerta_renovacion = "cerca_de_vencer"

            contratos.append(
                {
                    "id": i,
                    "oficina_id": i,
                    "inquilino_id": i,
                    "inicio": inicio.isoformat(),
                    "fin": fin.isoformat(),
                    "alerta_renovacion": alerta_renovacion,
                    "origen_dato": "sintetico",
                }
            )

            estatus_pago = "pagado"
            if escenario == "con_atencion" and i == INDICE_PAGO_PENDIENTE:
                estatus_pago = "pendiente"

            pagos.append(
                {
                    "id": i,
                    "contrato_id": i,
                    "precio": 5000.0 + i * 100,
                    "deposito_garantia": 5000.0,
                    "fecha_pago": self.fecha_hoy.isoformat() if estatus_pago == "pagado" else "",
                    "forma_pago": "transferencia",
                    "estatus_pago": estatus_pago,
                    "origen_dato": "sintetico",
                }
            )

        return {
            "oficinas": oficinas,
            "inquilinos": inquilinos,
            "contratos": contratos,
            "pagos": pagos,
        }
