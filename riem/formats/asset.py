from typing import Any

from .converter import Converter
from .molds.asset import Asset


class AssetConverter(Converter):

    def __init__(self) -> None:
        self.data_type = "assets"

    def handle(self, exchange_name: str, raw_data: Any) -> Asset | None:

        if exchange_name == "gmocoin":
            return self.format_from_gmocoin(raw_data)

        if exchange_name == "bitbank":
            return self.format_from_bitbank(raw_data)

        if exchange_name == "bybit":
            return self.format_from_bybit(raw_data)

        if exchange_name == "db":
            return self.format_from_db(raw_data)

        return None

    def format_from_gmocoin(self, raw_data: Any) -> Asset | None:

        asset_detail = {}
        try:
            for d in raw_data["data"]:
                name = d["symbol"]
                amount = d["amount"]

                asset_detail[name] = amount

        except KeyError:
            return None

        return Asset(asset_detail=asset_detail)

    def format_from_bitbank(self, raw_data: Any) -> Asset | None:

        asset_detail = {}
        try:
            for d in raw_data["data"]["assets"]:
                name = d["asset"]
                amount = d["onhand_amount"]

                asset_detail[name] = amount

        except KeyError:
            return None

        return Asset(asset_detail=asset_detail)

    def format_from_bybit(self, raw_data: Any) -> Asset | None:

        asset_detail = {}
        try:
            for d in raw_data["result"]["list"][0]["coin"]:
                name = d["coin"]
                amount = d["equity"]

                asset_detail[name] = amount

        except KeyError:
            return None

        return Asset(asset_detail=asset_detail)

    def format_from_db(self, raw_data: Any) -> Asset | None:

        asset_detail = {}
        try:
            for name, amount in raw_data.items():
                asset_detail[name] = amount

        except KeyError:
            return None

        return Asset(asset_detail=asset_detail)

    @property
    def get_data_type(self) -> str:
        return self.data_type
