from __future__ import annotations

from typing import Any
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


# Orderbook


class OrderbookTable(Base):
    __tablename__ = "orderbook"

    id = Column(Integer, primary_key=True)

    modelhash = Column(String)
    exchange_name = Column(String)
    symbol = Column(String)
    asks = relationship("AskTable", backref="orderbook")
    bids = relationship("BidTable", backref="orderbook")

    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        attrs = "modelhash={}, exchange_name={}, symbol={}, ask={}, bid={}".format(
            self.modelhash, self.exchange_name, self.symbol, self.asks, self.bids
        )

        return "OrderbookTable({})".format(attrs)
    
    @property
    def for_fmt(self) -> dict[str, Any]:
        return {
            'asks': [(a.price, a.size) for a in self.asks],
            'bids': [(b.price, b.size) for b in self.bids],
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

    modelhash = Column(String)
    exchange_name = Column(String)
    asset = relationship("AssetDetailTable", backref="asset")

    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        attrs = "modelhash={}, exchange_name={}, asset={}".format(
            self.modelhash, self.exchange_name, self.asset
        )

        return "AssetTable({})".format(attrs)

    @property
    def for_fmt(self) -> dict[str, Any]:
        return {
            'asset_detail': {a.name: a.amount for a in self.asset},
        }


class AssetDetailTable(Base):
    __tablename__ = "asset_detail"

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey("asset.id"))
    name = Column(String)
    amount = Column(String)

    def __repr__(self) -> str:
        return "AssetDetailTable(name={}, amount={})".format(self.name, self.amount)
