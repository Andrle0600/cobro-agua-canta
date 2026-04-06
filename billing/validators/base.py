"""
billing/validators/base.py

Define la interfaz abstracta que todo validador de pago debe implementar.

Principios SOLID aplicados:
  - ISP: los validadores son pequeñas interfaces de una sola responsabilidad.
  - OCP: se pueden agregar nuevas reglas sin modificar las existentes.
  - DIP: PagoService depende de esta abstracción, no de validadores concretos.
"""
from abc import ABC, abstractmethod
from decimal import Decimal


class PagoValidator(ABC):
    """Interfaz base para validadores de un intento de pago."""

    @abstractmethod
    def validate(self, deuda, monto_pagado: Decimal) -> None:
        """
        Valida si el pago puede proceder.

        Args:
            deuda:        Instancia de Deuda contra la que se paga.
            monto_pagado: Monto que el tesorero intenta registrar.

        Raises:
            ValueError: si la validación falla, con un mensaje descriptivo.
        """
        ...
