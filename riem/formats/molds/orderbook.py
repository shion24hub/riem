
from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Book:
    book: list[tuple[str, str]] # prices, sizes

    def __post_init__(self) -> None:
        self.best_price = self.book[0][0]
        self.price_map = {p: s for p, s in self.book}
        self.size_map = {s: p for p, s in self.book}

    def __len__(self) -> int:
        return len(self.book)
    
    def __getitem__(self, idx: int) -> Book:
        return self.book[idx]
    
    def __iter__(self):
        return iter(self.book)

    def convert_to(self, given_rate: float):

        return Book(
            book=[
                (str(float(p) / given_rate), s)
                for p, s in self.book
            ]
        )

    def calc_absdiff(self, before: Book):

        p_union: set[str] = set(self.prices) | set(before.prices)

        book = []
        for p in p_union:
            
            s_before = .0
            if p in before.price_map.keys():
                s_before = before.price_map[p]
            
            s_after = .0
            if p in self.price_map.keys():
                s_after = self.price_map[p]

            book.append((p, s_after - s_before))
        
        return Book(book=book)

    def calc_avg_acq_price(self, amount: float) -> float:

        total_amount = 0.0
        total_price = 0.0

        for price, size in self.book:
            price = float(price)
            size = float(size)
            total_amount += size
            total_price += price * size

            if total_amount >= amount:
                break

        return total_price / total_amount
    
    @property
    def prices(self) -> list[str]:
        return [p for p, _ in self.book]
    
    @property
    def float_prices(self) -> list[float]:
        return [float(p) for p, _ in self.book]
    
    @property
    def prices_with_idx(self) -> list[str]:
        return [(i, p) for i, (p, _) in enumerate(self.book)]

    @property
    def sizes(self) -> list[str]:
        return [s for _, s in self.book]
    
    @property
    def float_sizes(self) -> list[float]:
        return [float(s) for _, s in self.book]
    
    @property
    def sizes_with_idx(self) -> list[str]:
        return [(i, s) for i, (_, s) in enumerate(self.book)]


@dataclasses.dataclass
class Orderbook:
    asks: Book
    bids: Book

    def convert_to(self, given_rate: float) -> Orderbook:
        
        return Orderbook(
            asks=self.asks.convert_to(given_rate),
            bids=self.bids.convert_to(given_rate),
        )
    
    def calc_absdiff(self, before: Orderbook) -> Orderbook:
        
        return Orderbook(
            asks=self.asks.calc_absdiff(before.asks),
            bids=self.bids.calc_absdiff(before.bids),
        )
        