
from __future__ import annotations

import asyncio
import datetime
from typing import Any

import pybotters

from .response import RequestResponse, RequestResponses
from .formats.core import Formatter
from .models.core import (
    HTTPRequestContents,
    ExtraInformation,
    RequestContents,
)


class Agent:
    """ Agent

    [Responsibility]:
    - RequestContents.HTTPRequestContentsの通りに、リクエストを送信する。
    - Formatterが指定されている場合は、レスポンスをFormatterに渡し、フォーマットされたデータを返す。
    - ステータスコードによる、例外処理を行う。

    [note]:
    - Formatterは自分で作れる形にしておきたい。
    - ステータスコード以外での例外処理は行わない。レスポンスの中身を精査するのは、Formatterの責務である。
    
    """
    
    def __init__(self, *, client: pybotters.Client, echo=False) -> None:
        
        self.client = client
        self.echo = echo
        self.formatters: dict[str, Formatter] = {}
    
    def set_formatter(self, data_type: str, formatter: Formatter) -> None:
        self.formatters[data_type] = formatter
    
    async def request(self, *requests: RequestContents) -> RequestResponses:
        """async request

        Async request to exchanges.

        - note: responses are not guaranteed to be in the same order as requests.

        """

        requests = list(requests)

        tasks = []
        url_info_map: dict[str, ExtraInformation] = {}
        
        for request in requests:

            req_contents: HTTPRequestContents = request.http_request_contents
            ext_info: ExtraInformation = request.extra_information

            # url_info_map構成
            url_info_map[req_contents.full_url] = ext_info

            # tasks構成
            if req_contents.method == 'GET':
                tasks.extend(self.__gen_get_feture(req_contents))
            elif req_contents.method == 'POST':
                tasks.extend(self.__gen_post_feture(req_contents))
        
        # request
        responses = await asyncio.gather(*tasks)
        handled_responses = []
        for response in responses:
            if response.status != 200:
                if self.echo:
                    print()
                    print('[Warning]: status code is not 200.')
                    print('    -> datetime: {}'.format(datetime.datetime.now()))
                    print('    -> url: {}'.format(response.url))
                    print('    -> status code: {}'.format(response.status))
                    print()
                continue
            
            handled_responses.append(response)

        rets = []
        for response in handled_responses:

            # restore additional_information
            restored_ext_info: ExtraInformation = url_info_map[str(response.url)]
            raw_data = await response.json()

            rets.append(
                self.__format(
                    data_type=restored_ext_info.data_type,
                    exchange_name=restored_ext_info.exchange_name,
                    arguments=restored_ext_info.arguments,
                    raw_data=raw_data
                )
            )
    
        return RequestResponses(responses=rets)
    
    def __gen_get_feture(self, http_request_contents: HTTPRequestContents) -> list[Any]:
        return [
            asyncio.ensure_future(
                self.client.get(
                    url=http_request_contents.url,
                    headers=http_request_contents.headers,
                    params=http_request_contents.params,
                )
            )
        ]
    
    def __gen_post_feture(self, http_request_contents: HTTPRequestContents) -> list[Any]:
        return [
            asyncio.ensure_future(
                self.client.post(
                    url=http_request_contents.url,
                    headers=http_request_contents.headers,
                    params=http_request_contents.params,
                    data=http_request_contents.data,
                )
            )
        ]
    
    def __format(
            self, 
            data_type: str,
            exchange_name: str,
            arguments: dict[str, Any],
            raw_data: Any,
        ) -> RequestResponse:

        exsit_formatter = False
        if data_type in self.formatters.keys():
            exsit_formatter = True

        formatted = None
        if exsit_formatter:

            # formatできない形だった場合、Noneが返る
            formatted = (
                self.formatters[data_type]
                .handle_by_exchange(
                    exchange_name=exchange_name,
                    raw_data=raw_data,
                )
            )

        if exsit_formatter and formatted is None and self.echo:
            print()
            print('[Warning]: cannot format data.')
            print('    -> datetime: {}'.format(datetime.datetime.now()))
            print('    -> exchange_name: {}'.format(exchange_name))
            print('    -> data_type: {}'.format(data_type))
            print('    -> arguments: {}'.format(arguments))
            print('    -> raw_data: {}'.format(raw_data))
            print()
        
        return RequestResponse(
            exchange_name=exchange_name,
            data_type=data_type,
            arguments=arguments,
            raw_data=raw_data,
            formatted_data=formatted,
        )