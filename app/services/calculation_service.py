from decimal import Decimal, ROUND_HALF_UP

MONEY = Decimal("0.01")
PRODUCT_PRICE_THRESHOLD = Decimal("350000")

def calculate_product_selling_price(cost_price):
    """Apply the catalog markup rule to physical products."""
    cost_price = money(cost_price)
    markup = Decimal("0.25") if cost_price > PRODUCT_PRICE_THRESHOLD else Decimal("0.20")
    return money(cost_price * (Decimal("1") + markup))

def money(value) -> Decimal:
    return Decimal(str(value or 0)).quantize(MONEY, rounding=ROUND_HALF_UP)

def calculate_item(quantity, cost_price, selling_price, discount=0):
    quantity = money(quantity)
    gross = money(quantity * money(selling_price))
    discount = money(discount)
    subtotal = money(gross - discount)
    hpp = money(quantity * money(cost_price))
    return {"subtotal": subtotal, "hpp": hpp, "profit": money(subtotal - hpp)}

def calculate_quotation(items, discount=0, tax=0):
    subtotal = sum((money(item["subtotal"]) for item in items), Decimal(0))
    hpp = sum((money(item["hpp"]) for item in items), Decimal(0))
    discount = money(discount)
    tax = money(tax)
    total = money(subtotal - discount + tax)
    profit = money(total - hpp)
    margin = (profit / total * 100).quantize(MONEY) if total else Decimal(0)
    return {"subtotal": money(subtotal), "hpp": money(hpp), "discount": discount, "tax": tax, "total": total, "profit": profit, "margin": margin}
