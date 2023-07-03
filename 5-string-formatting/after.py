from dataclasses import dataclass
from decimal import Decimal


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

    # Print the cart
    print("Shopping Cart:")
    print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
    for item in items:
        total_price = item.price * item.quantity
        print(f"{item.name:<12}${item.price:>7.2f}{item.quantity:>7}     ${total_price:>7.2f}")
    print("=" * 40)
    print(f"Total: ${total:>7.2f}")


if __name__ == "__main__":
    main()
