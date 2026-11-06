"""DECORATOR - add extras to a pizza at runtime by wrapping it."""
from pizza import Pizza


class PizzaDecorator(Pizza):
    """Base decorator: it IS a Pizza and it HAS a Pizza (the wrapped one)."""

    def __init__(self, pizza: Pizza):
        self._pizza = pizza  # the pizza we wrap

    # by default just pass everything to the wrapped pizza
    @property
    def name(self) -> str:
        return self._pizza.name

    @property
    def price(self) -> float:
        return self._pizza.price

    def prepare(self) -> str:
        return self._pizza.prepare()


class ExtraCheese(PizzaDecorator):
    @property
    def name(self) -> str:
        return super().name + " + Extra Cheese"  # keep old name, add ours

    @property
    def price(self) -> float:
        return super().price + 15.0  # old price + cheese

    def prepare(self) -> str:
        return super().prepare() + " | adding extra cheese"


class Olives(PizzaDecorator):
    @property
    def name(self) -> str:
        return super().name + " + Olives"

    @property
    def price(self) -> float:
        return super().price + 10.0

    def prepare(self) -> str:
        return super().prepare() + " | adding olives"


class HotSauce(PizzaDecorator):
    @property
    def name(self) -> str:
        return super().name + " + Hot Sauce"

    @property
    def price(self) -> float:
        return super().price + 5.0

    def prepare(self) -> str:
        return super().prepare() + " | adding hot sauce"
