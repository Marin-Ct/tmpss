import json
from abc import ABC, abstractmethod
from typing import Dict, Optional

from models import Item, Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order, final_price: float) -> None: ...

    @abstractmethod
    def get(self, order_id: int) -> Optional[dict]: ...


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._data: Dict[int, dict] = {}

    def save(self, order: Order, final_price: float) -> None:
        self._data[order.order_id] = _to_dict(order, final_price)

    def get(self, order_id: int) -> Optional[dict]:
        return self._data.get(order_id)


class JsonFileOrderRepository(OrderRepository):
    def __init__(self, path: str):
        self.path = path

    def _load(self) -> Dict[str, dict]:
        try:
            with open(self.path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save(self, order: Order, final_price: float) -> None:
        data = self._load()
        data[str(order.order_id)] = _to_dict(order, final_price)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get(self, order_id: int) -> Optional[dict]:
        return self._load().get(str(order_id))


def _to_dict(order: Order, final_price: float) -> dict:
    return {
        "customer": order.customer,
        "items": [vars(i) for i in order.items],
        "total": order.total,
        "final_price": final_price,
    }
