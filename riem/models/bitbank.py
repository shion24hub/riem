
"""

[TODO] (status: unsolved | solved | done | canceled):
- [+] 情報を一箇所に集めたいので、pathを.coreのPATHSから取得するようにする(unsolved)
- [+] core.Exchangeのメソッドの返り値の型（RequestContents）に対応する。(solved)

"""

from .core import (
    ENDPOINTS,
    PATHS,
    Exchange,
    HTTPRequestContents,
    ExtraInformation,
    RequestContents,
)


class Bitbank(Exchange):
    """Model class for bitbank public/private API.

    [References]
    APIドキュメント: https://github.com/bitbankinc/bitbank-api-docs/blob/master/README_JP.md
    有効シンボル: https://github.com/bitbankinc/bitbank-api-docs/blob/master/pairs.md
    手数料体系: https://bitbank.cc/docs/fees/

    """

    def __init__(self) -> None:
        
        self.exchange_name = 'bitbank'
        self.public_endpoint = ENDPOINTS['bitbank']['public']
        self.private_endpoint = ENDPOINTS['bitbank']['private']

    def get_orderbooks(self, *, symbol: str, **kwargs) -> RequestContents:

        url = f'{self.public_endpoint}/{symbol}/depth'
        method = 'GET'

        return RequestContents(
            http_request_contents=HTTPRequestContents(
                url=url,
                method=method,
            ),
            extra_information=ExtraInformation(
                exchange_name=self.exchange_name,
                data_type='orderbooks',
                arguments={'symbol': symbol},
            )
        )
    
    def get_assets(self, **kwargs) -> RequestContents:
        
        url = f'{self.private_endpoint}/v1/user/assets'
        method = 'GET'

        return RequestContents(
            http_request_contents=HTTPRequestContents(
                url=url,
                method=method,
            ),
            extra_information=ExtraInformation(
                exchange_name=self.exchange_name,
                data_type='assets',
                arguments={},
            )
        )

    def post_order(
            self,
            *,
            pair: str,
            amount: str,
            side: str,
            type: str,
            price: str | None = None,
            post_only: bool | None = None,
            trigger_price: str | None = None,
            **kwargs
        ) -> RequestContents:
        """ method for placing an order.

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

        url = f'{self.private_endpoint}/v1/user/spot/order'
        method = 'POST'
        data = {
            'pair': pair,
            'amount': amount,
            'side': side,
            'type': type,
        }

        if type == 'limit' or type == 'stop_limit':
            if price is None:
                raise ValueError('price is required when type is limit or stop_limit.')
            
            data['price'] = price

        if post_only is not None:
            data['post_only'] = post_only
        
        if trigger_price is not None:
            data['trigger_price'] = trigger_price
        
        return RequestContents(
            http_request_contents=HTTPRequestContents(
                url=url,
                method=method,
                data=data,
            ),
            extra_information=ExtraInformation(
                exchange_name=self.exchange_name,
                data_type='orders',
                arguments={
                    'pair': pair, 
                    'amount': amount, 
                    'side': side, 
                    'type': type,
                    'price': price,
                    'post_only': post_only,
                    'trigger_price': trigger_price,
                },
            )
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