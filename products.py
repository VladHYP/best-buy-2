class Product:
    def __init__(self, name, price, quantity):
        if name == "":
            raise Exception("Name cannot be empty")
        if price < 0:
            raise Exception("Price cannot be negative")
        if quantity < 0:
            raise Exception("Quantity cannot be negative")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True
        self.promotions = []

    def get_quantity(self):
        return self.quantity

    def set_quantity(self, quantity):
        if quantity < 0:
            raise Exception("Quantity cannot be negative")

        self.quantity = quantity
        if self.quantity == 0:
            self.deactivate()
        else:
            self.activate()

    def is_active(self):
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self):
        promotion_text = ""
        if self.promotions:
            promotion_names = ", ".join(
                promotion.name for promotion in self.promotions
            )
            promotion_text = f", Promotions: {promotion_names}"

        return (
            f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}"
            f"{promotion_text}"
        )

    def buy(self, quantity):
        if quantity <= 0:
            raise Exception("Quantity to buy must be greater than zero")

        if quantity > self.quantity:
            raise Exception("Not enough quantity available")

        self.quantity -= quantity

        if self.quantity == 0:
            self.deactivate()

        total_price = self.price * quantity

        if self.promotions:
            for promotion in self.promotions:
                original_price = self.price
                self.price = total_price / quantity
                total_price = promotion.apply_promotion(self, quantity)
                self.price = original_price

        return total_price

    def set_promotion(self, promotion):
        self.promotions = [promotion]

    def add_promotion(self, promotion):
        self.promotions.append(promotion)

    def clear_promotions(self):
        self.promotions = []

    def get_promotion(self):
        if not self.promotions:
            return None
        return self.promotions[0]

    def get_promotions(self):
        return self.promotions


class NonStockedProduct(Product):
    def __init__(self, name, price):
        super().__init__(name, price, 0)

    def buy(self, quantity):
        if quantity <= 0:
            raise Exception("Quantity to buy must be greater than zero")

        total_price = self.price * quantity

        if self.promotions:
            for promotion in self.promotions:
                original_price = self.price
                self.price = total_price / quantity
                total_price = promotion.apply_promotion(self, quantity)
                self.price = original_price

        return total_price

    def show(self):
        promotion_text = ""
        if self.promotions:
            promotion_names = ", ".join(
                promotion.name for promotion in self.promotions
            )
            promotion_text = f", Promotions: {promotion_names}"

        return (
            f"{self.name}, Price: ${self.price}, Quantity: Unlimited"
            f"{promotion_text}"
        )


class LimitedProduct(Product):
    def __init__(self, name, price, quantity, maximum):
        super().__init__(name, price, quantity)

        if maximum < 1:
            raise Exception("Maximum must be at least 1")

        self.maximum = maximum

    def buy(self, quantity):
        if quantity > self.maximum:
            raise Exception("Cannot buy more than the maximum allowed")

        return super().buy(quantity)

    def show(self):
        promotion_text = ""
        if self.promotions:
            promotion_names = ", ".join(
                promotion.name for promotion in self.promotions
            )
            promotion_text = f", Promotions: {promotion_names}"

        return (
            f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, "
            f"Maximum per order: {self.maximum}{promotion_text}"
        )