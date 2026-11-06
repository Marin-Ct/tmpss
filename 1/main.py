from logger import OrderLogger
from factory import ItalianPizzaStore, AmericanPizzaStore
from order import OrderBuilder, OrderDirector


def main():
    print("=== SINGLETON ===")
    a, b = OrderLogger(), OrderLogger()
    print("Same logger instance?", a is b)

    print("\n=== FACTORY METHOD ===")
    italian, american = ItalianPizzaStore(), AmericanPizzaStore()
    margherita = italian.order_pizza("margherita")
    deepdish = american.order_pizza("deepdish")
    pepperoni = american.order_pizza("pepperoni")
    try:
        italian.order_pizza("deepdish")
    except ValueError as e:
        print("Error:", e)

    print("\n=== BUILDER ===")
    custom = (OrderBuilder()
              .for_customer("Marin")
              .add_pizza(margherita)
              .add_pizza(deepdish)
              .deliver_to("Str. Studenților 9, Chișinău")
              .pay_by("card")
              .with_note("No basil, please")
              .build())
    print(custom)

    director = OrderDirector(OrderBuilder())
    print()
    print(director.quick_pickup("Artur", pepperoni))
    print()
    print(director.student_delivery("Ana", "UTM Dorm 7", margherita, pepperoni))

    print("\n=== LOG HISTORY (Singleton shared state) ===")
    print(f"{len(OrderLogger().history)} messages stored in the single logger")


if __name__ == "__main__":
    main()
