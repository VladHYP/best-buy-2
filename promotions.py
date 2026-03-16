from abc import ABC, abstractmethod


class Promotion(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        pass


class PercentDiscount(Promotion):
    def __init__(self, name, percent):
        super().__init__(name)
        if percent < 0 or percent > 100:
            raise Exception("Percent must be between 0 and 100")
        self.percent = percent

    def apply_promotion(self, product, quantity) -> float:
        full_price = product.price * quantity
        discount = full_price * (self.percent / 100)
        return full_price - discount


class SecondHalfPrice(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        pairs = quantity // 2
        leftover = quantity % 2
        return (pairs * product.price * 1.5) + (leftover * product.price)


class ThirdOneFree(Promotion):
    def apply_promotion(self, product, quantity) -> float:
        paid_items = quantity - (quantity // 3)
        return paid_items * product.price
