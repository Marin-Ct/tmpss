from discounts import DiscountPolicy
from models import Order
from notifiers import Notifier
from repository import OrderRepository


class OrderService:
    """Coordinates the workflow. It knows only abstractions (DIP):
    which discount, storage and notifier are used is decided outside."""

    def __init__(self, discount: DiscountPolicy, repo: OrderRepository,
                 notifier: Notifier):
        self.discount = discount
        self.repo = repo
        self.notifier = notifier

    def checkout(self, order: Order) -> float:
        final_price = self.discount.apply(order)
        self.repo.save(order, final_price)
        self.notifier.send(
            order.customer,
            f"Order #{order.order_id} confirmed, total to pay: {final_price:.2f} MDL",
        )
        return final_price
