class TaxCalculator:
    """Calcula impostos sobre preços."""

    def __init__(self, tax_rate: float = 0.10):
        """
        Inicializa com a taxa de imposto.

        Args:
            tax_rate: Taxa de imposto em decimal (0.10 = 10%)
        """
        if tax_rate < 0:
            raise ValueError("A taxa de imposto não pode ser negativa")
        self._tax_rate = tax_rate

    @property
    def tax_rate(self) -> float:
        """Retorna a taxa de imposto atual."""
        return self._tax_rate

    def calculate_tax(self, price: float) -> float:
        """Calcula o valor do imposto para o preço fornecido."""
        if price < 0:
            raise ValueError("O preço não pode ser negativo")
        return price * self._tax_rate

    def apply_tax(self, price: float) -> float:
        """Aplica o imposto ao preço e retorna o total."""
        if price < 0:
            raise ValueError("O preço não pode ser negativo")
        return price * (1 + self._tax_rate)
