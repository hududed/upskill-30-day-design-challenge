from dataclasses import dataclass, field
from decimal import Decimal


class ItemNotFoundException(Exception):
    pass

@dataclass
class Item:
    name: str
    price: Decimal
    quantity: int

    def update_price(self, new_price: Decimal) -> None:
        self.price = new_price
    
    def update_quantity(self, new_quantity: int) -> None:
        self.quantity = new_quantity

    @property
    def subtotal(self) -> Decimal:
        return self.price * self.quantity

@dataclass
class ShoppingCart:
    items: list[Item] = field(default_factory=list)


    def add_item(self, item: Item) -> None:
        self.items.append(item)
    
    def remove_item(self, item_name: str) -> None:
        found_item = self.find_item(item_name)
        self.items.remove(found_item)
    
    def find_item(self, item_name: str) -> Item:
        for item in self.items:
            if item.name == item_name:
                return item
        raise ItemNotFoundException(f"Item '{item_name}' not found")

    @property
    def total(self) -> Decimal:
        return Decimal(sum(item.subtotal for item in self.items))
    
    def display(self) -> None:
            # Print the cart
        print("Shopping Cart:")
        print(f"{'Item':<10}{'Price':>10}{'Qty':>7}{'Total':>13}")
        for item in self.items:
            total_price = item.price * item.quantity
            print(
                f"{item.name:<12}${item.price:>7.2f}{item.quantity:>7}     ${total_price:>7.2f}"
            )
        print("=" * 40)
        print(f"Total: ${self.total:>7.2f}")
    
    def update_item_quantity(self, item_name: str, new_quantity: int) -> None:
        found_item = self.find_item(item_name)
        found_item.update_quantity(new_quantity)
    
    def update_item_price(self, item_name: str, new_price: Decimal) -> None:
        found_item = self.find_item(item_name)
        found_item.update_price(new_price)



def main() -> None:
    # Create a shopping cart and add some items to it
    cart = ShoppingCart(
        items=[
            Item("Apple", Decimal("1.5"), 10),
            Item("Banana", Decimal("2"), 2),
            Item("Pizza", Decimal("11.90"), 5),
        ],
    )

    cart.update_item_quantity("Apple", 10)
    cart.update_item_price("Pizza", Decimal("3.50"))

    # Remove an item
    cart.remove_item("Banana")

    cart.display()



if __name__ == "__main__":
    main()
