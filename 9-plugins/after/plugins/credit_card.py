from decimal import Decimal


def get_payment_method() -> str:
    return "cc"


def process_payment_cc(total: Decimal) -> None:
    card_number = input("Please enter your credit card number: ")
    expiration_date = input("Please enter your credit card expiration date: ")
    ccv = input("Please enter your credit card CCV: ")
    card_number_masked = card_number[-4:].rjust(len(card_number), "*")
    ccv_masked = len(ccv) * "*"
    print(
        f"Processing credit card payment of ${total:.2f} with card number {card_number_masked} and expiration date {expiration_date} and CCV {ccv_masked}..."
    )