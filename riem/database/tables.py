from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import DateTime, Integer, String

from .base import Base


# Orderbook


class OrderbookTable(Base):
    __tablename__ = "orderbook"

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime(), default=datetime.now)

    modelhash = Column(String)
    exchange_name = Column(String)
    symbol = Column(String)
    asks = relationship("AskTable", backref="orderbook")
    bids = relationship("BidTable", backref="orderbook")

    def __repr__(self) -> str:
        attrs = "modelhash={}, exchange_name={}, symbol={}, ask={}, bid={}".format(
            self.modelhash, self.exchange_name, self.symbol, self.asks, self.bids
        )

        return "OrderbookTable({})".format(attrs)

    @property
    def for_fmt(self) -> dict[str, Any]:
        return {
            "asks": [(a.price, a.size) for a in self.asks],
            "bids": [(b.price, b.size) for b in self.bids],
        }


class AskTable(Base):
    __tablename__ = "ask"

    id = Column(Integer, primary_key=True)
    ob_id = Column(Integer, ForeignKey("orderbook.id"))
    price = Column(String)
    size = Column(String)

    def __repr__(self) -> str:
        return "AskTable(price={}, size={})".format(self.price, self.size)


class BidTable(Base):
    __tablename__ = "bid"

    id = Column(Integer, primary_key=True)
    ob_id = Column(Integer, ForeignKey("orderbook.id"))
    price = Column(String)
    size = Column(String)

    def __repr__(self) -> str:
        return "BidTable(price={}, size={})".format(self.price, self.size)


# Asset


class AssetTable(Base):
    __tablename__ = "asset"

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime(), default=datetime.now)

    modelhash = Column(String)
    exchange_name = Column(String)
    asset = relationship("AssetDetailTable", backref="asset")

    def __repr__(self) -> str:
        attrs = "modelhash={}, exchange_name={}, asset={}".format(
            self.modelhash, self.exchange_name, self.asset
        )

        return "AssetTable({})".format(attrs)

    @property
    def for_fmt(self) -> dict[str, Any]:

        ret = {}
        for a in self.asset:
            ret[a.name] = a.amount

        return ret


class AssetDetailTable(Base):
    __tablename__ = "asset_detail"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    name = Column(String)
    amount = Column(String)

    def __repr__(self) -> str:
        return "AssetDetailTable(name={}, amount={})".format(self.name, self.amount)


# Order


class OrderTable(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime(), default=datetime.now)

    modelhash = Column(String)
    exchange_name = Column(String)
    order_id = Column(String)

    def __repr__(self) -> str:
        attrs = "modelhash={}, exchange_name={}, order_id={}".format(
            self.modelhash, self.exchange_name, self.order_id
        )

        return "OrderTable({})".format(attrs)
    
    @property
    def for_fmt(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id
        }
