
import copy

from .response import ResponseProxy
from .formats.converter import Converter


class Formatter:

    def __init__(self, *converters: Converter) -> None:
        
        self.conv_map: dict[str, Converter] = {
            converter.data_type: converter 
            for converter in converters
        }

    def format(self, responses: ResponseProxy) -> ResponseProxy:
        
        cresps = copy.deepcopy(responses)

        for i, r in enumerate(responses):

            # [TODO]: 保守性にめちゃくちゃな問題がある気がする
            fd = getattr(
                self.conv_map[r.data_type],
                f'format_from_{r.exchange_name}',
            )(r.raw_data)

            cresps[i].formatted_data = fd
        
        return cresps

    