from typing import Any

from .converter import Converter
from .molds.ticker import Ticker


class TickerConverter(Converter):

    def __init__(self) -> None:
        self.data_type = "ticker"

    def handle(self, exchange_name: str, raw_data: Any):

        if exchange_name == 'gmocoin':
            return self.format_from_gmocoin(raw_data)
        
        if exchange_name == 'bitbank':
            return self.format_from_bitbank(raw_data)

        if exchange_name == 'bitbank':
            return self.format_from_bybit(raw_data)
        
        if exchange_name == 'gmocoinfx':
            return self.format_from_gmocoinfx(raw_data)
        
        if exchange_name == 'db':
            return self.format_from_db(raw_data)
        
        return None
    
    def format_from_gmocoin(self, raw_data: Any) -> Ticker:
        pass

    def format_from_bitbank(self, raw_data: Any) -> Ticker:
        pass

    def format_from_bybit(self, raw_data: Any) -> Ticker:
        pass
    
    def format_from_gmocoinfx(self, raw_data: Any) -> Ticker:

        ticker_detail = {}
        try:
            for d in raw_data['data']:
                symbol = d['symbol']
                ask = d['ask']
                bid = d['bid']

                ticker_detail[symbol] = {
                    'ask': ask,
                    'bid': bid
                }
        except KeyError:
            return None

        return Ticker(ticker_detail=ticker_detail)
    
    def format_from_db(self, raw_data: Any) -> Ticker:
        pass

    @property
    def get_data_type(self) -> str:
        return self.data_type