from legacy.pedido_service import processar_pedido
from legacy.clients import cadastrar_cliente

orders = [
    {"Client": "TransLog", "Product": "diesel", "Qty": 1200, "Voucher": "MEGA10"},
    {"Client": "MoveMais", "Product": "gasolina", "Qty": 300, "Voucher": None},
    {"Client": "EcoFrota", "Product": "etanol", "Qty": 50, "Voucher": "NOVO5"},
    {"Client": "PetroPark", "Product": "lubrificante", "Qty": 12, "Voucher": "LUB2"},
]

clients = [
    {"nome": "Ana Paula", "email": "ana@@petrobahia", "cnpj": "123"},
    {"nome": "Carlos", "email": "carlos@petrobahia.com", "cnpj": "456"},
]

print("==== Início processamento PetroBahia ====")

for c in clientes:
    ok = cadastrar_cliente(c)
    if ok:
        print("cliente ok:", c["nome"])
    else:
        print("cliente com problema:", c)

valores = []
for p in pedidos:
    v = processar_pedido(p)
    valores.append(v)
    print("pedido:", p, "-- valor final:", v)

print("TOTAL =", sum(valores))
print("==== Fim processamento PetroBahia ====")
