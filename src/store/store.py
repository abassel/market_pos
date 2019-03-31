import json
from decimal import Decimal
from .offers import *   # Required for eval to work
from .cart import CartItem

class Store():

    """This class is used to load products and deals
       as well as convert cart and trigger calculations"""

    def __init__(self, prices, offers):

        ######### Load prices ########

        if type(prices) == str:
            with open(prices, 'r') as f:
                prices = json.load(f)

        self.prices = prices

        ######### Load offers ########

        if type(offers) == str:
            self.deals = []

            with open(offers, 'r') as f:
                offers = json.load(f)

            for key, value in offers.items():
                self.deals.append(eval(value))  # It is not the best way but we
        else:
            self.deals = offers

    def compute(self, cart):

        items = self.__convert2objects(cart)

        savings = self.deals
        savings.sort(key=lambda x: x.estimate_discount(items, self), reverse=True)

        for saving in savings:
            # Apply each savings to the items
            saving.apply_offer(items)

        receipt = "\n".join([item.render() for item in items])
        total = sum(items)

        return total, receipt

    def __convert2objects(self, cart):

        items = []

        for item in cart:
            item_name = self.prices[item.upper()]["name"]
            item_price = Decimal(self.prices[item.upper()]["price"])
            items.append(CartItem(code=item, name=item_name, price=item_price))

        return items

