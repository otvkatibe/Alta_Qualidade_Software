"""Testes unitários para o serviço de desconto."""

import pytest

from services.discount import QuantityDiscountCalculator, TierDiscountCalculator


class TestTierDiscountCalculator:
    """Casos de teste para TierDiscountCalculator."""

    def test_gold_tier_discount(self):
        """Testa o cálculo de desconto para o nível gold."""
        calculator = TierDiscountCalculator()
        assert calculator.get_discount_rate("gold") == 0.20

    def test_silver_tier_discount(self):
        """Testa o cálculo de desconto para o nível silver."""
        calculator = TierDiscountCalculator()
        assert calculator.get_discount_rate("silver") == 0.10

    def test_bronze_tier_discount(self):
        """Testa o cálculo de desconto para o nível bronze."""
        calculator = TierDiscountCalculator()
        assert calculator.get_discount_rate("bronze") == 0.05

    def test_unknown_tier_no_discount(self):
        """Testa que nível desconhecido não recebe desconto."""
        calculator = TierDiscountCalculator()
        assert calculator.get_discount_rate("platinum") == 0.0

    def test_case_insensitive_tier(self):
        """Testa que a correspondência de nível é case-insensitive."""
        calculator = TierDiscountCalculator()
        assert calculator.get_discount_rate("GOLD") == 0.20
        assert calculator.get_discount_rate("Silver") == 0.10

    def test_calculate_discounted_price_gold(self):
        """Testa o cálculo de preço com desconto do nível gold."""
        calculator = TierDiscountCalculator()
        result = calculator.calculate_discounted_price(100.0, "gold")
        assert result == 80.0

    def test_calculate_discounted_price_silver(self):
        """Testa o cálculo de preço com desconto do nível silver."""
        calculator = TierDiscountCalculator()
        result = calculator.calculate_discounted_price(100.0, "silver")
        assert result == 90.0

    def test_calculate_discounted_price_no_discount(self):
        """Testa o cálculo de preço sem desconto."""
        calculator = TierDiscountCalculator()
        result = calculator.calculate_discounted_price(100.0, "unknown")
        assert result == 100.0

    def test_negative_price_raises_error(self):
        """Testa que preço negativo gera ValueError."""
        calculator = TierDiscountCalculator()
        with pytest.raises(ValueError, match="O preço base não pode ser negativo"):
            calculator.calculate_discounted_price(-10.0, "gold")

    def test_custom_discount_rates(self):
        """Testa o calculador com taxas de desconto personalizadas."""
        custom_rates = {"platinum": 0.30, "gold": 0.25}
        calculator = TierDiscountCalculator(discount_rates=custom_rates)
        assert calculator.get_discount_rate("platinum") == 0.30
        assert calculator.get_discount_rate("gold") == 0.25


class TestQuantityDiscountCalculator:
    """Casos de teste para QuantityDiscountCalculator."""

    def test_quantity_10_or_more(self):
        """Testa 20% de desconto para 10+ itens."""
        calculator = QuantityDiscountCalculator()
        assert calculator.get_discount_rate(10) == 0.20
        assert calculator.get_discount_rate(15) == 0.20

    def test_quantity_5_to_9(self):
        """Testa 10% de desconto para 5-9 itens."""
        calculator = QuantityDiscountCalculator()
        assert calculator.get_discount_rate(5) == 0.10
        assert calculator.get_discount_rate(9) == 0.10

    def test_quantity_less_than_5(self):
        """Testa que não há desconto para menos de 5 itens."""
        calculator = QuantityDiscountCalculator()
        assert calculator.get_discount_rate(1) == 0.0
        assert calculator.get_discount_rate(4) == 0.0

    def test_apply_discount_10_items(self):
        """Testa a aplicação de desconto ao preço com 10 itens."""
        calculator = QuantityDiscountCalculator()
        result = calculator.apply_discount(100.0, 10)
        assert result == 80.0

    def test_apply_discount_5_items(self):
        """Testa a aplicação de desconto ao preço com 5 itens."""
        calculator = QuantityDiscountCalculator()
        result = calculator.apply_discount(100.0, 5)
        assert result == 90.0

    def test_apply_discount_3_items(self):
        """Testa a aplicação de desconto ao preço com 3 itens."""
        calculator = QuantityDiscountCalculator()
        result = calculator.apply_discount(100.0, 3)
        assert result == 100.0

    def test_negative_price_raises_error(self):
        """Testa que preço negativo gera ValueError."""
        calculator = QuantityDiscountCalculator()
        with pytest.raises(ValueError, match="O preço não pode ser negativo"):
            calculator.apply_discount(-10.0, 5)

    def test_negative_quantity_raises_error(self):
        """Testa que quantidade negativa gera ValueError."""
        calculator = QuantityDiscountCalculator()
        with pytest.raises(ValueError, match="A quantidade não pode ser negativa"):
            calculator.apply_discount(100.0, -5)
