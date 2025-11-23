"""Testes unitários para o caso de uso de cálculo de preço."""

import pytest

from domain.entities import OrderItem
from services.discount import QuantityDiscountCalculator
from services.tax import TaxCalculator
from use_cases.price_calculation import CalculateFinalPriceUseCase


class TestCalculateFinalPriceUseCase:
    """Casos de teste para CalculateFinalPriceUseCase."""

    def test_calculate_with_3_items(self):
        """Testa o cálculo com 3 itens (sem desconto por quantidade)."""
        quantity_discount = QuantityDiscountCalculator()
        tax_calculator = TaxCalculator(tax_rate=0.10)
        use_case = CalculateFinalPriceUseCase(quantity_discount, tax_calculator)

        items = [
            OrderItem(name="Produto A", price=50.0),
            OrderItem(name="Produto B", price=30.0),
            OrderItem(name="Produto C", price=20.0),
        ]

        # Subtotal: 100
        # Sem desconto por quantidade
        # Imposto: 10%
        # Final: 110.00
        result = use_case.execute(items)
        assert result == 110.0

    def test_calculate_with_5_items(self):
        """Testa o cálculo com 5 itens (10% de desconto por quantidade)."""
        quantity_discount = QuantityDiscountCalculator()
        tax_calculator = TaxCalculator(tax_rate=0.10)
        use_case = CalculateFinalPriceUseCase(quantity_discount, tax_calculator)

        items = [
            OrderItem(name="Produto A", price=20.0),
            OrderItem(name="Produto B", price=20.0),
            OrderItem(name="Produto C", price=20.0),
            OrderItem(name="Produto D", price=20.0),
            OrderItem(name="Produto E", price=20.0),
        ]

        # Subtotal: 100
        # Desconto por quantidade (5 itens): 10% -> 90
        # Imposto: 10% -> 99
        result = use_case.execute(items)
        assert result == 99.0

    def test_calculate_with_10_items(self):
        """Testa o cálculo com 10 itens (20% de desconto por quantidade)."""
        quantity_discount = QuantityDiscountCalculator()
        tax_calculator = TaxCalculator(tax_rate=0.10)
        use_case = CalculateFinalPriceUseCase(quantity_discount, tax_calculator)

        items = [OrderItem(name=f"Produto {i}", price=10.0) for i in range(10)]

        # Subtotal: 100
        # Desconto por quantidade (10 itens): 20% -> 80
        # Imposto: 10% -> 88
        result = use_case.execute(items)
        assert result == 88.0

    def test_empty_items_raises_error(self):
        """Testa que lista de itens vazia gera ValueError."""
        quantity_discount = QuantityDiscountCalculator()
        tax_calculator = TaxCalculator(tax_rate=0.10)
        use_case = CalculateFinalPriceUseCase(quantity_discount, tax_calculator)

        with pytest.raises(ValueError, match="A lista de itens não pode estar vazia"):
            use_case.execute([])

    def test_single_item(self):
        """Testa o cálculo com um único item."""
        quantity_discount = QuantityDiscountCalculator()
        tax_calculator = TaxCalculator(tax_rate=0.10)
        use_case = CalculateFinalPriceUseCase(quantity_discount, tax_calculator)

        items = [OrderItem(name="Produto A", price=100.0)]

        # Subtotal: 100
        # Sem desconto
        # Imposto: 10%
        # Final: 110.00
        result = use_case.execute(items)
        assert result == 110.0

    def test_result_rounded_to_two_decimals(self):
        """Testa que o resultado é arredondado para 2 casas decimais."""
        quantity_discount = QuantityDiscountCalculator()
        tax_calculator = TaxCalculator(tax_rate=0.10)
        use_case = CalculateFinalPriceUseCase(quantity_discount, tax_calculator)

        items = [
            OrderItem(name="Produto A", price=33.33),
            OrderItem(name="Produto B", price=33.33),
            OrderItem(name="Produto C", price=33.34),
        ]

        result = use_case.execute(items)
        # Deve ter exatamente 2 casas decimais
        assert round(result, 2) == result
