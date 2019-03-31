
# Basic example of how to use the store class

from store import *

store = Store(prices="./src/prices.json", offers="./src/deals.json")

cart = ["CH1", "AP1", "CF1", "MK1"]

total, receipt = store.compute(cart)

print("-"*45)
print(receipt)
print("-"*45)
print(f"{total:.2f}")

