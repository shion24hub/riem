
from abc import ABCMeta, abstractmethod
import dataclasses
from typing import Any, Literal

import xxhash


@dataclasses.dataclass
class HTTPRequestConponents:
    """ HTTPRequestConponents

    Components of HTTP request Massage (HTTPリクエストの構成要素).
    Contains the information to be passed to `aiohttp.Client.request()`.

    Attributes:
        method (str): HTTP method.
        url (str): URL.
        params (dict): URL parameters.
        headers (dict): HTTP headers.
        data (dict): HTTP body.

    """

    method: Literal["GET", "POST", "PUT", "DELETE"]
    url: str
    params: dict = dataclasses.field(default_factory=dict)
    headers: dict = dataclasses.field(default_factory=dict)
    data: dict = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class ModelIdentifier:
    """ ModelIdentifier

    Identifier for the model (モデル識別情報).
    Contains the information to identify the model.

    Attributes:
        exchange_name (str): Exchange name.
        data_type (str): Data type.
        arguments (dict[str, Any]): Arguments for the request.

    """

    exchange_name: str
    data_type: str
    arguments: dict[str, Any] = dataclasses.field(default_factory=dict)

    modelhash: str = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        self.modelhash = self.generate_modelhash()

    def generate_modelhash(self) -> str:
        """ generate_modelhash

        Generate model hash (モデルハッシュを生成).

        Args:
            exchange_name (str): Exchange name.
            data_type (str): Data type.
            arguments (dict[str, Any]): Arguments for the request.
        
        Returns:
            str: Model hash.

        """

        argstext = self.generate_argstext(self.arguments)

        modelhash = ""
        modelhash += xxhash.xxh64(self.exchange_name).hexdigest()
        modelhash += xxhash.xxh64(self.data_type).hexdigest()
        modelhash += xxhash.xxh64(argstext).hexdigest()

        return modelhash
    
    @staticmethod
    def generate_argstext(arguments: dict[str, Any]) -> str:

        args = [(k, str(v)) for k, v in arguments.items()]
        args.sort(key=lambda x: x[0])
        argstext = "".join([k + v for k, v in args])

        return argstext


@dataclasses.dataclass
class RequestContents:
    """RequestContents

    Request contents (リクエスト内容).
    Contains the information to be passed to riem.Client.fetch().

    Attributes:
        http (HTTPRequestConponents): Components of HTTP request.
        identifier (ModelIdentifier): Identifier for the model.

    """

    http_request_conponents: HTTPRequestConponents
    model_identifier: ModelIdentifier


class Exchange(metaclass=ABCMeta):
    """Exchange

    ABC for the exchange (取引所の抽象基底クラス).

    """

    @classmethod
    @abstractmethod
    def get_orderbooks(self) -> RequestContents:
        pass

    @classmethod
    @abstractmethod
    def get_assets(self) -> RequestContents:
        pass

    @classmethod
    @abstractmethod
    def post_order(self) -> RequestContents:
        pass

    @property
    @abstractmethod
    def get_exchange_name(self) -> str:
        pass

    @property
    @abstractmethod
    def get_public_endpoint(self) -> str:
        pass

    @property
    @abstractmethod
    def get_private_endpoint(self) -> str:
        pass
