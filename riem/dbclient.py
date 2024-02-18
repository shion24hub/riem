from typing import Any, Callable

from .database.database import Database
from .database.tables import (
    AskTable, 
    AssetDetailTable, 
    AssetTable, 
    BidTable,
    OrderbookTable
)
from .fmt import Formatter
from .formats.molds.asset import Asset
from .formats.molds.orderbook import Orderbook
from .models.core import ModelIdentifier, RequestContents
from .response import ClientResponse, ClientResponseProxy


def create_orderbooks(r: ClientResponse):

    model_id: ModelIdentifier = r.model_identifier
    fd: Orderbook = r.formatted_data

    asks = [AskTable(price=p, size=s) for p, s in fd.asks.book]
    bids = [BidTable(price=p, size=s) for p, s in fd.bids.book]

    return OrderbookTable(
        modelhash=model_id.modelhash,
        exchange_name=model_id.exchange_name,
        symbol=model_id.arguments["symbol"],
        asks=asks,
        bids=bids,
    )


def create_assets(r: ClientResponse):

    model_id: ModelIdentifier = r.model_identifier
    fd: Asset = r.formatted_data

    details = [AssetDetailTable(name=k, amount=v) for k, v in fd.asset_detail.items()]

    return AssetTable(
        modelhash=model_id.modelhash,
        exchange_name=model_id.exchange_name,
        asset=details,
    )


class DatabaseClient:
    """ DatabaseClient

    Client for riem.Database (データベースクライアント). 
    Provides methods for CRUD method to the database.

    Attributes:
        fmt (Formatter): riem.Formatter.
        database (Database): riem.Database.
    
    """

    create_funcs: dict[str, Callable[[ClientResponse], Any]] = {
        "orderbooks": create_orderbooks,
        "assets": create_assets,
    }

    tables: dict[str, Any] = {
        "orderbooks": OrderbookTable,
        "assets": AssetTable,
    }

    def __init__(self, fmt: Formatter, database: Database) -> None:

        self.fmt = fmt
        self.database = database

    def create(self, resps: ClientResponseProxy):

        records = []
        for r in resps:
            records.append(self.create_funcs[r.model_identifier.data_type](r))

        with self.database.session as session:
            session.add_all(records)
            session.commit()

    def create_from_table(self, table_objs: list[Any]):
        
        with self.database.session as session:
            session.add_all(table_objs)
            session.commit()

    def read(
        self,
        *requests: RequestContents,
        is_desc=True,
        limit: int = 1,
    ) -> ClientResponseProxy:

        crp = ClientResponseProxy(responses=[], mapping=False)

        with self.database.session as session:
            for req in requests:

                model_id = req.model_identifier
                data_type = model_id.data_type
                table = self.tables[data_type]

                # struct query
                query = session.query(table)
                query = query.filter(table.modelhash == model_id.modelhash)
                if is_desc:
                    query = query.order_by(self.tables[data_type].id.desc())
                results = query.limit(limit)

                # create response
                for res in results:
                    crp += ClientResponseProxy(
                        responses=[
                            ClientResponse(
                                model_identifier=model_id,
                                acq_source="DB",
                                raw_data=res.for_fmt,
                            )
                        ],
                        mapping=False,
                    )

        crp.remap_hash_idxs()

        crp = self.fmt.format(crp)

        return crp
    
    def read_from_table(
        self, 
        table: Any, 
        desc: bool = True, 
        limit: int = 1
    ) -> list[dict[str, Any]]:

        ans = []

        with self.database.session as session:

            query = session.query(table)
            if desc:
                query = query.order_by(table.id.desc())
            results = query.limit(limit)

            for res in results:                
                ans.append(res)
        
        return ans