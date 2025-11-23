from abc import ABC, abstractmethod

from domain.entities import Client


class EmailSender(ABC):
    """Interface para envio de emails."""

    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> None:
        """Envia um email."""
        ...


class ClientValidator(ABC):
    """Interface para validação de clientes."""

    @abstractmethod
    def validate(self, client: Client) -> bool:
        """Valida os dados do cliente."""
        ...


class DiscountCalculator(ABC):
    """Interface para cálculo de descontos."""

    @abstractmethod
    def get_discount_rate(self, tier: str) -> float:
        """Obtém a taxa de desconto para um nível."""
        ...

    @abstractmethod
    def calculate_discounted_price(self, base_price: float, tier: str) -> float:
        """Calcula o preço com desconto aplicado."""
        ...
