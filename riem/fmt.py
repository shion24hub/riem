from .response import ClientResponse, ClientResponseProxy
from .formats.converter import Converter


class Formatter:

    def __init__(self, *converters: Converter) -> None:
        
        self.conv_map: dict[str, Converter] = {
            converter.data_type: converter 
            for converter in converters
        }

    def format(self, responses: ClientResponseProxy) -> ClientResponseProxy:
        
        crp = ClientResponseProxy(responses=[], mapping=False)
        for cr in responses:
            
            model_id = cr.model_identifier

            fd = None
            if model_id.data_type in self.conv_map:

                en = model_id.exchange_name
                if cr.acq_source == 'DB':
                    en = 'db'

                fd = self.conv_map[model_id.data_type].handle(
                        exchange_name=en,
                        raw_data=cr.raw_data,
                    )

            crp += ClientResponseProxy(
                responses=[
                    ClientResponse(
                        model_identifier=model_id,
                        acq_source=cr.acq_source,
                        raw_data=cr.raw_data,
                        formatted_data=fd,
                    )
                ],
                mapping=False,
            )
        
        crp.remap_hash_idxs()

        return crp

    