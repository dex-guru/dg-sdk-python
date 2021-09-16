from typing import List

from pydantic import BaseModel


class AmmModel(BaseModel):
    chain_id: int
    name: str
    description: str
    type: str


class AmmListModel(BaseModel):
    total: int
    data: List[AmmModel]
