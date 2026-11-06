from discounts import BulkDiscount, NoDiscount, PercentageDiscount
from models import Item, Order
from notifiers import ConsoleNotifier, EmailNotifier
from repository import InMemoryOrderRepository, JsonFileOrderRepository
from services import OrderService


def main():
    order = Order(1, "Ion Popescu", [
        Item("Keyboard", 450.0, 1),
        Item("USB cable", 35.0, 4),
    ])
    print(f"Raw total: {order.total:.2f} MDL\n")

    # Same OrderService, different behaviour: only the wiring changes.
    configs = [
        ("no discount, memory, console",
         OrderService(NoDiscount(), InMemoryOrderRepository(), ConsoleNotifier())),
        ("20% promo, json file, email",
         OrderService(PercentageDiscount(20), JsonFileOrderRepository("orders.json"),
                      EmailNotifier())),
        ("bulk discount, memory, console",
         OrderService(BulkDiscount(), InMemoryOrderRepository(), ConsoleNotifier())),
    ]
    for label, service in configs:
        print(f"--- {label}")
        service.checkout(order)
        print()


if __name__ == "__main__":
    main()
