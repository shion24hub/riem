
"""

orderIDを返す。

"""

from __future__ import annotations

import dataclasses
from typing import Any

from .core import Formatter


@dataclasses.dataclass
class Order:
    order_id: str


class OrderFormatter(Formatter):

    def handle_by_exchange(self, exchange_name: str, raw_data: Any) -> Order | None:

        if exchange_name == 'gmocoin':
            return self.__format_order_from_gmocoin(raw_data)
        elif exchange_name == 'bitbank':
            return self.__format_order_from_bitbank(raw_data)
        elif exchange_name == 'bybit':
            return self.__format_order_from_bybit(raw_data)
        else:
            raise ValueError(f'exchange_name: {exchange_name} is not supported.')
    
    def __format_order_from_gmocoin(self, raw_data) -> Order | None:

        try:
            return Order(
                order_id=raw_data['data']
            )
        except KeyError:
            return None
    
    def __format_order_from_bitbank(self, raw_data) -> Order | None:

        try:
            return Order(
                order_id=raw_data['data']['order_id']
            )
        except KeyError:
            return None
        
    def __format_order_from_bybit(self, raw_data) -> Order | None:
        
        try:
            return Order(
                order_id=raw_data['result']['orderId']
            )
        except KeyError:
            return None