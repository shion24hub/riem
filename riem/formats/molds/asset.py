from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Asset:

    asset_detail: dict[str, float]
