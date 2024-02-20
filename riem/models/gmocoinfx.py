
from .core import (
    Exchange,
    HTTPRequestConponents,
    ModelIdentifier,
    RequestContents,
)

    
class Gmocoinfx(Exchange):
    """Model class for gmocoin public/private API.

    [References]
    APIドキュメント: https://api.coin.z.com/docs/
    有効シンボル: https://api.coin.z.com/docs/#parameters-ref
    手数料体系: https://coin.z.com/jp/corp/guide/fees/
    銘柄ごとの手数料: https://coin.z.com/jp/corp/product/info/exchange/
    API制限: https://api.coin.z.com/docs/#restrictions

    """

    exchange_name: str = 'gmocoinfx'
    public_endpoint: str = 'https://forex-api.coin.z.com/public'
    private_endpoint: str = 'https://forex-api.coin.z.com/private'
    
    def __init__(self) -> None:
        pass

    @classmethod
    def get_ticker(cls):
        
        url = f'{cls.public_endpoint}/v1/ticker'
        method = 'GET'

        return RequestContents(
            http_request_conponents=HTTPRequestConponents(
                url=url,
                method=method,
            ),
            model_identifier=ModelIdentifier(
                exchange_name=cls.exchange_name,
                data_type='ticker',
                arguments={},
            ),
        )
    
    @classmethod
    def get_orderbooks(cls, *, symbol: str, **kwargs) -> RequestContents:
        pass
    
    @classmethod
    def get_assets(self) -> RequestContents:
        pass

    @classmethod
    def post_order(self) -> RequestContents:
        pass

    @property
    def get_exchange_name(self) -> str:
        return self.exchange_name
    
    @property
    def get_public_endpoint(self) -> str:
        return self.public_endpoint

    @property
    def get_private_endpoint(self) -> str:
        return self.private_endpoint