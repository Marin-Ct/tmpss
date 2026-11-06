from abc import ABC, abstractmethod

from models import Order


class DiscountPolicy(ABC):
    """Abstraction that OrderService depends on (OCP + DIP)."""

    @abstractmethod
    def apply(self, order: Order) -> float:
        """Return the final price of the order after discount."""


class NoDiscount(DiscountPolicy):
    def apply(self, order: Order) -> float:
        return order.total


class PercentageDiscount(DiscountPolicy):
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, order: Order) -> float:
        return round(order.total * (1 - self.percent / 100), 2)


class BulkDiscount(DiscountPolicy):
    """10% off when the order has at least `min_items` units."""

    def __init__(self, min_items: int = 5, percent: float = 10):
        self.min_items = min_items
        self.percent = percent

    def apply(self, order: Order) -> float:
        units = sum(i.quantity for i in order.items)
        if units >= self.min_items:
            return round(order.total * (1 - self.percent / 100), 2)
        return order.total
