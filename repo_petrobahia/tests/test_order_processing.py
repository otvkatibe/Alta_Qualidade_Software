"""Testes unitários para os casos de uso de processamento de pedidos."""

import pytest

from domain.entities import Client, OrderItem
from services.discount import TierDiscountCalculator
from use_cases.order_processing import (
    GenerateOrderSummaryUseCase,
    ProcessOrderUseCase,
)


class TestProcessOrderUseCase:
    """Casos de teste para ProcessOrderUseCase."""

    def test_process_order_gold_tier(self):
        """Testa o processamento de pedido para cliente nível gold."""
        calculator = TierDiscountCalculator()
        use_case = ProcessOrderUseCase(calculator)

        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
        ]

        order = use_case.execute(client, items)

        assert order.client == client
        assert order.items == items
        assert order.subtotal == 150.0
        assert order.discount_rate == 0.20
        assert order.total == 120.0

    def test_process_order_silver_tier(self):
        """Testa o processamento de pedido para cliente nível silver."""
        calculator = TierDiscountCalculator()
        use_case = ProcessOrderUseCase(calculator)

        client = Client(name="Maria Santos", email="maria@example.com", tier="silver")
        items = [OrderItem(name="Produto A", price=100.0)]

        order = use_case.execute(client, items)

        assert order.discount_rate == 0.10
        assert order.total == 90.0

    def test_process_order_empty_items_raises_error(self):
        """Testa que lista de itens vazia gera ValueError."""
        calculator = TierDiscountCalculator()
        use_case = ProcessOrderUseCase(calculator)

        client = Client(name="João Silva", email="joao@example.com", tier="gold")

        with pytest.raises(ValueError, match="O pedido deve conter pelo menos um item"):
            use_case.execute(client, [])


class TestGenerateOrderSummaryUseCase:
    """Casos de teste para GenerateOrderSummaryUseCase."""

    def test_generate_summary(self):
        """Testa a geração de resumo do pedido."""
        use_case = GenerateOrderSummaryUseCase()

        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
        ]

        # Cria manualmente um pedido para teste
        from domain.entities import Order

        order = Order(client=client, items=items, total=120.0, discount_rate=0.20)

        summary = use_case.execute(order)

        assert "João Silva" in summary
        assert "nível gold" in summary
        assert "Produto A" in summary
        assert "Produto B" in summary
        assert "R$ 100.00" in summary
        assert "R$ 50.00" in summary
        assert "20%" in summary
        assert "R$ 120.00" in summary

    def test_generate_summary_format(self):
        """Testa que o resumo contém todas as seções necessárias."""
        use_case = GenerateOrderSummaryUseCase()

        client = Client(name="Maria Santos", email="maria@example.com", tier="silver")
        items = [OrderItem(name="Produto X", price=75.0)]

        from domain.entities import Order

        order = Order(client=client, items=items, total=67.50, discount_rate=0.10)

        summary = use_case.execute(order)

        assert "Pedido de" in summary
        assert "Itens:" in summary
        assert "Subtotal:" in summary
        assert "Desconto:" in summary
        assert "Total:" in summary
