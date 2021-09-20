from typing import List

from pydantic import BaseModel

from dexguru_sdk.models.choices import CategoriesChoices


class WalletModel(BaseModel):
    wallet_address: str
    volume_1m_usd: float = None
    txns_1m: int = None
    category: CategoriesChoices
    timestamp: int = None


class WalletsListModel(BaseModel):
    total: int
    data: List[WalletModel]
