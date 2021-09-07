from typing import List

from pydantic import BaseModel


class AmmModel(BaseModel):
    amm_id: str
    chain_id: int
    name: str
    description: str
    type: str
    last_pair_index: int
    router_address: List
    factory_address: str


class AmmListModel(BaseModel):
    total: int
    data: List[AmmModel]

    @classmethod
    def from_response(cls, models: List):
        data = [AmmModel.parse_obj(model) for model in models]
        return cls(data=data, total=len(data))
