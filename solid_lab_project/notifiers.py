from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def send(self, customer: str, message: str) -> None: ...


class ConsoleNotifier(Notifier):
    def send(self, customer: str, message: str) -> None:
        print(f"[console] to {customer}: {message}")


class EmailNotifier(Notifier):
    """Simulated e-mail sender (no real SMTP, keeps the lab self-contained)."""

    def __init__(self):
        self.outbox = []

    def send(self, customer: str, message: str) -> None:
        self.outbox.append((customer, message))
        print(f"[email] to {customer}: {message}")
