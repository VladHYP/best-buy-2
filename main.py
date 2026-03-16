import products
import promotions
import store


def start(best_buy_store):
    """Start the store user interface."""
    while True:
        print("\n   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        choice = input("Please choose a number: ")

        if choice == "1":
            print("------")
            active_products = best_buy_store.get_all_products()
            for index, product in enumerate(active_products, start=1):
                print(f"{index}. {product.show()}")
            print("------")

        elif choice == "2":
            total_quantity = best_buy_store.get_total_quantity()
            print(f"Total of {total_quantity} items in store")

        elif choice == "3":
            active_products = best_buy_store.get_all_products()

            print("------")
            for index, product in enumerate(active_products, start=1):
                print(f"{index}. {product.show()}")
            print("------")

            shopping_list = []

            while True:
                product_choice = input(
                    "Which product # do you want? "
                    "(Press Enter to finish) "
                )

                if product_choice == "":
                    break

                if not product_choice.isdigit():
                    print("Invalid product number.")
                    continue

                product_index = int(product_choice) - 1

                if product_index < 0 or product_index >= len(active_products):
                    print("Product number out of range.")
                    continue

                quantity_input = input("What amount do you want? ")

                if not quantity_input.isdigit():
                    print("Invalid quantity.")
                    continue

                quantity = int(quantity_input)

                if quantity <= 0:
                    print("Quantity must be greater than 0.")
                    continue

                product = active_products[product_index]

                if isinstance(product, products.LimitedProduct):
                    already_ordered = 0
                    for ordered_product, ordered_quantity in shopping_list:
                        if ordered_product == product:
                            already_ordered += ordered_quantity

                    if quantity + already_ordered > product.maximum:
                        print("Error: You exceeded the maximum allowed per order.")
                        continue

                elif not isinstance(product, products.NonStockedProduct):
                    already_ordered = 0
                    for ordered_product, ordered_quantity in shopping_list:
                        if ordered_product == product:
                            already_ordered += ordered_quantity

                    if quantity + already_ordered > product.get_quantity():
                        print("Error: Not enough products in stock.")
                        continue

                shopping_list.append((product, quantity))
                print("Product added to list!\n")

            if shopping_list:
                try:
                    total_price = best_buy_store.order(shopping_list)
                    print(f"Order made! Total payment: ${total_price}")
                except Exception as error:
                    print(f"Error while processing order: {error}")
            else:
                print("No products were ordered.")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid input, please try again.")


product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
    products.NonStockedProduct("Windows License", price=125),
    products.LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
]

second_half_price = promotions.SecondHalfPrice("Second Half price!")
third_one_free = promotions.ThirdOneFree("Third One Free!")
thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

product_list[0].set_promotion(second_half_price)
product_list[1].set_promotion(third_one_free)
product_list[3].set_promotion(thirty_percent)

best_buy = store.Store(product_list)
start(best_buy)