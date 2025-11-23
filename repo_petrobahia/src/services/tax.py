class TaxCalculator:
    """Calcula impostos sobre preços."""

    def __init__(self, tax_rate: float = 0.10):
        """Inicializa o calculador de impostos."""
        if tax_rate < 0:
            raise ValueError("A taxa de imposto não pode ser negativa")
        self._tax_rate = tax_rate

    @property
    def tax_rate(self) -> float:
        """Taxa de imposto atual."""
        return self._tax_rate

    def calculate_tax(self, price: float) -> float:
        """Calcula o valor do imposto."""
        if price < 0:
            raise ValueError("O preço não pode ser negativo")
        return price * self._tax_rate

    def apply_tax(self, price: float) -> float:
        """Aplica o imposto ao preço."""
        if price < 0:
            raise ValueError("O preço não pode ser negativo")
        return price * (1 + self._tax_rate)
