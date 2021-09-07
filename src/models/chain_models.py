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

    @classmethod
    def from_response(cls, chains: dict) -> 'ChainsListModel':
        data = [ChainModel.parse_obj(chain) for chain in chains]
        return cls(data=data, total=len(data))
