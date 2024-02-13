
from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class Asset:
    
    assets: dict[str, float]