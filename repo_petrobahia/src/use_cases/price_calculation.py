from typing import List

from domain.entities import OrderItem
from services.discount import QuantityDiscountCalculator
from services.tax import TaxCalculator


class CalculateFinalPriceUseCase:
    """
    Caso de uso para calcular preço final com descontos por quantidade e impostos.

    Substitui a função legada calculate_final_price com uma abordagem mais
    estruturada seguindo os princípios SOLID.
    """

    def __init__(
        self,
        quantity_discount: QuantityDiscountCalculator,
        tax_calculator: TaxCalculator,
    ):
        """
        Inicializa o caso de uso com os calculadores.

        Args:
            quantity_discount: Calculador para descontos baseados em quantidade.
            tax_calculator: Calculador para impostos.
        """
        self._quantity_discount = quantity_discount
        self._tax_calculator = tax_calculator

    def execute(self, items: List[OrderItem]) -> float:
        """
        Calcula o preço final: subtotal → desconto por quantidade → imposto.

        Args:
            items: Lista de itens do pedido.

        Returns:
            Preço final com 2 casas decimais.

        Raises:
            ValueError: Se a lista de itens estiver vazia.
        """
        if not items:
            raise ValueError("A lista de itens não pode estar vazia")

        # Calcula o subtotal
        subtotal = sum(item.price for item in items)

        # Aplica desconto por quantidade
        quantity = len(items)
        price_with_discount = self._quantity_discount.apply_discount(subtotal, quantity)

        # Aplica imposto
        final_price = self._tax_calculator.apply_tax(price_with_discount)

        return round(final_price, 2)
