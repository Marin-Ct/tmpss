"""SINGLETON - one shared logger for the whole application."""
import threading
from datetime import datetime


class OrderLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:                 # 1st check (fast path)
            with cls._lock:                       # thread safety
                if cls._instance is None:         # 2nd check
                    cls._instance = super().__new__(cls)
                    cls._instance._messages = []
        return cls._instance

    def log(self, message: str) -> None:
        line = f"[{datetime.now():%H:%M:%S}] {message}"
        self._messages.append(line)
        print(line)

    @property
    def history(self) -> list:
        return list(self._messages)
