
from __future__ import annotations

import dataclasses
from typing import Any

from .core import Formatter


@dataclasses.dataclass
class OrderbookRecord:
    price: str
    size: str

    def convert_to_usd(self, given_rate: float) -> OrderbookRecord:
        return OrderbookRecord(
            price=str(float(self.price) / given_rate),
            size=self.size,
        )


@dataclasses.dataclass
class Orderbook:
    book: list[OrderbookRecord]

    def __post_init__(self) -> None:
        self.best_price = self.book[0].price

    def convert_to_usd(self, given_rate: float) -> Orderbook:
        return Orderbook(
            book=[record.convert_to_usd(given_rate) for record in self.book]
        )

    def calc_avg_acq_price(self, amount: float) -> float:
        total_amount = 0.0
        total_price = 0.0

        for record in self.book:
            price = float(record.price)
            size = float(record.size)
            total_amount += size
            total_price += price * size

            if total_amount >= amount:
                break

        return total_price / total_amount

    def find_price_by_heaped_amount(self, amount: float) -> float:
        total_amount = 0.0

        for record in self.book:
            price = record.price
            size = record.size
            total_amount += size

            if total_amount >= amount:
                break

        return price
    
    # 2024/1/27:　以下追加
    def get_size(self, price:float) -> float:
        for record in self.book:
            if float(record.price) == price:
                return float(record.size)
        return 0.0
    
    def calc_absolute_differences(self, before: Orderbook) -> Orderbook:

        existing_prices: set[float] = set(self.prices) | set(before.prices)

        book = []
        for price in existing_prices:
            size_before = before.get_size(price)
            size_after = self.get_size(price)

            diff = size_after - size_before

            book.append(
                OrderbookRecord(
                    price=str(price),
                    size=str(diff),
                )
            )
        
        return Orderbook(book=book)
    
    @property
    def prices(self) -> list[set(float)]:
        return [float(record.price) for record in self.book]

    @property
    def sizes(self) -> list[float]:
        return [float(record.size) for record in self.book]


@dataclasses.dataclass
class OrderbookResponce:
    asks: Orderbook
    bids: Orderbook

    def convert_to_usd(self, given_rate: float) -> OrderbookResponce:

        return OrderbookResponce(
            asks=self.asks.convert_to_usd(given_rate),
            bids=self.bids.convert_to_usd(given_rate),
        )
    

class OrderbookFormatter(Formatter):
    
    def __init__(self, length: int) -> None:
        self.length = length

    def select_formatter(self, exchange_name: str, data: Any) -> OrderbookResponce | None:
        
        if exchange_name == 'gmocoin':
            return self.__format_orderbook_from_gmocoin(data)
        elif exchange_name == 'bitbank':
            return self.__format_orderbook_from_bitbank(data)
        elif exchange_name == 'bybit':
            return self.__format_orderbook_from_bybit(data)
        else:
            None
    
    def handle_by_exchange(
            self, 
            exchange_name: str, 
            raw_data: Any
        ) -> OrderbookResponce | None:
        """handle_by_exchange

        Args:
            exchange_name (str): [description]
            raw_data (Any): [description]
        
        Returns:
            OrderbookResponce | None: [description]
        
        """
        
        if exchange_name == 'gmocoin':
            return self.__format_orderbook_from_gmocoin(raw_data)
        elif exchange_name == 'bitbank':
            return self.__format_orderbook_from_bitbank(raw_data)
        elif exchange_name == 'bybit':
            return self.__format_orderbook_from_bybit(raw_data)
        else:
            raise ValueError(f'exchange_name: {exchange_name} is not supported.')
    
    def __format_orderbook_from_gmocoin(self, res) -> OrderbookResponce | None:

        try:
            asks = res['data']['asks'][:self.length]
            bids = res['data']['bids'][:self.length]
        except KeyError:
            return None
        
        # format asks and bids
        ask_records: list[OrderbookRecord] = [
            OrderbookRecord(asks[i]["price"], asks[i]["size"]) for i in range(len(asks))
        ]
        bid_records: list[OrderbookRecord] = [
            OrderbookRecord(bids[i]["price"], bids[i]["size"]) for i in range(len(bids))
        ]

        return OrderbookResponce(
            asks=Orderbook(ask_records),
            bids=Orderbook(bid_records),
        )
    
    def __format_orderbook_from_bitbank(self, res) -> OrderbookResponce | None:

        try:
            asks = res['data']['asks'][:self.length]
            bids = res['data']['bids'][:self.length]
        except KeyError:
            return None

        # format asks and bids
        ask_records: list[OrderbookRecord] = [
            OrderbookRecord(asks[i][0], asks[i][1]) for i in range(len(asks))
        ]
        bid_records: list[OrderbookRecord] = [
            OrderbookRecord(bids[i][0], bids[i][1]) for i in range(len(bids))
        ]

        return OrderbookResponce(
            asks=Orderbook(ask_records),
            bids=Orderbook(bid_records),
        )

    def __format_orderbook_from_bybit(self, res) -> OrderbookResponce | None:

        try:
            asks = res['result']['a'][:self.length]
            bids = res['result']['b'][:self.length]
        except KeyError:
            return None

        # format asks and bids
        ask_records: list[OrderbookRecord] = [
            OrderbookRecord(asks[i][0], asks[i][1]) for i in range(len(asks))
        ]
        bid_records: list[OrderbookRecord] = [
            OrderbookRecord(bids[i][0], bids[i][1]) for i in range(len(bids))
        ]

        return OrderbookResponce(
            asks=Orderbook(ask_records),
            bids=Orderbook(bid_records),
        )