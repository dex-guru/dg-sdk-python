from typing import List

from pydantic import BaseModel


class RestChainModel(BaseModel):
    chain_id: int
    name: str
    description: str
    last_block_number: int


class RestChainsListModel(BaseModel):
    total: int
    data: List[RestChainModel]

    @classmethod
    def from_response(cls, chains: List[dict]) -> 'RestChainsListModel':
        data = [RestChainModel.parse_obj(chain) for chain in chains]
        return cls(data=data, total=len(data))
