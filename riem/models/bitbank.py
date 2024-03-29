from .core import (
    Exchange, 
    HTTPRequestConponents, 
    ModelIdentifier,
    RequestContents
)


class Bitbank(Exchange):
    """Model class for bitbank public/private API.

    [References]
    APIドキュメント: https://github.com/bitbankinc/bitbank-api-docs/blob/master/README_JP.md
    有効シンボル: https://github.com/bitbankinc/bitbank-api-docs/blob/master/pairs.md
    手数料体系: https://bitbank.cc/docs/fees/

    """

    exchange_name: str = "bitbank"
    public_endpoint: str = "https://public.bitbank.cc"
    private_endpoint: str = "https://api.bitbank.cc"

    def __init__(self) -> None:
        pass

    @classmethod
    def get_orderbooks(cls, *, symbol: str, **kwargs) -> RequestContents:

        url = f"{cls.public_endpoint}/{symbol}/depth"
        method = "GET"

        return RequestContents(
            http_request_conponents=HTTPRequestConponents(
                url=url,
                method=method,
            ),
            model_identifier=ModelIdentifier(
                exchange_name=cls.exchange_name,
                data_type="orderbooks",
                arguments={"symbol": symbol},
            ),
        )

    @classmethod
    def get_assets(cls, **kwargs) -> RequestContents:

        url = f"{cls.private_endpoint}/v1/user/assets"
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
        cls,
        *,
        pair: str,
        amount: str,
        side: str,
        type: str,
        price: str | None = None,
        post_only: bool | None = None,
        trigger_price: str | None = None,
        **kwargs,
    ) -> RequestContents:
        """method for placing an order.

        Args:
            pair (str): completely required. symbol.
            amount (str): completely required. size or qty.
            side (str): completely required. [buy | sell].
            type (str): completely required. [limit | market | stop | stop_limit].
            price (str): not required.
            post_only (bool): not required. check API docs.
            trigger_price (str): not required. check API docs.

        Returns:
            RequestContents: contains HTTPRequestContents and ExtraInformation.

        TODO:
        [+] dataの追加について、挙動について確認し、より正確にハンドリングする。(status: UNSOLVED)

        """

        url = f"{cls.private_endpoint}/v1/user/spot/order"
        method = "POST"
        data = {
            "pair": pair,
            "amount": amount,
            "side": side,
            "type": type,
        }

        if type == "limit" or type == "stop_limit":
            if price is None:
                raise ValueError("price is required when type is limit or stop_limit.")

            data["price"] = price

        if post_only is not None:
            data["post_only"] = post_only

        if trigger_price is not None:
            data["trigger_price"] = trigger_price

        return RequestContents(
            http_request_conponents=HTTPRequestConponents(
                url=url,
                method=method,
                data=data,
            ),
            model_identifier=ModelIdentifier(
                exchange_name=cls.exchange_name,
                data_type="orders",
                arguments={
                    "pair": pair,
                    "amount": amount,
                    "side": side,
                    "type": type,
                    "price": price,
                    "post_only": post_only,
                    "trigger_price": trigger_price,
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
