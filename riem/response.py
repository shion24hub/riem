from __future__ import annotations

import dataclasses
import datetime
from typing import Any, Callable, Literal

import xxhash

from .models.core import ModelIdentifier, RequestContents


@dataclasses.dataclass
class ClientResponse:
    """ClientResponse

    Response from the client (クライアントレスポンス).
    Contains the response from the client.

    Attributes:
        model_identifier (ModelIdentifier): Model identifier.
        acq_source (Literal['HTTP', 'DB']): Acquisition source.
        raw_data (Any): Raw data decoded from JSON.
        formatted_data (Any): Formatted data.

        ts (float): Timestamp.
        model_hash (str): Model hash.
            See models.core.ModelIdentifier for more details.

    """

    model_identifier: ModelIdentifier
    acq_source: Literal["HTTP", "DB"]
    raw_data: Any
    formatted_data: Any = None

    modelhash: str = dataclasses.field(init=False)
    ts: float = dataclasses.field(init=False)

    def __post_init__(self) -> None:

        self.modelhash = self.model_identifier.modelhash
        self.ts = datetime.datetime.now().timestamp()


@dataclasses.dataclass
class ClientResponseProxy:
    """ClientResponseProxy

    Proxy for ClientResponse (クライアントレスポンスプロキシ).
    Provides methods for handling ClientResponse.

    Attributes:
        responses (list[ClientResponse]): List of ClientResponse.
        mapping (bool): Whether to use mapping.
            If False, can't use all methods that use hash_idxs_map.
            To re-enable mapping, use remap_hash_idxs().

        hash_idxs_map (dict[str, set[int]]): Hash index map.

    """

    responses: list[ClientResponse]
    mapping: bool = True

    hash_idxs_map: dict[str, set[int]] = dataclasses.field(default_factory=dict)

    def __post_init__(self) -> None:

        if self.mapping:
            self._map_hash_idxs()

    def __len__(self) -> int:
        return len(self.responses)

    def __getitem__(self, index: int):
        return self.responses[index]

    def __iter__(self):
        return iter(self.responses)

    def __next__(self):
        return next(self.responses)

    def __bool__(self):
        return bool(self.responses)

    def __add__(self, other: ClientResponseProxy) -> ClientResponseProxy:
        return ClientResponseProxy(responses=self.responses + other.responses)

    def _map_hash_idxs(self) -> None:

        for i, r in enumerate(self.responses):
            for j in range(0, len(r.modelhash), 16):

                h = r.modelhash[j : j + 16]
                if h not in self.hash_idxs_map.keys():
                    self.hash_idxs_map[h] = set()

                self.hash_idxs_map[h].add(i)

    def remap_hash_idxs(self) -> None:

        self.hash_idxs_map = {}
        self._map_hash_idxs()

    def _find(
        self,
        exchange_names: list[str] | None = None,
        data_types: list[str] | None = None,
        arguments_list: list[dict[str, Any]] | None = None,
    ) -> list[tuple[int, ClientResponse]]:

        enu = set(range(len(self)))
        if exchange_names is not None:
            enu = set()
            for en in exchange_names:
                h = xxhash.xxh64(en).hexdigest()
                enu = enu | self.hash_idxs_map[h]

        dtu = set(range(len(self)))
        if data_types is not None:
            dtu = set()
            for dt in data_types:
                h = xxhash.xxh64(dt).hexdigest()
                dtu = dtu | self.hash_idxs_map[h]

        au = set(range(len(self)))
        if arguments_list is not None:
            au = set()
            for a in arguments_list:
                atext = ModelIdentifier.generate_argstext(a)
                h = xxhash.xxh64(atext).hexdigest()
                au = au | self.hash_idxs_map[h]

        indices = enu & dtu & au

        return [(i, self.responses[i]) for i in indices]

    def find(
        self,
        exchange_names: list[str] | None = None,
        data_types: list[str] | None = None,
        arguments_list: list[dict[str, Any]] | None = None,
    ) -> ClientResponseProxy:

        return ClientResponseProxy(
            responses=[
                r for _, r in self._find(exchange_names, data_types, arguments_list)
            ]
        )

    def arg_find(
        self,
        exchange_names: list[str] | None = None,
        data_types: list[str] | None = None,
        arguments_list: list[dict[str, Any]] | None = None,
    ) -> list[int]:

        return [i for i, _ in self._find(exchange_names, data_types, arguments_list)]

    def mfind(self, *requests: RequestContents) -> ClientResponseProxy:

        return ClientResponseProxy(
            responses=[
                r
                for _, r in self._find(
                    [r.exchange_name for r in requests],
                    [r.data_type for r in requests],
                    [r.arguments for r in requests],
                )
            ]
        )

    def sort_by_ts(self, desc=False) -> ClientResponseProxy:

        return ClientResponseProxy(
            responses=[
                r
                for _, r in sorted(
                    [(i, r) for i, r in enumerate(self.responses)],
                    key=lambda x: x[1].ts,
                    reverse=desc,
                )
            ],
            mapping=False,
        )

    def map_to_responses(
        self, f: Callable[[ClientResponse], ClientResponse]
    ) -> ClientResponseProxy:

        new_resps: list[ClientResponse] = []
        for resp in self:
            new_resps.append(f(resp))

        return ClientResponseProxy(responses=new_resps)

    def apply_to_responses(
        self,
        f: Callable[[ClientResponse, dict[str, Any]], ClientResponse],
        arguments: dict[str, Any],
    ) -> ClientResponseProxy:

        new_resps: list[ClientResponse] = []
        for resp in self:
            new_resps.append(f(resp, arguments))

        return ClientResponseProxy(responses=new_resps)