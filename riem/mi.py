
from .models.core import Exchange, RequestContents


class ModelInterface:

    def __init__(self, *models: Exchange) -> None:
        
        self.models: dict[str, Exchange] = {}
        for model in models:
            self.models[model.exchange_name] = model

    def get_orderbooks(self, exchange_name: str, **kwargs) -> RequestContents:
        return self.models[exchange_name].get_orderbooks(**kwargs)
    
    def get_assets(self, exchange_name: str, **kwargs) -> RequestContents:
        return self.models[exchange_name].get_assets(**kwargs)
    
    def post_order(self, exchange_name: str, **kwargs) -> RequestContents:
        return self.models[exchange_name].post_order(**kwargs)