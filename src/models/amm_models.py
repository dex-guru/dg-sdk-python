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

    @classmethod
    def from_response(cls, models: List):
        data = [AmmModel.parse_obj(model) for model in models]
        return cls(data=data, total=len(data))
