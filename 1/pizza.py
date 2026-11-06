"""Product classes used by the Factory Method."""
from abc import ABC, abstractmethod
#objects will b created

class Pizza(ABC):
    name = "Pizza"
    dough = ""
    sauce = ""
    toppings: list = []
    price = 0.0

    def prepare(self) -> str:
        return (f"Preparing {self.name}: {self.dough} dough, "
                f"{self.sauce} sauce, toppings: {', '.join(self.toppings)}")

    def __str__(self) -> str:
        return f"{self.name} ({self.price:.2f} MDL)"


class MargheritaPizza(Pizza):
    name = "Margherita"
    dough, sauce = "thin", "tomato"
    toppings = ["mozzarella", "basil"]
    price = 90.0


class PepperoniPizza(Pizza):
    name = "Pepperoni"
    dough, sauce = "classic", "spicy tomato"
    toppings = ["mozzarella", "pepperoni"]
    price = 120.0


class VeggiePizza(Pizza):
    name = "Veggie"
    dough, sauce = "whole-grain", "pesto"
    toppings = ["peppers", "mushrooms", "olives"]
    price = 105.0


class ChicagoDeepDish(Pizza):
    name = "Chicago Deep Dish"
    dough, sauce = "thick", "chunky tomato"
    toppings = ["cheese", "sausage", "onion"]
    price = 150.0
