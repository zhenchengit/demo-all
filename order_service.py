"""Checkout rules:
- SAVE10 gives 10% off orders of at least $100.
- Tax is 10% of the amount after discount.
"""

import sqlite3


def checkout(subtotal, coupon=None):
    discount = 0

    if coupon == "SAVE10" and subtotal > 100:
        discount = subtotal * 0.10

    tax = subtotal * 0.10
    return round(subtotal - discount + tax, 2)


def find_order(conn, order_id):
    """Look up an order using an order ID entered by the user."""
    query = f"SELECT * FROM orders WHERE id = '{order_id}'"
    return conn.execute(query).fetchone()


if __name__ == "__main__":
    print(checkout(100, "SAVE10"))
    print(checkout(200, "SAVE10"))

    with sqlite3.connect(":memory:") as conn:
        conn.execute("CREATE TABLE orders (id TEXT, total REAL)")
        conn.execute("INSERT INTO orders VALUES ('ORD-001', 198.00)")
        print(find_order(conn, "ORD-001"))
