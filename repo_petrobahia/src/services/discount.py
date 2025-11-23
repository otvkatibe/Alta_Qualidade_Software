from typing import Optional

from domain.services import DiscountCalculator as IDiscountCalculator


class TierDiscountCalculator(IDiscountCalculator):
    """
    Calcula descontos baseados no nível do cliente.

    Aberto para extensão (novos níveis podem ser adicionados) mas fechado
    para modificação.
    """

    DEFAULT_DISCOUNT_RATES = {
        "gold": 0.20,
        "silver": 0.10,
        "bronze": 0.05,
    }

    def __init__(self, discount_rates: Optional[dict[str, float]] = None):
        """Inicializa o calculador de descontos."""
        self._discount_rates = discount_rates or self.DEFAULT_DISCOUNT_RATES

    def get_discount_rate(self, tier: str) -> float:
        """Obtém a taxa de desconto do nível."""
        return self._discount_rates.get(tier.lower(), 0.0)

    def calculate_discounted_price(self, base_price: float, tier: str) -> float:
        """Calcula o preço com desconto do nível."""
        if base_price < 0:
            raise ValueError("O preço base não pode ser negativo")

        discount_rate = self.get_discount_rate(tier)
        return base_price * (1 - discount_rate)


class QuantityDiscountCalculator:
    """Calcula descontos baseados na quantidade de itens."""

    def __init__(self):
        """Inicializa o calculador de desconto por quantidade."""
        self._thresholds = [
            (10, 0.20),  # 10+ itens: 20% de desconto
            (5, 0.10),  # 5-9 itens: 10% de desconto
            (0, 0.0),  # <5 itens: sem desconto
        ]

    def get_discount_rate(self, quantity: int) -> float:
        """Obtém a taxa de desconto por quantidade."""
        for threshold, rate in self._thresholds:
            if quantity >= threshold:
                return rate
        return 0.0

    def apply_discount(self, price: float, quantity: int) -> float:
        """Aplica o desconto por quantidade ao preço."""
        if price < 0:
            raise ValueError("O preço não pode ser negativo")
        if quantity < 0:
            raise ValueError("A quantidade não pode ser negativa")

        discount_rate = self.get_discount_rate(quantity)
        return price * (1 - discount_rate)
