
# Basic example of how to use the store class

from store import *


def main():
    store = Store(prices="./src/prices.json", offers="./src/deals.json")

    cart = []

    while True:

        total, receipt = store.compute(cart)

        print("-"*45)
        print(receipt)
        print("-"*45)
        print(f"{total:.2f}")

        print("\n\nAvailable codes ", list(store.prices.keys()))
        code = input("Enter product code(type q to exit and ENTER to clear):")

        if code == "q":
            return

        if code == "":
            cart = []
            continue

        if code in store.prices:
            cart.append(code)
        else:
            print("**Invalid product code**")


if __name__ == "__main__":
    main()
