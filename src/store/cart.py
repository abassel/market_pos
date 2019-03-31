from decimal import *


class CartItem:
    """
    This class stores all the product data needed to calculate
    normal price, discount price, and what deal triggered the
    discount


    """
    def __init__(self, code, name, price):
        self.code = code.upper()
        self.name = name
        self.price = Decimal(str(price))
        self.discount = Decimal(0)                  # Offers sets the discount percentage 0.0<discount<1.0 and final_price uses it
        self.used_in_discount = False               # Offers sets it to true when giving a discount so we use it once
        self.deal_code = ""                         # Used to print a discount in the receipt renderization

    @property
    def final_price(self):
        temp = self.price * (Decimal('1.00') - Decimal(self.discount))
        temp.quantize(Decimal('0.01'), context=Context(traps=[Inexact]))
        return temp


    def render(self):
        # CH1 - Chai    3.11
        temp = f"{self.code} - {self.name:<30} {self.price}"

        if self.final_price != self.price:
            temp = temp + f"\n {self.deal_code:^32}   -{self.price - self.final_price:.2f}"

        return temp

    def __radd__(self, y):
        """used by the sum and the end of the compute"""
        return self.final_price + Decimal(str(y))

    def __eq__(self, item):
        """ Used for "in" operator
            Offer classes searches for a product with
            this code before applying discount
        """
        return item == self.code

    def __repr__(self):
        return self.code

