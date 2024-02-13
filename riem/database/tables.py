
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


# Orderbook

class OrderbookTable(Base):

    __tablename__ = 'orderbook'

    id = Column(Integer, primary_key=True)
    exchange_name = Column(String)
    symbol = Column(String)
    book = relationship('BookTable', backref='orderbook')
    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        return 'Orderbook(exchange_name={}, symbol={}, book={})'.format(self.exchange_name, self.symbol, self.book)


class BookTable(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    ob_id = Column(Integer, ForeignKey('orderbook.id'))
    isAsk = Column(Boolean)
    price = Column(String)
    size = Column(String)

    def __repr__(self) -> str:
        return 'Book(isAsk={}, price={}, size={})'.format(self.isAsk, self.price, self.size)


# Asset

class AssetTable(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    exchange_name = Column(String)
    asset = relationship('AssetDetailTable', backref='asset')
    created_on = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        return 'Asset(exchange_name={}, asset={})'.format(self.exchange_name, self.asset)


class AssetDetailTable(Base):
    __tablename__ = 'asset_detail'

    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('asset.id'))
    name = Column(String)
    amount = Column(String)

    def __repr__(self) -> str:
        return 'AssetDetail(name={}, amount={})'.format(self.name, self.amount)


