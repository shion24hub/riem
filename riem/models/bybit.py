

from .core import (
    Exchange,
    HTTPRequestContents,
    ExtraInformation,
    RequestContents,
)

    
class Bybit(Exchange):
    """

    [References]
    APIドキュメント(V5): https://bybit-exchange.github.io/docs/v5/intro
    手数料体系: https://www.bybit.com/ja-JP/help-center/article/Trading-Fee-Structure

    """

    exchange_name: str = 'bybit'
    public_endpoint: str = 'https://api.bybit.com'
    private_endpoint: str = 'https://api.bybit.com'

    def __init__(self) -> None:
        pass
    
    def get_orderbooks(self, *, symbol: str, category: str, **kwargs) -> RequestContents:
        """
        returns HTTPRequestContents.
        """
        
        url = f'{self.public_endpoint}/v5/market/orderbook'
        method = 'GET'
        params = {
            'symbol': symbol,
            'category': category,
            'limit': 200 # required
        }

        return RequestContents(
            http_request_contents=HTTPRequestContents(
                url=url,
                method=method,
                params=params,
            ),
            extra_information=ExtraInformation(
                exchange_name=self.exchange_name,
                data_type='orderbooks',
                arguments={'symbol': symbol, 'category': category},
            )
        )
    
    def get_assets(self, *, account_type: str, coin: str | None = None, **kwargs) -> HTTPRequestContents:
        """ get wallet balance

        Args:
            account_type (str): [UNIFIED | CONTRACT | SPOT]
        
        Returns:
            HTTPRequestContents
        
        [TODO]:
        - [+] coinを指定できるようにする

        """
        
        url = f'{self.private_endpoint}/v5/account/wallet-balance'
        method = 'GET'
        params = {
            'accountType': account_type
        }

        return RequestContents(
            http_request_contents=HTTPRequestContents(
                url=url,
                method=method,
                params=params,
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
        category: str,
        symbol: str,
        side: str,
        order_type: str,
        qty: str,
        is_leverage: int | None = None,
        market_unit: str | None = None,
        price: str | None = None,
        trigger_direction: str | None = None,
        order_filter: str | None = None,
        trigger_price: str | None = None,
        trigger_by: str | None = None,
        order_iv: str | None = None,
        time_in_force: str | None = None,
        position_idx: str | None = None,
        order_link_id: str | None = None,
        take_profit: str | None = None,
        stop_loss: str | None = None,
        tp_trigger_by: str | None = None, 
        sl_trigger_by: str | None = None,
        reduce_only: bool | None = None,
        close_on_trigger: bool | None = None, 
        smp_type: str | None = None,
        mmp: bool | None = None,
        tpsl_mode: str | None = None,
        tp_limit_price: str | None = None,
        sl_limit_price: str | None = None,
        tp_order_type: str | None = None,
        sl_order_type: str | None = None,
        **kwargs
    ) -> HTTPRequestContents:
        """ post order

        Args:
            category (str): completely required.\n
            - unified account -> [spot | linear | inverse | option]\n
            - classic account -> [spot | linear | inverse]\n
            symbol (str): completely required.\n
            side (str): completely required. [Buy | Sell]\n
            order_type (str): completely required. [Market | Limit]\n
            qty (str): completely required.\n
            is_leverage (int): \n
            market_unit (str): Defaults to 'quoteCoin' [baseCoin | quoteCoin]\n
            - baseCoin -> e.g. BTCUSDT -> BTC\n
            - quoteCoin -> e.g. BTCUSDT -> USDT\n
            price (str): \n
            trigger_direction (str): \n
            order_filter (str): \n
            trigger_price (str): \n
            trigger_by (str): \n
            order_iv (str): \n
            time_in_force (str): \n
            position_idx (str): \n
            order_link_id (str): \n
            take_profit (str): \n
            stop_loss (str): \n
            tp_trigger_by (str): \n
            sl_trigger_by (str): \n
            reduce_only (bool): \n
            close_on_trigger (bool): \n
            smp_type (str): \n
            mmp (bool): \n
            tpsl_mode (str): \n
            tp_limit_price (str): \n
            sl_limit_price (str): \n
            tp_order_type (str): \n
            sl_order_type (str): \n
        
        Returns:
            HTTPRequestContents

        """

        url = f'{self.private_endpoint}/v5/order/create'
        method = 'POST'
        data = {
            'category': category,
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'qty': qty,
        }

        if is_leverage is not None:
            data['is_leverage'] = is_leverage
        
        if market_unit is not None:
            data['market_unit'] = market_unit
        else:
            print('[WARN] market_unit is not specified. Default value is used.')
        
        if price is not None:
            data['price'] = price
        
        if trigger_direction is not None:
            data['trigger_direction'] = trigger_direction
        
        if order_filter is not None:
            data['order_filter'] = order_filter
        
        if trigger_price is not None:
            data['trigger_price'] = trigger_price
        
        if trigger_by is not None:
            data['trigger_by'] = trigger_by
        
        if order_iv is not None:
            data['order_iv'] = order_iv

        if time_in_force is not None:
            data['time_in_force'] = time_in_force
        
        if position_idx is not None:
            data['position_idx'] = position_idx
        
        if order_link_id is not None:
            data['order_link_id'] = order_link_id
        
        if take_profit is not None:
            data['take_profit'] = take_profit
        
        if stop_loss is not None:
            data['stop_loss'] = stop_loss
        
        if tp_trigger_by is not None:
            data['tp_trigger_by'] = tp_trigger_by
        
        if sl_trigger_by is not None:
            data['sl_trigger_by'] = sl_trigger_by
        
        if reduce_only is not None:
            data['reduce_only'] = reduce_only

        if close_on_trigger is not None:
            data['close_on_trigger'] = close_on_trigger
        
        if smp_type is not None:
            data['smp_type'] = smp_type
        
        if mmp is not None:
            data['mmp'] = mmp

        if tpsl_mode is not None:
            data['tpsl_mode'] = tpsl_mode
        
        if tp_limit_price is not None:
            data['tp_limit_price'] = tp_limit_price
        
        if sl_limit_price is not None:
            data['sl_limit_price'] = sl_limit_price
        
        if tp_order_type is not None:
            data['tp_order_type'] = tp_order_type
        
        if sl_order_type is not None:
            data['sl_order_type'] = sl_order_type

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
                    'category': category,
                    'symbol': symbol,
                    'side': side,
                    'order_type': order_type,
                    'qty': qty,
                    'is_leverage': is_leverage,
                    'market_unit': market_unit,
                    'price': price,
                    'trigger_direction': trigger_direction,
                    'order_filter': order_filter,
                    'trigger_price': trigger_price,
                    'trigger_by': trigger_by,
                    'order_iv': order_iv,
                    'time_in_force': time_in_force,
                    'position_idx': position_idx,
                    'order_link_id': order_link_id,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'tp_trigger_by': tp_trigger_by,
                    'sl_trigger_by': sl_trigger_by,
                    'reduce_only': reduce_only,
                    'close_on_trigger': close_on_trigger,
                    'smp_type': smp_type,
                    'mmp': mmp,
                    'tpsl_mode': tpsl_mode,
                    'tp_limit_price': tp_limit_price,
                    'sl_limit_price': sl_limit_price,
                    'tp_order_type': tp_order_type,
                    'sl_order_type': sl_order_type,
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
        