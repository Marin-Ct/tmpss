"""FACTORY METHOD - each store decides which Pizza to instantiate."""
from abc import ABC, abstractmethod
from logger import OrderLogger
from pizza import (Pizza, MargheritaPizza, PepperoniPizza,
                   VeggiePizza, ChicagoDeepDish)


class PizzaStore(ABC):
    """Creator: declares the factory method, uses its product."""

    @abstractmethod
    def create_pizza(self, kind: str) -> Pizza:      # <- factory method
        ...

    def order_pizza(self, kind: str) -> Pizza:
        pizza = self.create_pizza(kind)
        OrderLogger().log(f"{type(self).__name__}: {pizza.prepare()}")
        return pizza
# cp doesn’t know which pizza class it will get. The subclass decides

class ItalianPizzaStore(PizzaStore):
    def create_pizza(self, kind: str) -> Pizza:
        menu = {"margherita": MargheritaPizza,
                "pepperoni": PepperoniPizza,
                "veggie": VeggiePizza}
        if kind not in menu:
            raise ValueError(f"Italian store has no '{kind}'")
        return menu[kind]()


class AmericanPizzaStore(PizzaStore):
    def create_pizza(self, kind: str) -> Pizza:
        menu = {"pepperoni": PepperoniPizza,
                "deepdish": ChicagoDeepDish}
        if kind not in menu:
            raise ValueError(f"American store has no '{kind}'")
        return menu[kind]()
