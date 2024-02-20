from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Ticker:

    ticker_detail: dict[str, str] # symbol, ask, bid