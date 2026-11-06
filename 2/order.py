"""BUILDER - step-by-step construction of a complex Order."""
from dataclasses import dataclass, field
from pizza import Pizza


@dataclass
class Order:
    customer: str = ""
    pizzas: list = field(default_factory=list)
    address: str = "Pick-up in store"
    payment: str = "cash"
    note: str = ""
    discount: float = 0.0          # percent

    @property
    def total(self) -> float:
        return sum(p.price for p in self.pizzas) * (1 - self.discount / 100)

    def __str__(self) -> str:
        items = "\n".join(f"   - {p}" for p in self.pizzas)
        return (f"Order for {self.customer}\n{items}\n"
                f"   Address : {self.address}\n"
                f"   Payment : {self.payment}\n"
                f"   Note    : {self.note or '-'}\n"
                f"   Discount: {self.discount:.0f}%\n"
                f"   TOTAL   : {self.total:.2f} MDL")


class OrderBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._order = Order()
        return self

    def for_customer(self, name: str):
        self._order.customer = name
        return self

    def add_pizza(self, pizza: Pizza):
        self._order.pizzas.append(pizza)
        return self

    def deliver_to(self, address: str):
        self._order.address = address
        return self

    def pay_by(self, method: str):
        self._order.payment = method
        return self

    def with_note(self, note: str):
        self._order.note = note
        return self

    def with_discount(self, percent: float):
        self._order.discount = percent
        return self

    def build(self) -> Order:
        if not self._order.customer or not self._order.pizzas:
            raise ValueError("Order needs a customer and at least one pizza")
        order, _ = self._order, self.reset()
        return order


class OrderDirector:
    """Ready-made recipes using the same builder."""

    def __init__(self, builder: OrderBuilder):
        self.builder = builder

    def quick_pickup(self, customer: str, pizza: Pizza) -> Order:
        return self.builder.for_customer(customer).add_pizza(pizza).build()

    def student_delivery(self, customer: str, address: str, *pizzas) -> Order:
        self.builder.for_customer(customer).deliver_to(address)\
            .pay_by("card").with_discount(10)
        for p in pizzas:
            self.builder.add_pizza(p)
        return self.builder.build()
