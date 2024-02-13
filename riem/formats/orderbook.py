
from typing import Any

from .molds.orderbook import Orderbook, Book
from .converter import Converter


class OrderbookConverter(Converter):
    
    def __init__(self, length: int) -> None:
        self.data_type = 'orderbooks'
        self.length = length

    def format_from_gmocoin(self, raw_data: Any) -> Orderbook:
        
        try:
            asks = raw_data['data']['asks'][:self.length]
            bids = raw_data['data']['bids'][:self.length]
        except KeyError:
            return None
        
        ask_book, bid_book = [], []
        for i in range(self.length):
            ask_book.append((asks[i]['price'], asks[i]['size']))
            bid_book.append((bids[i]['price'], bids[i]['size']))

        return Orderbook(
            asks=Book(book=ask_book),
            bids=Book(book=bid_book)
        )
    
    def format_from_bitbank(self, raw_data: Any) -> Orderbook:
        
        try:
            asks = raw_data['data']['asks'][:self.length]
            bids = raw_data['data']['bids'][:self.length]
        except KeyError:
            return None
        
        ask_book, bid_book = [], []
        for i in range(self.length):
            ask_book.append((asks[i][0], asks[i][1]))
            bid_book.append((bids[i][0], bids[i][1]))
        
        return Orderbook(
            asks=Book(book=ask_book),
            bids=Book(book=bid_book)
        )
    
    def format_from_bybit(self, raw_data: Any) -> Orderbook:
        
        try:
            asks = raw_data['result']['a'][:self.length]
            bids = raw_data['result']['b'][:self.length]
        except KeyError:
            return None
        
        ask_book, bid_book = [], []
        for i in range(self.length):
            ask_book.append((asks[i][0], asks[i][1]))
            bid_book.append((bids[i][0], bids[i][1]))
        
        return Orderbook(
            asks=Book(book=ask_book),
            bids=Book(book=bid_book)
        )

    @property
    def get_data_type(self) -> str:
        return self.data_type
            