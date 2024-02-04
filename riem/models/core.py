
from abc import ABCMeta, abstractmethod
import dataclasses
from typing import Any


@dataclasses.dataclass
class HTTPRequestContents:
    url: str
    full_url: str = dataclasses.field(init=False)
    method: str
    params: dict = dataclasses.field(default_factory=dict)
    headers: dict = dataclasses.field(default_factory=dict)
    data: dict = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:
        if len(self.params) == 0:
            self.full_url = self.url
        else:
            self.full_url = self.url + '?' + '&'.join([f'{key}={value}' for key, value in self.params.items()])


@dataclasses.dataclass
class ExtraInformation:
    exchange_name: str
    data_type: str
    arguments: dict[str, Any] = dataclasses.field(default_factory=dict) # 実行中の関数内で引数を取得できるなら、それをここに入れたい。


@dataclasses.dataclass
class RequestContents:
    http_request_contents: HTTPRequestContents
    extra_information: ExtraInformation


class Exchange(metaclass=ABCMeta):
    
    @abstractmethod
    def get_orderbooks(self) -> RequestContents:
        pass

    @abstractmethod
    def get_assets(self) -> RequestContents:
        pass

    @abstractmethod
    def post_order(self) -> RequestContents:
        pass
    
    # # Exchangeを継承したクラスは、以下のメンバ変数を持つ必要がある。
    # @property
    # @abstractmethod
    # def get_exchange_name(self) -> str:
    #     pass

    # @property
    # @abstractmethod
    # def get_public_endpoint(self) -> str:
    #     pass

    # @property
    # @abstractmethod
    # def get_private_endpoint(self) -> str:
    #     pass