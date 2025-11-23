"""Testes unitários para o serviço calculador de impostos."""

import pytest

from services.tax import TaxCalculator


class TestTaxCalculator:
    """Casos de teste para TaxCalculator."""

    def test_default_tax_rate(self):
        """Testa que a taxa de imposto padrão é 10%."""
        calculator = TaxCalculator()
        assert calculator.tax_rate == 0.10

    def test_custom_tax_rate(self):
        """Testa a inicialização com taxa de imposto personalizada."""
        calculator = TaxCalculator(tax_rate=0.15)
        assert calculator.tax_rate == 0.15

    def test_negative_tax_rate_raises_error(self):
        """Testa que taxa de imposto negativa gera ValueError."""
        with pytest.raises(ValueError, match="A taxa de imposto não pode ser negativa"):
            TaxCalculator(tax_rate=-0.05)

    def test_calculate_tax(self):
        """Testa o cálculo do valor do imposto."""
        calculator = TaxCalculator(tax_rate=0.10)
        tax_amount = calculator.calculate_tax(100.0)
        assert tax_amount == 10.0

    def test_calculate_tax_different_rate(self):
        """Testa o cálculo de imposto com taxa diferente."""
        calculator = TaxCalculator(tax_rate=0.15)
        tax_amount = calculator.calculate_tax(200.0)
        assert tax_amount == 30.0

    def test_apply_tax(self):
        """Testa a aplicação de imposto ao preço."""
        calculator = TaxCalculator(tax_rate=0.10)
        total = calculator.apply_tax(100.0)
        assert abs(total - 110.0) < 0.01

    def test_apply_tax_different_rate(self):
        """Testa a aplicação de taxa de imposto diferente."""
        calculator = TaxCalculator(tax_rate=0.20)
        total = calculator.apply_tax(50.0)
        assert total == 60.0

    def test_calculate_tax_negative_price_raises_error(self):
        """Testa que preço negativo gera ValueError em calculate_tax."""
        calculator = TaxCalculator()
        with pytest.raises(ValueError, match="O preço não pode ser negativo"):
            calculator.calculate_tax(-10.0)

    def test_apply_tax_negative_price_raises_error(self):
        """Testa que preço negativo gera ValueError em apply_tax."""
        calculator = TaxCalculator()
        with pytest.raises(ValueError, match="O preço não pode ser negativo"):
            calculator.apply_tax(-10.0)

    def test_zero_tax_rate(self):
        """Testa o calculador com taxa de imposto zero."""
        calculator = TaxCalculator(tax_rate=0.0)
        assert calculator.apply_tax(100.0) == 100.0
