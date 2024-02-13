
from .models.core import ExtraInformation, RequestContents
from .response import RequestResponse, ResponseProxy
from .formats.molds.orderbook import Orderbook
from .database.database import Database
from .database.tables import OrderbookTable, BookTable


class DatabaseInterface:

    def __init__(self, database: Database) -> None:
        
        self.database = database
    
    def create(self, resps: ResponseProxy): 

        records = []
        for r in resps:
            records.append(getattr(self, f'create_{r.data_type}')(r))
        
        with self.database.session as session:
            session.add_all(records)
            session.commit()

    def create_orderbooks(self, r: RequestResponse):

        fd: Orderbook = r.formatted_data

        asks = [BookTable(isAsk=True, price=p, size=s) for p, s in fd.asks.book]
        bids = [BookTable(isAsk=False, price=p, size=s) for p, s in fd.bids.book]

        return OrderbookTable(
            exchange_name=r.exchange_name,
            symbol=r.arguments['symbol'],
            book=asks + bids
        )
    
    def read(self, *requests: RequestContents, is_desc=True, limit: int = 1) -> ResponseProxy:
        """ read

        未完成。
        
        TODO:
        - raw_dataに何を含めるか、フォーマットした形で渡すかを決める。
        
        """

        mapper = {
            'orderbooks': OrderbookTable
        }
        
        ans = ResponseProxy(responses=[])

        with self.database.session as session:
            for r in requests:
                
                ext_info: ExtraInformation = r.extra_information
                data_type = ext_info.data_type
                exchange_name = ext_info.exchange_name
                symbol = ext_info.arguments['symbol']

                query = session.query(mapper[data_type])
                query = query.filter(mapper[data_type].exchange_name == exchange_name)
                query = query.filter(mapper[data_type].symbol == symbol)

                if is_desc:
                    query = query.order_by(mapper[data_type].id.desc())

                result = query.limit(limit)

                ans += ResponseProxy(
                    responses=[
                        RequestResponse(
                            exchange_name=exchange_name,
                            data_type=data_type,
                            arguments=r.arguments,
                            raw_data=result,
                        )
                    ]
                )
        
        return ans