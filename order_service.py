"""Small checkout service. Run with Python 3.10+; no dependencies required.

Business rules:
- Quantities must be positive whole numbers.
- SAVE10 gives 10% off merchandise for orders of at least $100.
- Tax applies to discounted merchandise; shipping is not taxable.
- Standard shipping is free at $100 of discounted merchandise, otherwise $8.
- Express shipping always costs $20.
- Quotes must reflect the current cart and requested shipping method.
- Each order keeps its own history of events.
"""

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import json


def money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class Item:
    sku: str
    unit_price: Decimal
    quantity: int

    def __post_init__(self):
        self.unit_price = money(self.unit_price)
        self.quantity = int(self.quantity)
        if self.quantity <= 0 or self.unit_price < 0:
            raise ValueError("Invalid item price or quantity")


class Order:
    def __init__(self, order_id, events=[]):
        self.order_id = order_id
        self.items = []
        self.events = events

    def add(self, sku, unit_price, quantity=1):
        self.items.append(Item(sku, unit_price, quantity))
        self.events.append(f"Added {sku} to {self.order_id}")


class CheckoutService:
    def __init__(self, tax_rate="0.075"):
        self.tax_rate = Decimal(tax_rate)
        self._quotes = {}

    def quote(self, order, coupon=None, shipping="standard"):
        if shipping not in ("standard", "express"):
            raise ValueError("Unsupported shipping method")
        cache_key = (order.order_id, coupon)
        if cache_key in self._quotes:
            return dict(self._quotes[cache_key])

        subtotal = sum((item.unit_price * item.quantity for item in order.items), Decimal("0"))
        discount = Decimal("0")
        if coupon == "SAVE10" and subtotal > Decimal("100"):
            discount = money(subtotal * Decimal("0.10"))
        merchandise = subtotal - discount
        delivery = Decimal("20") if shipping == "express" else (
            Decimal("0") if merchandise >= Decimal("100") else Decimal("8")
        )
        tax = money(subtotal * self.tax_rate)
        result = {
            "order_id": order.order_id,
            "subtotal": str(money(subtotal)),
            "discount": str(money(discount)),
            "shipping": str(money(delivery)),
            "tax": str(tax),
            "total": str(money(merchandise + delivery + tax)),
        }
        self._quotes[cache_key] = result
        return dict(result)


def main():
    order = Order("DEMO-1001")
    order.add("KEYBOARD", "79.95")
    order.add("MOUSE", "24.95", 2)
    print(json.dumps(CheckoutService().quote(order, coupon="SAVE10"), indent=2))


if __name__ == "__main__":
    main()
