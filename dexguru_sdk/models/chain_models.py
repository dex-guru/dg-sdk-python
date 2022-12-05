from typing import List

from pydantic import BaseModel

from dexguru_sdk.models.token_models import TokenInventoryModel


class ChainModel(BaseModel):
    chain_id: int
    name: str
    description: str
    native_token: TokenInventoryModel
    eip1559: bool


class ChainsListModel(BaseModel):
    total: int
    data: List[ChainModel]
