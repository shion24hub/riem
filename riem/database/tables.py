
from __future__ import annotations

from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


# Orderbook

class OrderbookTable(Base):

    __tablename__ = 'orderbook'

    id = Column(Integer, primary_key=True)
    exchange_name = Column(String)
    symbol = Column(String)
    asks = relationship('AskTable', backref='orderbook')
    bids = relationship('BidTable', backref='orderbook')
    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        return 'OrderbookTable(exchange_name={}, symbol={}, ask={}, bid={})'.format(
            self.exchange_name, self.symbol, self.asks, self.bids
        )


class AskTable(Base):
    __tablename__ = 'ask'

    id = Column(Integer, primary_key=True)
    ob_id = Column(Integer, ForeignKey('orderbook.id'))
    price = Column(String)
    size = Column(String)

    def __repr__(self) -> str:
        return 'AskTable(price={}, size={})'.format(self.price, self.size)


class BidTable(Base):
    __tablename__ = 'bid'

    id = Column(Integer, primary_key=True)
    ob_id = Column(Integer, ForeignKey('orderbook.id'))
    price = Column(String)
    size = Column(String)

    def __repr__(self) -> str:
        return 'BidTable(price={}, size={})'.format(self.price, self.size)


# Asset

class AssetTable(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    exchange_name = Column(String)
    asset = relationship('AssetDetailTable', backref='asset')
    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        return 'AssetTable(exchange_name={}, asset={})'.format(self.exchange_name, self.asset)


class AssetDetailTable(Base):
    __tablename__ = 'asset_detail'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'))
    name = Column(String)
    amount = Column(String)

    def __repr__(self) -> str:
        return 'AssetDetailTable(name={}, amount={})'.format(self.name, self.amount)


