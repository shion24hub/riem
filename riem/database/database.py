from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .base import Base


class BaseEngine:
    def __init__(self, url) -> None:

        self.engine = create_engine(url)


class BaseSession(BaseEngine):
    def __init__(self, url) -> None:
        super().__init__(url)

        session = sessionmaker(bind=self.engine)
        self.session = session()


class Database:    
    def __init__(self, url: str) -> None:
        
        self.engine = BaseEngine(url).engine
        Base.metadata.create_all(self.engine)

        self.session = BaseSession(url).session
