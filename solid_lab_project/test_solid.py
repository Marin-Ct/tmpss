import unittest

from discounts import BulkDiscount, DiscountPolicy, NoDiscount, PercentageDiscount
from models import Item, Order
from notifiers import Notifier
from repository import InMemoryOrderRepository
from services import OrderService


def sample_order(qty=1):
    return Order(7, "Test", [Item("A", 100.0, qty), Item("B", 50.0, 1)])


class FakeNotifier(Notifier):
    def __init__(self):
        self.sent = []

    def send(self, customer, message):
        self.sent.append((customer, message))


class SRPTests(unittest.TestCase):
    def test_order_total(self):
        self.assertEqual(sample_order(2).total, 250.0)


class OCPTests(unittest.TestCase):
    def test_existing_policies(self):
        o = sample_order(1)
        self.assertEqual(NoDiscount().apply(o), 150.0)
        self.assertEqual(PercentageDiscount(20).apply(o), 120.0)
        self.assertEqual(BulkDiscount().apply(o), 150.0)
        self.assertEqual(BulkDiscount().apply(sample_order(5)), 495.0)

    def test_new_policy_without_touching_service(self):
        class FixedOff(DiscountPolicy):          # new code, nothing modified
            def apply(self, order):
                return order.total - 10

        svc = OrderService(FixedOff(), InMemoryOrderRepository(), FakeNotifier())
        self.assertEqual(svc.checkout(sample_order(1)), 140.0)


class DIPTests(unittest.TestCase):
    def test_service_works_with_fakes(self):
        repo, notifier = InMemoryOrderRepository(), FakeNotifier()
        OrderService(NoDiscount(), repo, notifier).checkout(sample_order(1))
        self.assertEqual(repo.get(7)["final_price"], 150.0)
        self.assertEqual(len(notifier.sent), 1)


if __name__ == "__main__":
    unittest.main()
