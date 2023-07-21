from dataclasses import dataclass
from decimal import Decimal

from tabulate import tabulate


@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int


def main():
    # Create a shopping cart
    items = [
        Item("Apple", Decimal("1.50"), 10),
        Item("Banana", Decimal("2.00"), 2),
        Item("Pizza", Decimal("11.90"), 5),
    ]

    total = sum(item.price * item.quantity for item in items)

    data = [
        [item.name, item.price, item.quantity, item.price * item.quantity]
        for item in items
    ]

    # Print the cart
    print("Shopping Cart:")
    print(tabulate(data, headers=["Item", "Price", "Qty", "Total"], floatfmt=".2f"))
    print("=" * 40)
    print(f"Total: ${total:>7.2f}")


if __name__ == "__main__":
    main()
