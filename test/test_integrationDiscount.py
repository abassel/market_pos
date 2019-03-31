
from src.store import *

# Integration tests

products = {
    "CH1": {"name": "Chai", "price": "3.11"},
    "AP1": {"name": "Apples", "price": "6.00"},
    "CF1": {"name": "Coffee", "price": "11.23"},
    "MK1": {"name": "Milk", "price": "4.75"},
    "OM1": {"name": "Oatmeal", "price": "3.69"}
}

BOGO = MultiBuyOffer("BOGO", "CF1", 1, 1)
APPL = ThresholdOffer("APPL", "AP1", 3, '0.25')
APOM = DependentDiscountOffer("APOM", "AP1", "OM1", Decimal(0.5))
CHMK = DependentDiscountOffer("CHMK", "MK1", "CH1", Decimal(1.0), limit=1)  # 1==100% Discount==Free

savings = [BOGO, APOM, CHMK, APPL]

local_store = Store(prices=products, offers=savings)

def test_Integration_SingleProduct_ExpectPass():

    user_cart = ["CH1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('3.11')


def test_Integration_FreeMilk_ExpectPass():

    user_cart = ["CH1", "AP1", "CF1", "MK1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('20.34')


def test_Integration_Discount_ExpectPass():

    user_cart = ["CH1", "AP1", "AP1", "AP1", "MK1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('16.61')


def test_Integration_HalfOffApples_ExpectPass():

    user_cart = ["MK1", "AP1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('10.75')


def test_Integration_BuyOneGetOneFree_ExpectPass():

    user_cart = ["CF1", "CF1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('11.23')


def test_Integration_25OffFor3OrMore_ExpectPass():

    user_cart = ["AP1", "AP1", "CH1", "AP1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('16.61')


def test_Integration_25OffFor3OrMore_2_ExpectPass():

    user_cart = ["AP1", "AP1", "CH1", "AP1", "AP1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('21.11')


def test_Integration_Buy4Pay2Coffes_ExpectPass():

    user_cart = ["CF1", "CF1", "CF1", "CF1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('22.46')


def test_Integration_Buy5Pay2Coffes_ExpectPass():

    user_cart = ["CF1", "CF1", "CF1", "CF1", "CF1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('33.69')


def test_Integration_Buy2ApplesDontPayLess_ExpectPass():

    user_cart = ["AP1", "AP1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('12.00')


def test_Integration_Buy3ApplesPayLess_ExpectPass():

    user_cart = ["AP1", "AP1", "AP1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('13.50')


def test_Integration_BuyManyApplesPayLess_ExpectPass():

    user_cart = ["AP1", "AP1", "AP1", "AP1", "AP1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('22.50')


def test_Integration_ConflictAppleDealWithOatmealDeal_AppleWins_ExpectPass():

    user_cart = ["AP1", "AP1", "AP1", "OM1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('17.19')


def test_Integration_ConflictAppleDealWithOatmealDeal_OatmealWins_ExpectPass():

    # if we apply the apple deal:
    #               3x4.50 + 2x3.69=20.88
    #
    # if we apply the oatmeal deal:
    #               2x3.00 + 6 + 2x3.69=19.38

    user_cart = ["AP1", "AP1", "AP1", "OM1", "OM1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('19.38')


def test_Integration_FreeMilkDeal_ExpectPass():

    user_cart = ["CH1", "MK1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('3.11')


def test_Integration_FreeMilkDealWithLimit_ExpectPass():

    user_cart = ["CH1", "MK1", "CH1", "MK1"]

    total, receipt = local_store.compute(user_cart)

    assert total == Decimal('10.97')


def test_Integration_BogoWithLimit_ExpectPass():
    products = {
        "CF1": {"name": "Coffee", "price": "11.23"}
    }

    BOGO = MultiBuyOffer("BOGO", "CF1", 1, 1, 1)

    savings = [BOGO]

    MyStore = Store(prices=products, offers=savings)

    user_cart = ["CF1", "CF1", "CF1", "CF1", "CF1"]

    total, receipt = MyStore.compute(user_cart)

    assert total == Decimal('44.92')


def test_BogoWithLimitPrediction_ExpectPass():

    products = {
        "CF1": {"name": "Coffee", "price": "11.23"}
    }

    BOGO = MultiBuyOffer("BOGO", "CF1", 1, 1, 1)

    savings = [BOGO]

    MyStore = Store(prices=products, offers=savings)

    user_cart = ["CF1", "CF1", "CF1", "CF1", "CF1"]

    user_cart_obj = MyStore._Store__convert2objects(user_cart)

    savings = BOGO.estimate_discount(user_cart_obj, MyStore)

    assert savings == Decimal('11.23')


def test_BogoWithLimit2Prediction_ExpectPass():

    products = {
        "CF1": {"name": "Coffee", "price": "11.23"}
    }

    BOGO = MultiBuyOffer("BOGO", "CF1", 1, 1, 2)

    savings = [BOGO]

    MyStore = Store(prices=products, offers=savings)

    user_cart = ["CF1", "CF1", "CF1", "CF1", "CF1"]

    user_cart_obj = MyStore._Store__convert2objects(user_cart)

    total_savings = BOGO.estimate_discount(user_cart_obj, MyStore)

    assert total_savings == Decimal('22.46')

    total, receipt = MyStore.compute(user_cart)

    assert total == Decimal('33.69')

    #########################################

    user_cart = ["CF1", "CF1"]

    user_cart_obj = MyStore._Store__convert2objects(user_cart)

    total_savings = BOGO.estimate_discount(user_cart_obj, MyStore)

    assert total_savings == Decimal('11.23')

    total, receipt = MyStore.compute(user_cart)

    assert total == Decimal('11.23')

    #########################################

    user_cart = ["CF1", "CF1", "CF1"]

    user_cart_obj = MyStore._Store__convert2objects(user_cart)

    total_savings = BOGO.estimate_discount(user_cart_obj, MyStore)

    assert total_savings == Decimal('11.23')

    total, receipt = MyStore.compute(user_cart)

    assert total == Decimal('22.46')

