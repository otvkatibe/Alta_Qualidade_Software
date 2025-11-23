from typing import List

from domain.entities import Client, Order, OrderItem
from domain.services import DiscountCalculator


class ProcessOrderUseCase:
    """
    Caso de uso para processar pedidos de clientes.

    Segue os princípios da Responsabilidade Única e Inversão de Dependência.
    """

    def __init__(self, discount_calculator: DiscountCalculator):
        """Inicializa o caso de uso de processamento de pedido."""
        self._discount_calculator = discount_calculator

    def execute(self, client: Client, items: List[OrderItem]) -> Order:
        """Processa um pedido para um cliente."""
        if not items:
            raise ValueError("O pedido deve conter pelo menos um item")

        # Calcula o subtotal
        subtotal = sum(item.price for item in items)

        # Obtém a taxa de desconto para o nível do cliente
        discount_rate = self._discount_calculator.get_discount_rate(client.tier)

        # Calcula o total final
        total = self._discount_calculator.calculate_discounted_price(
            subtotal, client.tier
        )

        # Cria a entidade do pedido
        order = Order(
            client=client,
            items=items,
            total=total,
            discount_rate=discount_rate,
        )

        return order


class GenerateOrderSummaryUseCase:
    """Caso de uso para gerar resumos de pedidos."""

    def execute(self, order: Order) -> str:
        """Gera um resumo formatado do pedido."""
        lines = []
        lines.append(f"Pedido de {order.client.name} (nível {order.client.tier})")
        lines.append("Itens:")

        for item in order.items:
            lines.append(f"  - {item.name}: R$ {item.price:.2f}")

        lines.append(f"Subtotal: R$ {order.subtotal:.2f}")
        lines.append(f"Desconto: {order.discount_rate * 100:.0f}%")
        lines.append(f"Valor do Desconto: R$ {order.discount_amount:.2f}")
        lines.append(f"Total: R$ {order.total:.2f}")

        return "\n".join(lines)
