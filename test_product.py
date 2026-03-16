import pytest
from products import Product


def test_create_normal_product():
    product = Product("MacBook Air M2", 1450, 100)

    assert product.name == "MacBook Air M2"
    assert product.price == 1450
    assert product.quantity == 100
    assert product.is_active() is True


def test_create_invalid_product_raises_exception():
    with pytest.raises(Exception):
        Product("", 1450, 100)

    with pytest.raises(Exception):
        Product("MacBook Air M2", -10, 100)


def test_product_becomes_inactive_when_quantity_reaches_zero():
    product = Product("MacBook Air M2", 1450, 1)

    product.buy(1)

    assert product.quantity == 0
    assert product.is_active() is False


def test_product_purchase_updates_quantity_and_returns_total_price():
    product = Product("MacBook Air M2", 1450, 10)

    total_price = product.buy(2)

    assert total_price == 2900
    assert product.quantity == 8


def test_buying_more_than_available_raises_exception():
    product = Product("MacBook Air M2", 1450, 2)

    with pytest.raises(Exception):
        product.buy(3)