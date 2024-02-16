from typing import Any, Callable

from .models.core import ModelIdentifier, RequestContents
from .response import ClientResponse, ClientResponseProxy
from .fmt import Formatter
from .formats.molds.orderbook import Orderbook
from .formats.molds.asset import Asset
from .database.database import Database
from .database.tables import (
    OrderbookTable,
    AskTable,
    BidTable,
    AssetTable,
    AssetDetailTable,
)


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

    create_funcs: dict[str, Callable[[ClientResponse], Any]] = {
        "orderbooks": create_orderbooks,
        "assets": create_assets,
    }

    tables: dict[str, Any] = {
        "orderbooks": OrderbookTable,
        "assets": AssetTable,
    }

    def __init__(self,fmt: Formatter, database: Database) -> None:

        self.fmt = fmt
        self.database = database

    def create(self, resps: ClientResponseProxy):

        records = []
        for r in resps:
            records.append(self.create_funcs[r.model_identifier.data_type](r))

        with self.database.session as session:
            session.add_all(records)
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