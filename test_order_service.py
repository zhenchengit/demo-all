import unittest
from order_service import Item, Order, CheckoutService

class CheckoutTests(unittest.TestCase):
    def order(self, amount, order_id="test"):
        order = Order(order_id)
        order.add("item", amount)
        return order

    def test_coupon_boundary(self):
        service = CheckoutService()
        below = service.quote(self.order("99.99"), "SAVE10")
        at = service.quote(self.order("100"), "SAVE10")
        self.assertEqual(below["discount"], "0.00")
        self.assertEqual(at["discount"], "10.00")
        self.assertEqual(at["shipping"], "8.00")
        self.assertEqual(at["tax"], "6.75")
        self.assertEqual(at["total"], "104.75")

    def test_tax_after_discount(self):
        quote = CheckoutService().quote(self.order("200"), "SAVE10")
        self.assertEqual(quote["tax"], "13.50")
        self.assertEqual(quote["total"], "193.50")

    def test_cart_changes(self):
        service = CheckoutService()
        order = self.order("50")
        service.quote(order)
        order.add("extra", "60")
        self.assertEqual(service.quote(order)["subtotal"], "110.00")
        order.items[0].quantity = 2
        self.assertEqual(service.quote(order)["subtotal"], "160.00")

    def test_shipping_changes_and_boundary(self):
        service = CheckoutService()
        order = self.order("50")
        self.assertEqual(service.quote(order)["shipping"], "8.00")
        self.assertEqual(service.quote(order, shipping="express")["shipping"], "20.00")
        self.assertEqual(service.quote(self.order("100"))["shipping"], "0.00")
        self.assertEqual(service.quote(self.order("200"), shipping="express")["shipping"], "20.00")
        with self.assertRaises(ValueError):
            service.quote(order, shipping="unsupported")

    def test_same_id_and_returned_quote_independence(self):
        service = CheckoutService()
        first = service.quote(self.order("10"))
        first["subtotal"] = "999"
        self.assertEqual(service.quote(self.order("90"))["subtotal"], "90.00")

    def test_independent_events(self):
        a, b = Order("a"), Order("b")
        a.add("item", "1")
        self.assertEqual(b.events, [])
        history = ["created"]
        c, d = Order("c", history), Order("d", history)
        c.add("item", "1")
        self.assertEqual(d.events, ["created"])
        self.assertEqual(history, ["created"])

    def test_quantities(self):
        for quantity in (1.9, "1.5", 0, -1, True, False, "NaN", "Infinity", None, "abc"):
            with self.subTest(quantity=quantity), self.assertRaises(ValueError):
                Item("item", "10", quantity)
        for quantity in (1, "2", 2.0):
            self.assertEqual(Item("item", "10", quantity).quantity, int(quantity))

    def test_demo_total(self):
        order = Order("demo")
        order.add("KEYBOARD", "79.95")
        order.add("MOUSE", "24.95", 2)
        self.assertEqual(CheckoutService().quote(order, "SAVE10")["total"], "125.62")

if __name__ == "__main__":
    unittest.main()
