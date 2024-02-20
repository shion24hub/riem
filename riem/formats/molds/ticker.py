from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Ticker:

    ticker_detail: dict[str, str]  # symbol, ask, bid

    def __getitem__(self, key: str) -> dict[str, str]:
        return self.ticker_detail[key]
