from typing import List

from pydantic import BaseModel


class ChainModel(BaseModel):
    chain_id: int
    name: str
    description: str


class ChainsListModel(BaseModel):
    total: int
    data: List[ChainModel]
