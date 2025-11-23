"""Testes unitários para as entidades do domínio."""

import pytest

from domain.entities import Client, Order, OrderItem


class TestClient:
    """Casos de teste para a entidade Client."""

    def test_client_creation_valid(self):
        """Testa a criação de um cliente válido."""
        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        assert client.name == "João Silva"
        assert client.email == "joao@example.com"
        assert client.tier == "gold"

    def test_client_empty_name_raises_error(self):
        """Testa que nome vazio gera ValueError."""
        with pytest.raises(ValueError, match="O nome do cliente não pode estar vazio"):
            Client(name="", email="joao@example.com", tier="gold")

    def test_client_empty_email_raises_error(self):
        """Testa que email vazio gera ValueError."""
        with pytest.raises(ValueError, match="O email do cliente não pode estar vazio"):
            Client(name="João Silva", email="", tier="gold")

    def test_client_empty_tier_raises_error(self):
        """Testa que nível vazio gera ValueError."""
        with pytest.raises(ValueError, match="O nível do cliente não pode estar vazio"):
            Client(name="João Silva", email="joao@example.com", tier="")


class TestOrderItem:
    """Casos de teste para a entidade OrderItem."""

    def test_order_item_creation_valid(self):
        """Testa a criação de um item de pedido válido."""
        item = OrderItem(name="Produto A", price=100.0)
        assert item.name == "Produto A"
        assert item.price == 100.0

    def test_order_item_empty_name_raises_error(self):
        """Testa que nome vazio gera ValueError."""
        with pytest.raises(ValueError, match="O nome do item não pode estar vazio"):
            OrderItem(name="", price=100.0)

    def test_order_item_negative_price_raises_error(self):
        """Testa que preço negativo gera ValueError."""
        with pytest.raises(ValueError, match="O preço do item não pode ser negativo"):
            OrderItem(name="Produto A", price=-10.0)


class TestOrder:
    """Casos de teste para a entidade Order."""

    def test_order_creation_valid(self):
        """Testa a criação de um pedido válido."""
        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
        ]
        order = Order(client=client, items=items, total=120.0, discount_rate=0.20)

        assert order.client == client
        assert order.items == items
        assert order.total == 120.0
        assert order.discount_rate == 0.20

    def test_order_subtotal_calculation(self):
        """Testa o cálculo do subtotal."""
        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
        ]
        order = Order(client=client, items=items, total=120.0, discount_rate=0.20)

        assert order.subtotal == 150.0

    def test_order_discount_amount_calculation(self):
        """Testa o cálculo do valor do desconto."""
        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
        ]
        order = Order(client=client, items=items, total=120.0, discount_rate=0.20)

        assert order.discount_amount == 30.0

    def test_order_items_count(self):
        """Testa a propriedade de contagem de itens."""
        client = Client(name="João Silva", email="joao@example.com", tier="gold")
        items = [
            OrderItem(name="Produto A", price=100.0),
            OrderItem(name="Produto B", price=50.0),
            OrderItem(name="Produto C", price=25.0),
        ]
        order = Order(client=client, items=items, total=140.0, discount_rate=0.20)

        assert order.items_count == 3
