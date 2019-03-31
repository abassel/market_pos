from decimal import *

class AbstractOffer(object):

    """An interface for subclassing Offer classes."""

    def __init__(self, deal_code, target_product_code):
        self.deal_code = deal_code
        self.target_product = target_product_code.upper()

    def apply_offer(self, list_items):
        """
        All subclasses must implement this method to apply a discount to items in the cart
        Steps:
        - Get all items that were not used in previous discount
        - Apply discount by setting the discount property and used_in_discount=True
        """
        raise NotImplementedError()

    def estimate_discount(self, list_items, store):
        """
        All subclasses must implement this method, returning an
        estimation for the savings based on the carts content
        It is used to give customer the biggest discount first.
        Steps:
        - Get all items required to apply this discount to list_items
        - Calculate difference (price - discount price)
        - Return the difference BUT WITHOUT setting used_in_discount (It is only an estimation)
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.deal_code


class MultiBuyOffer(AbstractOffer):

    """
    Buy a certain quantity to get another quantity free.
    eg. a Buy One Get One Free offer would look like:

    MultiBuyOffer('<OFFER NAME>', '<PRODUCT CODE>', <#ITEMS REQUIRED>, <#ITEMS GET FREE>)

    Buy one coffee, get one coffee free
        MultiBuyOffer('BOGO-Coffee', 'CF1', 1, 1)

    and a buy two get one free would look like:
        MultiBuyOffer('BOGO-Coffee', 'CF1', 2, 1)

    To set a maximum limit to a special
    Buy two PRODUCT-A, get one free - Limit 3 per person
        MultiBuyOffer('BOGO-PRODUCT-A', 'CODE_A', 2, 1, 3)
    """

    def __init__(self, deal_code, target_product, charge_for_quantity, free_quantity, limit=99999):
        self.charge_for_quantity = charge_for_quantity
        self.free_quantity = free_quantity
        self.limit = limit
        super(MultiBuyOffer, self).__init__(deal_code, target_product)

    def apply_offer(self, list_items):
        """
        Set the flag for all the products that are involved in
        the transaction. Also, sets the item.discount to 100%=free=1.0
        """

        limit = self.limit
        while limit > 0:
            same_items_not_used = list(filter(lambda i: not i.used_in_discount and i.code == self.target_product, list_items))

            if len(same_items_not_used) < self.charge_for_quantity + self.free_quantity:
                # Not enough items to continue
                return

            for item in same_items_not_used[0:self.charge_for_quantity]:
                item.used_in_discount = True

            for item in same_items_not_used[self.charge_for_quantity: self.charge_for_quantity + self.free_quantity]:
                item.discount = Decimal(1)
                item.used_in_discount = True
                item.deal_code = self.deal_code

            limit -= 1

    def estimate_discount(self, list_items, store):
        S = store.prices

        items_not_used = list(filter(lambda i: not i.used_in_discount, list_items))

        if self.target_product not in items_not_used:
            # One of the needed products is not in the basket
            return Decimal(0)
        import math
        count_target = math.floor(items_not_used.count(self.target_product)/(self.charge_for_quantity + self.free_quantity))

        number_of_discounts = min(count_target, self.limit)

        return Decimal(S[self.target_product]["price"]) * Decimal(number_of_discounts)


class DependentDiscountOffer(AbstractOffer):

    """
    Target Product(target_product) gets a discount if Dependent Product(dependent_product) is present
    """

    def __init__(self, deal_code, target_product, dependent_product, discount, limit=99999):
        self.dependent_product = dependent_product
        self.discount = Decimal(str(discount))
        self.limit = limit
        super(DependentDiscountOffer, self).__init__(deal_code, target_product)

    def apply_offer(self, list_items):

        limit = self.limit
        while limit > 0:
            items_not_used = list(filter(lambda i: not i.used_in_discount, list_items))

            if self.target_product not in items_not_used or self.dependent_product not in items_not_used:
                # One of the needed products is not in the basket
                return

            i = items_not_used.index(self.target_product)
            items_not_used[i].used_in_discount = True
            items_not_used[i].discount = self.discount
            items_not_used[i].deal_code = self.deal_code

            i = items_not_used.index(self.dependent_product)
            items_not_used[i].used_in_discount = True
            limit -= 1

    def estimate_discount(self, list_items, store):
        S = store.prices

        items_not_used = list(filter(lambda i: not i.used_in_discount, list_items))

        if self.target_product not in items_not_used or self.dependent_product not in items_not_used:
            # One of the needed products is not in the basket
            return 0

        count_target = items_not_used.count(self.target_product)
        count_dependent = items_not_used.count(self.dependent_product)

        number_of_discounts = min(count_target, count_dependent, self.limit)

        return Decimal(S[self.target_product]["price"]) * self.discount*Decimal(number_of_discounts)


class ThresholdOffer(AbstractOffer):

    """
    After buying a certain quantity the price of all products
    gets a discount.
    """

    def __init__(self, deal_code, target_product, min_product, discount):
        self.dependent_product = target_product
        self.min_product = min_product
        self.discount = Decimal(str(discount))
        super(ThresholdOffer, self).__init__(deal_code, target_product)

    def apply_offer(self, list_items):

        items_not_used = list(filter(lambda i: not i.used_in_discount and i.code == self.target_product, list_items))

        if len(items_not_used) < self.min_product:
            # One of the needed products is not in the basket
            return

        for item in items_not_used:
            item.used_in_discount = True
            item.discount = self.discount
            item.deal_code = self.deal_code


    def estimate_discount(self, list_items, store):
        S = store.prices
        items = list(filter(lambda i: i.code == self.target_product, list_items))
        if len(items) >= self.min_product:
            return Decimal(S[self.target_product]["price"]) * self.discount * Decimal(len(items))

        return 0

