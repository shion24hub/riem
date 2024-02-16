from abc import ABCMeta, abstractmethod
from typing import Any


class Converter(metaclass=ABCMeta):

    @abstractmethod
    def handle(self, exchange_name: str, raw_data: Any):
        pass

    @abstractmethod
    def format_from_gmocoin(self, raw_data: Any):
        pass

    @abstractmethod
    def format_from_bitbank(self, raw_data: Any):
        pass

    @abstractmethod
    def format_from_bybit(self, raw_data: Any):
        pass

    @abstractmethod
    def format_from_db(self, raw_data: Any):
        pass

    @property
    @abstractmethod
    def get_data_type(self) -> str:
        pass
