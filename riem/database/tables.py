
from datetime import datetime

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

from .base import Base


class OrderbookTable(Base):

    __tablename__ = 'orderbook'

    id = Column(Integer, primary_key=True)
    exchange_name = Column(String)
    symbol = Column(String)
    book = relationship('BookTable', backref='orderbook')
    dt = Column(DateTime(), default=datetime.now)

    def __repr__(self) -> str:
        return 'Orderbook(exchange_name={}, symbol={})'.format(self.exchange_name, self.symbol)


class BookTable(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    ob_id = Column(Integer, ForeignKey('orderbook.id'))
    isAsk = Column(Boolean)
    price = Column(String)
    size = Column(String)