from factory import ItalianPizzaStore
from decorators import ExtraCheese, Olives
from payment import (CashPayment, BankAdapter, WalletAdapter,
                     LegacyBankGateway, MobileWalletSDK)
from facade import PizzaShopFacade


def main():
    print("=== DECORATOR ===")
    pizza = ItalianPizzaStore().order_pizza("margherita")
    print("Plain   :", pizza)
    decorated = Olives(ExtraCheese(pizza))  # wrapped twice, original pizza is not changed
    print("Decorated:", decorated)          # 90 + 15 + 10 = 115
    print(decorated.prepare())

    print("\n=== ADAPTER ===")
    # the legacy API used directly: cents in, dict out
    raw = LegacyBankGateway().make_transaction("Marin", 24000)
    print("Legacy API directly (cents, returns dict):", raw)
    processors = {"cash": CashPayment(),
                  "bank": BankAdapter(LegacyBankGateway()),
                  "wallet": WalletAdapter(MobileWalletSDK())}
    for name, proc in processors.items():
        # same call for every service, the adapter hides the differences
        print(f"{name:7} -> same call pay(): {proc.pay('Marin', 240.0)}")

    print("\n=== FACADE ===")
    shop = PizzaShopFacade()
    # one call does everything: pizza, extras, order, payment, log
    order1 = shop.order("Marin", "italian", "margherita",
                        extras=["cheese", "olives"], pay_by="card",
                        address="Str. Studenților 9, Chișinău")
    print(order1)
    print()
    order2 = shop.order("Artur", "american", "deepdish", pay_by="wallet")
    print(order2)


if __name__ == "__main__":
    main()
