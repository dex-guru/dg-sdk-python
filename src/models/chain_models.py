from typing import List

from pydantic import BaseModel


class ChainModel(BaseModel):
    chain_id: int
    name: str
    description: str
    last_block_number: int


class ChainsListModel(BaseModel):
    total: int
    data: List[ChainModel]
