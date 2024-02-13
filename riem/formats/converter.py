from typing import Any
from abc import ABCMeta, abstractmethod


class Converter(metaclass=ABCMeta):

    @abstractmethod
    def format_from_gmocoin(self, raw_data: Any):
        pass

    @abstractmethod
    def format_from_bitbank(self, raw_data: Any):
        pass

    @abstractmethod
    def format_from_bybit(self, raw_data: Any):
        pass

    @property
    @abstractmethod
    def get_data_type(self) -> str:
        pass