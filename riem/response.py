
from __future__ import annotations

import dataclasses
from typing import Any, Callable
import copy


@dataclasses.dataclass
class RequestResponse:
    exchange_name: str | None
    data_type: str | None
    arguments: dict[str, Any]
    raw_data: Any
    formatted_data: Any = None


@dataclasses.dataclass
class RequestResponses:

    responses: list[RequestResponse]

    def __len__(self) -> int:
        return len(self.responses)
    
    def __getitem__(self, index: int) -> RequestResponse:
        return self.responses[index]
    
    def __find(
            self,
            *,
            exchange_name: str | list[str] | None = None,
            data_type: str | list[str] | None = None,
            arguments: dict[str, Any] | list[dict[str, Any]] | None = None,
            only_formatted: bool = False,
        ) -> list[tuple[int, RequestResponse]]:
        """ __find

        self.find(), self.arg_find(), self.identify(), self.arg_identify()の内部処理。
        Descriptionは、各メソッドを参照。

        Args:
            exchange_name (str | list[str] | None, optional): Defaults to None.
            data_type (str | list[str] | None, optional): Defaults to None.
            arguments (dict[str, Any] | list[dict[str, Any]] | None, optional): Exact match. Defaults to None.
            only_formatted (bool, optional): Defaults to False.
        
        Returns:
            list[tuple[int, RequestResponse]]: intはself.responsesのindexを表す。
        
        [TODO]:
        - [+] ExtendedRequestResponseのother_informationに対応したいが、
                このメソッドに追加するのは責務を逸脱していると思われる。
                ExtendedRequestResponsesでこのクラスを継承してなんとかしたい。

        """

        if arguments is not None and type(arguments) is not list:
            arguments = [arguments]

        ans = []
        for i, response in enumerate(self.responses):
            if exchange_name is not None and response.exchange_name not in exchange_name:
                continue
            if data_type is not None and response.data_type not in data_type:
                continue

            # argumentsの処理
            if arguments is not None:
                arg_flag = False
                for arg in arguments:
                    if response.arguments == arg:
                        arg_flag = True
                        break
                if arg_flag == False:
                    continue
            
            # only formattedの処理
            if only_formatted and response.formatted_data is None:
                continue
            
            ans.append((i, response))
        
        return ans
    
    def find(
        self, 
        *, 
        exchange_name: str | list[str] | None = None, 
        data_type: str | list[str] | None = None,
        arguments: dict[str, Any] | list[dict[str, Any]] | None = None,
        only_formatted: bool = False,
    ) -> RequestResponses:
        """ find

        検索条件に合致するRequestResponseを探し、それらをRequestResponsesとしてまとめて返す。
        内部処理は__findメソッドを参照。

        [Overall Description]:\n
        各引数のリストの中身は、OR条件で絞り込まれる。
        一方、各引数どうしは、AND条件で絞り込まれる。
        例えば、exchange_name=['bitbank'], data_type=['orderbooks', 'assets']とすると、
        exchange_nameが'bitbank'で、かつ、data_typeが'orderbooks'または'assets'であるような
        RequestResponseが格納されたRequestResponsesが返される。

        [About arguments]:\n
        argumentsは、渡した辞書に完全一致する辞書を持つRequestResponseを探す。
        

        Args:
            exchange_name (str | list[str] | None, optional): Defaults to None.
            data_type (str | list[str] | None, optional): Defaults to None.
            arguments (dict[str, Any] | list[dict[str, Any]] | None, optional): Exact match. Defaults to None.
            only_formatted (bool, optional): Defaults to False.
        
        Returns:
            RequestResponses | None: [description]
        
        [TODO]:
        - [+] 検索結果が0のときにNoneを返すのは、メソッドチェーンに対応できなくさせる。
                確定でRequestResponsesを返すようにしたい。
                影響範囲が非常に大きいので、修正する場合は注意すること。

        """
        
        ans = self.__find(
            exchange_name=exchange_name,
            data_type=data_type,
            arguments=arguments,
            only_formatted=only_formatted,
        )

        return RequestResponses(responses=[response for _, response in ans])
    
    def arg_find(
        self,
        *,
        exchange_name: str | list[str] | None = None,
        data_type: str | list[str] | None = None,
        arguments: dict[str, Any] | list[dict[str, Any]] | None = None,
        only_formatted: bool = False,
    ) -> list[int]:
        """ arg_find

        検索条件に合致するRequestResponseを探し、それらのself.responsesでのindexのリストを返す。
        内部処理は__findメソッドを参照。

        [Overall Description]:\n
        各引数のリストの中身は、OR条件で絞り込まれる。
        一方、各引数どうしは、AND条件で絞り込まれる。
        例えば、exchange_name=['bitbank'], data_type=['orderbooks', 'assets']とすると、
        exchange_nameが'bitbank'で、かつ、data_typeが'orderbooks'または'assets'であるような
        RequestResponseが格納されたRequestResponsesが返される。

        [About arguments]:\n
        argumentsは、渡した辞書に完全一致する辞書を持つRequestResponseを探す。
        

        Args:
            exchange_name (str | list[str] | None, optional): Defaults to None.
            data_type (str | list[str] | None, optional): Defaults to None.
            arguments (dict[str, Any] | list[dict[str, Any]] | None, optional): Exact match. Defaults to None.
            only_formatted (bool, optional): Defaults to False.
        
        Returns:
            list[int] | None: 検索条件に合致するRequestResponseのindex

        """

        ans = self.__find(
            exchange_name=exchange_name,
            data_type=data_type,
            arguments=arguments,
            only_formatted=only_formatted,
        )

        return [index for index, _ in ans]
    
    def identify(
            self,
            *,
            exchange_name: str | list[str] | None = None,
            data_type: str | list[str] | None = None,
            arguments: dict[str, Any] | list[dict[str, Any]] | None = None,
        ) -> RequestResponse | None:
        """identify

        一意に識別できなければ、Noneを返すfind.
        同じ結果は、findの返り値のlen()が1であることを調べることで得られる。
        可読性向上のために呼び出されることを想定している。
        なお、only_formattedがなくても一意に特定できるはずなので、この引数は受け取らない。

        Args:
            exchange_name (str | list[str] | None, optional): Defaults to None.
            data_type (str | list[str] | None, optional): Defaults to None.
            arguments (dict[str, Any] | list[dict[str, Any]] | None, optional): Exact match. Defaults to None.

        Returns:
            RequestResponse | None: [description]
        
        [TODO]:
        - [+] 検索結果が0のときにNoneを返すのは、メソッドチェーンに対応できなくさせる。
                確定でRequestResponsesを返すようにしたい。
                影響範囲が非常に大きいので、修正する場合は注意すること。
        
        """
        
        ans = self.__find(
            exchange_name=exchange_name,
            data_type=data_type,
            arguments=arguments,
        )

        if len(ans) == 1:
            return ans[0][1]
        else:
            return None
        
    def arg_identify(
            self,
            *,
            exchange_name: str | None = None,
            data_type: str | None = None,
            arguments: dict[str, Any] | list[dict[str, Any]] | None = None,
        ) -> int | None:
        """arg_identify

        一意に識別できなければ、Noneを返すarg_find.
        同じ結果は、arg_findの返り値のlen()が1であることを調べることで得られる。
        可読性向上のために呼び出されることを想定している。
        なお、only_formattedがなくても一意に特定できるはずなので、この引数は受け取らない。

        Args:
            exchange_name (str | None, optional): Defaults to None.
            data_type (str | None, optional): Defaults to None.
            arguments (dict[str, Any] | list[dict[str, Any]] | None, optional): Exact match. Defaults to None.
        
        Returns:
            int | None: [description]

        """

        ans = self.__find(
            exchange_name=exchange_name,
            data_type=data_type,
            arguments=arguments,
        )

        if len(ans) == 1:
            return ans[0][0]
        else:
            return None

    def replace(
            self,
            response: RequestResponse
        ) -> RequestResponses:
        """
        add later.
        """

        copied_self: RequestResponses = copy.deepcopy(self)

        index = self.arg_identify(
            exchange_name=response.exchange_name,
            data_type=response.data_type,
            arguments=response.arguments,
        )

        if index is None:
            raise Exception('cannot identify response.')
        
        copied_self.responses[index] = response

        return copied_self
        
    def replace_index():
        pass

    def map_to_responses(
            self, 
            f: Callable[[RequestResponse], RequestResponse],
        ) -> RequestResponses:
        """
        map関数。自身の持っているresponsesに対して、引数に与えられた関数fを適用する。
        関数fは、RequestResponseを引数に取り、RequestResponseを返すように設計しなければならない。

        [note]:
        - 引数を指定することはできない。
        - 引数を指定したい場合は、apply_to_responsesメソッドを使う。
        """

        copied_self: RequestResponses = copy.deepcopy(self)
        
        for response in self.responses:
            res: RequestResponse = f(response)
            copied_self: RequestResponses = copied_self.replace(res)

        return copied_self

    def apply_to_responses(
            self, 
            f: Callable[[RequestResponse, dict[str, Any]], RequestResponse],
            arguments: dict[str, Any],
        ) -> RequestResponses:
        """
        apply関数。自身の持っているresponsesに対して、引数に与えられた関数fを適用する。
        関数fは、RequestResponseとdict[str, Any]を引数に取り、RequestResponseを返すように設計しなければならない。
        関数fの第二引数arguments: dict[str, Any]は、関数fに渡される引数である。
        
        [note]:
        - 引数を指定しないことはできない。
        - 引数を指定しない場合は、map_to_responsesメソッドを使う。
        """

        copied_self: RequestResponses = copy.deepcopy(self)

        for response in self.responses:
            res: RequestResponse = f(response, arguments)
            copied_self: RequestResponses = copied_self.replace(res)
        
        return copied_self
    
    @property
    def exchanges(self) -> list[str]:
        return list(set([response.exchange_name for response in self.responses]))
    
    @property
    def data_types(self) -> list[str]:
        return list(set([response.data_type for response in self.responses]))

    @property
    def arguments_list(self) -> list[dict[str, Any]]:
        return [response.arguments for response in self.responses]
    
    @property
    def raw_data_list(self) -> list[Any]:
        return [response.raw_data for response in self.responses]
    
    @property
    def formatted_data_list(self) -> list[Any]:
        return [response.formatted_data for response in self.responses]