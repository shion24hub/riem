
from abc import ABCMeta, abstractmethod
from typing import Any

class Formatter(metaclass=ABCMeta):

    @abstractmethod
    def handle_by_exchange(self, exchange_name: str, raw_data: Any) -> Any:
        pass