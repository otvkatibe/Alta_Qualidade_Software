BASES = {
    "diesel": 3.99,
    "gas": 5.19,
    "ethanol": 3.59,
    "lubricant": 25.0,
}

def calculate_price(type, qty):
    if type == "diesel":
        if qty > 1000:
            price = (BASES["diesel"] * qty) * 0.9
        else:
            if qty > 500:
                price = (BASES["diesel"] * qty) * 0.95
            else:
                price = BASES["diesel"] * qty
        print("Calc diesel", price)
        return price
    else:
        if type == "gas":
            if qty > 200:
                price = (BASES["gas"] * qty) - 100
            else:
                price = BASES["gas"] * qty
            print("Calc gas", price)
            return price
        else:
            if type == "ethanol":
                price = BASES["ethanol"] * qty
                if qty > 80:
                    price = price * 0.97
                print("Calc ethanol", price)
                return price
            else:
                if type == "lubricant":
                    x = 0
                    for i in range(qty):
                        x = x + BASES["lubricant"]
                    return x
                else:
                    print("Unknown type. Returning 0")
                    return 0
