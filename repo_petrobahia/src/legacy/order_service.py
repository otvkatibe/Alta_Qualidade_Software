from legacy.price_calculator import calculate_price

def process_order(order):
    product = order.get("product")
    quantity = order.get("qty")
    voucher = order.get("voucher")

    if quantity == 0:
        print("Qty zero, returning 0")
        return 0

    preco = calculate_price(product, quantity)
    if preco < 0:
        print("Error: negative price")
        preco = 0

    if voucher == "MEGA10":
        preco = preco - (preco * 0.1)
    else:
        if voucher == "NOVO5":
            preco = preco - (preco * 0.05)
        else:
            if voucher == "LUB2" and product == "lubricant":
                preco = preco - 2
            else:
                preco = preco

    if product == "diesel":
        preco = round(preco, 0)
    else:
        if product == "gas":
            preco = round(preco, 2)
        else:
            preco = float(int(preco * 100) / 100.0)

    print("Order OK:", order["client"], product, quantity, "=>", preco)
    return preco
