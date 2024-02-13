
from typing import Any
from .molds.asset import Asset
from .converter import Converter


class AssetConverter(Converter):

    def __init__(self) -> None:
        self.data_type = 'assets'

    def format_from_gmocoin(self, raw_data: Any) -> Asset | None:

        asset_detail = {}
        try:
            for d in raw_data['data']:
                name = d['symbol']
                amount = d['amount']

                asset_detail[name] = amount

        except KeyError:
            return None
        
        return Asset(asset_detail=asset_detail)
    
    def format_from_bitbank(self, raw_data: Any) -> Asset | None:

        asset_detail = {}
        try:
            for d in raw_data['data']['assets']:
                name = d['asset']
                amount = d['onhand_amount']

                asset_detail[name] = amount

        except KeyError:
            return None
        
        return Asset(asset_detail=asset_detail)
    
    def format_from_bybit(self, raw_data: Any) -> Asset | None:
        
        asset_detail = {}
        try:
            for d in raw_data['result']['list'][0]['coin']:
                name = d['coin']
                amount = d['equity']

                asset_detail[name] = amount

        except KeyError:
            return None
        
        return Asset(asset_detail=asset_detail)
    
    @property
    def get_data_type(self) -> str:
        return self.data_type