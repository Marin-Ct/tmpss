"""FACADE - one simple entry point hiding the whole ordering subsystem."""
from logger import OrderLogger
from factory import ItalianPizzaStore, AmericanPizzaStore
from decorators import ExtraCheese, Olives, HotSauce
from order import OrderBuilder
from payment import CashPayment, BankAdapter, WalletAdapter, LegacyBankGateway, MobileWalletSDK


class PizzaShopFacade:
    def __init__(self):
        # all the objects the client would normally have to create itself
        self._stores = {"italian": ItalianPizzaStore(), "american": AmericanPizzaStore()}
        self._extras = {"cheese": ExtraCheese, "olives": Olives, "hot sauce": HotSauce}
        self._payments = {"cash": CashPayment(),
                          "card": BankAdapter(LegacyBankGateway()),
                          "wallet": WalletAdapter(MobileWalletSDK())}
        self._log = OrderLogger()

    # the only method the client needs to call
    def order(self, customer, store, pizza, extras=(), pay_by="cash", address=None):
        pizza_obj = self._stores[store].order_pizza(pizza)       # Factory Method (lab 1)
        for e in extras:
            pizza_obj = self._extras[e](pizza_obj)               # Decorator: wrap once per extra
        builder = OrderBuilder().for_customer(customer).add_pizza(pizza_obj).pay_by(pay_by)
        if address:
            builder.deliver_to(address)
        order = builder.build()                                  # Builder (lab 1)
        if not self._payments[pay_by].pay(customer, order.total):  # Adapter: same pay() for all
            raise RuntimeError("Payment failed")
        self._log.log(f"Order for {customer} completed: {order.total:.2f} MDL")  # Singleton (lab 1)
        return order
