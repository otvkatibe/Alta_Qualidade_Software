from dataclasses import dataclass

@dataclass
class Client:
    """Entidade de cliente com dados imutáveis."""

    name: str
    email: str
    tier: str

    def __post_init__(self):
        """Valida os dados do cliente após a inicialização."""
        if not self.name or not self.name.strip():
            raise ValueError("O nome do cliente não pode estar vazio")
        if not self.email or not self.email.strip():
            raise ValueError("O email do cliente não pode estar vazio")
        if not self.tier or not self.tier.strip():
            raise ValueError("O nível do cliente não pode estar vazio")


@dataclass
class OrderItem:
    """Entidade de item do pedido."""

    name: str
    price: float

    def __post_init__(self):
        """Valida os dados do item após a inicialização."""
        if not self.name or not self.name.strip():
            raise ValueError("O nome do item não pode estar vazio")
        if self.price < 0:
            raise ValueError("O preço do item não pode ser negativo")


@dataclass
class Order:
    """Entidade de pedido contendo informações do cliente e itens."""

    client: Client
    items: list[OrderItem]
    total: float
    discount_rate: float

    @property
    def subtotal(self) -> float:
        """Calcula o subtotal antes do desconto."""
        return sum(item.price for item in self.items)

    @property
    def discount_amount(self) -> float:
        """Calcula o valor do desconto."""
        return self.subtotal * self.discount_rate

    @property
    def items_count(self) -> int:
        """Retorna a quantidade de itens no pedido."""
        return len(self.items)
