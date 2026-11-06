from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Item:
    name: str
    price: float
    quantity: int = 1

    @property
    def subtotal(self) -> float:
        return round(self.price * self.quantity, 2)


@dataclass
class Order:
    """Only holds order data and the raw (pre-discount) total."""
    order_id: int
    customer: str
    items: List[Item] = field(default_factory=list)

    @property
    def total(self) -> float:
        return round(sum(i.subtotal for i in self.items), 2)
