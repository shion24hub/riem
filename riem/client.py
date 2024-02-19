from __future__ import annotations

import asyncio

import pybotters

from .fmt import Formatter
from .models.core import HTTPRequestConponents, ModelIdentifier, RequestContents
from .response import ClientResponse, ClientResponseProxy


class Client(pybotters.Client):
    """HTTPClient

    Client for HTTP requests (HTTPクライアント).
    Wrapper for pybotters.Client().

    Attributes:
        fmt (Formatter): Formatter.
    """

    def __init__(self, fmt: Formatter, **kwargs):
        super().__init__(**kwargs)

        self.fmt = fmt

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(self, *args: asyncio.Any) -> None:
        return await super().__aexit__(*args)

    async def _fetch(
        self, 
        rcs: RequestContents
    ) -> ClientResponse | None:

        https: HTTPRequestConponents = rcs.http_request_conponents
        modelid: ModelIdentifier = rcs.model_identifier

        resp = await super().fetch(
            url=https.url,
            method=https.method,
            params=https.params,
            headers=https.headers,
            data=https.data,
        )

        # Fetch data validation
        # https://pybotters.readthedocs.io/ja/stable/advanced.html#fetch-data-validation
        crs = None
        if resp.data:
            crs = ClientResponse(
                model_identifier=modelid,
                acq_source="HTTP",
                raw_data=resp.data,
            )

        return crs

    async def fetch(self, rc: RequestContents) -> ClientResponseProxy:

        crs = await self._fetch(rc)

        if crs is None:
            return ClientResponseProxy(responses=[])

        crp = ClientResponseProxy(responses=[crs])

        return self.fmt.format(crp)

    async def paralell_fetch(
        self, 
        *rcs: tuple[RequestContents]
    ) -> ClientResponseProxy:

        tasks = []
        for request in rcs:
            tasks.append(self._fetch(request))

        crs = await asyncio.gather(*tasks)
        crs = [r for r in crs if r]

        crp = ClientResponseProxy(responses=crs)

        return self.fmt.format(crp)
