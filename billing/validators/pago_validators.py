"""
billing/validators/pago_validators.py

Implementaciones concretas de PagoValidator.

Para agregar una nueva regla de negocio (mora, periodo máximo, etc.):
  1. Crear una nueva clase que herede de PagoValidator.
  2. Implementar validate().
  3. Inyectarla en PagoService — sin tocar las clases existentes (OCP).
"""
from decimal import Decimal

from .base import PagoValidator


class NoPagosParciales(PagoValidator):
    """
    V1 — Regla de negocio: el monto pagado debe ser igual o mayor al total de
    la deuda. No se admiten abonos parciales.
    """

    def validate(self, deuda, monto_pagado: Decimal) -> None:
        if monto_pagado < deuda.monto_total:
            raise ValueError(
                f"No se permiten pagos parciales. "
                f"El monto total de la deuda es {deuda.monto_total} "
                f"y se intentó registrar {monto_pagado}."
            )


class DeudaPendiente(PagoValidator):
    """
    Garantiza que solo se pueda pagar una deuda que esté en estado 'pendiente'.
    """

    def validate(self, deuda, monto_pagado: Decimal) -> None:
        if deuda.estado != "pendiente":
            raise ValueError(
                f"La deuda no está pendiente de pago (estado actual: {deuda.estado})."
            )
