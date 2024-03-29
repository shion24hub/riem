from .core import (
    Exchange, 
    HTTPRequestConponents, 
    ModelIdentifier,
    RequestContents
)


class Gmocoin(Exchange):
    """Model class for gmocoin public/private API.

    [References]
    APIドキュメント: https://api.coin.z.com/docs/
    有効シンボル: https://api.coin.z.com/docs/#parameters-ref
    手数料体系: https://coin.z.com/jp/corp/guide/fees/
    銘柄ごとの手数料: https://coin.z.com/jp/corp/product/info/exchange/
    API制限: https://api.coin.z.com/docs/#restrictions

    """

    exchange_name: str = "gmocoin"
    public_endpoint: str = "https://api.coin.z.com/public"
    private_endpoint: str = "https://api.coin.z.com/private"

    def __init__(self) -> None:
        pass

    @classmethod
    def get_orderbooks(cls, *, symbol: str, **kwargs) -> RequestContents:

        url = f"{cls.public_endpoint}/v1/orderbooks"
        method = "GET"
        params = {"symbol": symbol}

        return RequestContents(
            http_request_conponents=HTTPRequestConponents(
                url=url,
                method=method,
                params=params,
            ),
            model_identifier=ModelIdentifier(
                exchange_name=cls.exchange_name,
                data_type="orderbooks",
                arguments={"symbol": symbol},
            ),
        )

    @classmethod
    def get_assets(cls, **kwargs) -> RequestContents:

        url = f"{cls.private_endpoint}/v1/account/assets"
        method = "GET"

        return RequestContents(
            http_request_conponents=HTTPRequestConponents(
                url=url,
                method=method,
            ),
            model_identifier=ModelIdentifier(
                exchange_name=cls.exchange_name,
                data_type="assets",
                arguments={},
            ),
        )

    @classmethod
    def post_order(
        self,
        *,
        symbol: str,
        side: str,
        size: str,
        execution_type: str,
        price: str | None = None,
        time_in_force: str | None = None,
        losscut_price: str | None = None,
        cancel_before: str | None = None,
        **kwargs,
    ) -> RequestContents:
        """method for placing an order.

        Args:
            symbol (str): completely required.
            side (str):  completely required. [BUY | SELL].
            size (str):  completely required.
            execution_type (str): completely required. [MARKET | LIMIT | STOP].
            price (str): LIMIT | STOP -> required. MARKET -> not required.
            time_in_force (str): not required. check the API doc.
            losscut_price (str): not required. check the API doc.
            cancel_before (str): not required. check the API doc.

        Returns:
            RequestContents: contains HTTPRequestContents and ExtraInformation.

        """

        url = f"{self.private_endpoint}/v1/order"
        method = "POST"
        data = {
            "symbol": symbol,
            "side": side,
            "size": size,
            "executionType": execution_type,
        }

        if execution_type == "LIMIT" or execution_type == "STOP":
            if price is None:
                raise ValueError(
                    "price is required when execution_type is LIMIT or STOP."
                )
            data["price"] = price

        if time_in_force is not None:
            data["timeInForce"] = time_in_force

        if losscut_price is not None:
            data["losscutPrice"] = losscut_price

        if cancel_before is not None:
            data["cancelBefore"] = cancel_before

        return RequestContents(
            http_request_conponents=HTTPRequestConponents(
                url=url,
                method=method,
                data=data,
            ),
            model_identifier=ModelIdentifier(
                exchange_name=self.exchange_name,
                data_type="orders",
                # TODO: Noneを排除するようにする
                arguments={
                    "symbol": symbol,
                    "side": side,
                    "size": size,
                    "execution_type": execution_type,
                    "price": price,
                    "time_in_force": time_in_force,
                    "losscut_price": losscut_price,
                    "cancel_before": cancel_before,
                },
            ),
        )

    @property
    def get_exchange_name(self) -> str:
        return self.exchange_name

    @property
    def get_public_endpoint(self) -> str:
        return self.public_endpoint

    @property
    def get_private_endpoint(self) -> str:
        return self.private_endpoint
