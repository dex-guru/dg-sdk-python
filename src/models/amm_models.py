from typing import List

from pydantic import BaseModel


class AmmModel(BaseModel):
    amm_id: str
    chain_id: int
    name: str
    description: str
    type: str
    last_pair_index: int
    contracts: dict


class AmmListModel(BaseModel):
    total: int
    data: List[AmmModel]
