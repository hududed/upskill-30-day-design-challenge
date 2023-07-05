from decimal import Decimal


def get_payment_method() -> str:
    return "paypal"

def process_payment_paypal(total: Decimal) -> None:
    username = input("Please enter your PayPal username: ")
    password = input("Please enter your PayPal password: ")
    password_masked = len(password) * "*"
    print(
        f"Processing PayPal payment of ${total:.2f} with username {username} and password {password_masked}..."
    )