"""ADAPTER - make incompatible payment APIs fit one interface."""
from abc import ABC, abstractmethod
from logger import OrderLogger


class PaymentProcessor(ABC):  # Target: the interface our app wants
    @abstractmethod
    def pay(self, customer: str, amount_mdl: float) -> bool:
        ...


class CashPayment(PaymentProcessor):  # already matches, no adapter needed
    def pay(self, customer: str, amount_mdl: float) -> bool:
        OrderLogger().log(f"Cash: {customer} pays {amount_mdl:.2f} MDL")
        return True


# ---- Adaptees: third-party code, we can't change it ------------------
class LegacyBankGateway:
    # works in cents and returns a dict, so it doesn't match pay()
    def make_transaction(self, card_holder: str, cents: int) -> dict:
        return {"status": "OK" if cents > 0 else "DECLINED", "code": 200}


class MobileWalletSDK:
    # wants the amount as text and returns a string
    def transfer(self, account: str, amount_text: str) -> str:
        return "SUCCESS" if float(amount_text) > 0 else "FAILED"


# ---- Adapters: they translate our pay() into their methods -----------
class BankAdapter(PaymentProcessor):
    def __init__(self, gateway: LegacyBankGateway):
        self._gateway = gateway  # the object we adapt

    def pay(self, customer: str, amount_mdl: float) -> bool:
        cents = int(round(amount_mdl * 100))  # MDL -> cents
        result = self._gateway.make_transaction(customer, cents)
        ok = result["status"] == "OK"  # dict -> bool
        OrderLogger().log(f"Bank: {customer} {amount_mdl:.2f} MDL -> {result['status']}")
        return ok


class WalletAdapter(PaymentProcessor):
    def __init__(self, sdk: MobileWalletSDK):
        self._sdk = sdk

    def pay(self, customer: str, amount_mdl: float) -> bool:
        answer = self._sdk.transfer(customer.lower(), f"{amount_mdl:.2f}")  # float -> text
        ok = answer == "SUCCESS"  # text -> bool
        OrderLogger().log(f"Wallet: {customer} {amount_mdl:.2f} MDL -> {answer}")
        return ok
