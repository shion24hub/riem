
from __future__ import annotations

import asyncio
import pybotters

from .response import RequestResponse, ResponseProxy
from .models.core import (
    HTTPRequestContents,
    ExtraInformation,
    RequestContents,
)


class Client(pybotters.Client):
    """Client

    pybotters.Clientのラッパークラス。
    pybotters.Clientの各リクエストメソッドに、riem.RequestContentsを渡せるようにする。
    
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def paralell_fetch(
        self, 
        *requests: RequestContents
    ) -> ResponseProxy:
        """ paralell_fetch

        add later.
        
        """

        tasks = []
        for request in requests:
            tasks.append(self.fetch(request))
        
        resps = await asyncio.gather(*tasks)
        
        ans = resps[0]
        for resp in resps[1:]:
            ans += resp
        
        return ResponseProxy(responses=ans)

    async def fetch(
        self, 
        requests: RequestContents
    ) -> ResponseProxy:
        """ fetch

        pybotters.Client.fetchのwrapperメソッド。
        
        """

        https: HTTPRequestContents = requests.http_request_contents
        ext_info: ExtraInformation = requests.extra_information

        resp = await super().fetch(
            url=https.url, 
            method=https.method,
            params=https.params,
            headers=https.headers,
            data=https.data,
        )

        ans = []

        # Fetch data validation
        # https://pybotters.readthedocs.io/ja/stable/advanced.html#fetch-data-validation
        if resp.data:
            ans.append(
                RequestResponse(
                    exchange_name=ext_info.exchange_name,
                    data_type=ext_info.data_type,
                    arguments=ext_info.arguments,
                    raw_data=resp.data,
                )
            )
        
        return ResponseProxy(responses=ans)