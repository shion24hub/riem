from typing import Any

from .converter import Converter
from .molds.order import Order


class OrderConverter(Converter):

    def __init__(self) -> None:
        self.data_type = "orders"

    def handle(self, exchange_name: str, raw_data: Any) -> Order | None:

        if exchange_name == "gmocoin":
            return self.format_from_gmocoin(raw_data)
        
        if exchange_name == "bitbank":
            return self.format_from_bitbank(raw_data)
        
        if exchange_name == "bybit":
            return self.format_from_bybit(raw_data)
        
        if exchange_name == "db":
            return self.format_from_db(raw_data)
        
        return None
    
    def format_from_gmocoin(self, raw_data: Any) -> Order | None:

        try:
            return Order(
                order_id=raw_data['data']
            )
        except KeyError:
            return None
    
    def format_from_bitbank(self, raw_data: Any) -> Order | None:

        try:
            return Order(
                order_id=raw_data['data']['order_id']
            )
        except KeyError:
            return None
    
    def format_from_bybit(self, raw_data: Any) -> Order | None:
            
        try:
            return Order(
                order_id=raw_data['result']['orderId']
            )
        except KeyError:
            return None
        
    def format_from_db(self, raw_data: Any) -> Order | None:
        
        try:
            return Order(
                order_id=raw_data['order_id']
            )
        except KeyError:
            return None
        
    @property
    def get_data_type(self) -> str:
        return self.data_type
    
