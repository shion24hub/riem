
from __future__ import annotations

import dataclasses
from typing import Any

from .core import Formatter


@dataclasses.dataclass
class Asset:
    name: str
    amount: str

@dataclasses.dataclass
class AssetResponse:
    
    assets: list[Asset]
    
    def __len__(self) -> int:
        return len(self.assets)

    def __getitem__(self, index: int) -> Asset:
        return self.assets[index]
    
    def get(self, name: str) -> Asset | None:
        for asset in self.assets:
            if asset.name == name:
                return asset
        return None
    
    def calc_total(self, rates: dict[str, float]) -> float:

        total = 0.0
        for asset in self.assets:
            if asset.name in rates:
                total += float(asset.amount) * rates[asset.name]
        return total
    
    def rename(self, asset: str, to: str) -> AssetResponse:

        renamed_assets = []
        for a in self.assets:
            if a.name == asset:
                renamed_assets.append(Asset(name=to, amount=a.amount))
            else:
                renamed_assets.append(a)
        
        return AssetResponse(assets=renamed_assets)
    
    def filter(self, names: list[str]) -> AssetResponse:
        
        filtered_assets = []
        for asset in self.assets:
            if asset.name in names:
                filtered_assets.append(asset)
        return AssetResponse(assets=filtered_assets)
    
    @property
    def names(self) -> list[str]:
        return [asset.name for asset in self.assets]
    

class AssetFormatter(Formatter):

    def __init__(self, name_map: dict[str, list[str]] | None = None) -> None:
        
        self.name_map = {}
        for k, vs in name_map.items():
            for v in vs:
                self.name_map[v] = k
            

    def handle_by_exchange(self, exchange_name: str, raw_data: Any) -> AssetResponse | None:

        if exchange_name == 'gmocoin':
            return self.__format_asset_from_gmocoin(raw_data)
        elif exchange_name == 'bitbank':
            return self.__format_asset_from_bitbank(raw_data)
        elif exchange_name == 'bybit':
            return self.__format_asset_from_bybit(raw_data)
        else:
            raise ValueError(f'Exchange name {exchange_name} is not supported.')
    
    def __format_asset_from_gmocoin(self, raw_data: Any) -> AssetResponse | None:
        
        assets = []
        try:
            for d in raw_data['data']:
                
                name = d['symbol']
                amount = d['amount']
                
                # name_mapに指定があれば変換
                if name in self.name_map:
                    name = self.name_map[name]

                assets.append(Asset(name=name, amount=amount))

        except KeyError:
            return None
            
        return AssetResponse(assets=assets)
    
    def __format_asset_from_bitbank(self, raw_data: Any) -> AssetResponse | None:

        assets = []
        try:
            for d in raw_data['data']['assets']:
                
                name = d['asset']
                amount = d['onhand_amount']

                # name_mapに指定があれば変換
                if name in self.name_map:
                    name = self.name_map[name]
                    
                assets.append(Asset(name=name, amount=amount))

        except KeyError:
            return None
        
        return AssetResponse(assets=assets)
    
    def __format_asset_from_bybit(self, raw_data: Any) -> AssetResponse | None:
        
        assets = []
        try:
            for d in raw_data['result']['list'][0]['coin']:
                
                name = d['coin']
                amount = d['equity']

                # name_mapに指定があれば変換
                if name in self.name_map:
                    name = self.name_map[name]

                assets.append(Asset(name=name, amount=amount))

        except KeyError:
            return None
            
        return AssetResponse(assets=assets)

    