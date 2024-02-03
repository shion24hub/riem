
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
    
    def rename(self, name_map: dict[str, str]) -> AssetResponse:
        
        renamed_assets = []
        for asset in self.assets:
            if asset.name in name_map:
                renamed_assets.append(Asset(name=name_map[asset.name], amount=asset.amount))
            else:
                renamed_assets.append(asset)
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
        self.name_map = name_map

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
                assets.append(Asset(name=d['symbol'], amount=d['amount']))
        except KeyError:
            return None
            
        return AssetResponse(assets=assets)
    
    def __format_asset_from_bitbank(self, raw_data: Any) -> AssetResponse | None:

        assets = []
        try:
            for d in raw_data['data']['assets']:
                assets.append(Asset(name=d['asset'], amount=d['onhand_amount']))
        except KeyError:
            return None
        
        return AssetResponse(assets=assets)
    
    def __format_asset_from_bybit(self, raw_data: Any) -> AssetResponse | None:
        
        assets = []
        try:
            for d in raw_data['result']['list'][0]['coin']:
                assets.append(Asset(name=d['coin'], amount=d['equity']))
        except KeyError:
            return None
            
        return AssetResponse(assets=assets)

    