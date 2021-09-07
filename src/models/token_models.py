from typing import List, Optional
from pydantic import BaseModel, Field


class TokenInventoryModel(BaseModel):
    address: str
    name: str
    symbol: str
    decimals: int


class TokensInventoryListModel(BaseModel):
    total: int
    data: List[TokenInventoryModel]

    # @classmethod
    # def from_response(cls, models: Optional[List] = None, total: int = 0) -> 'TokensInventoryListModel':
    #     models = models or []
    #     data = [TokenInventoryModel(
    #         address=model.address,
    #         name=model.name,
    #         symbol=model.symbol,
    #         decimals=model.decimals
    #     ) for model in models]
    #     return cls(data=data, total=total)


class TokenFinanceModel(BaseModel):
    address: str
    volume_24h: float
    liquidity: float
    volume_24h_usd: float
    liquidity_usd: float
    price_usd: float
    volume_24h_delta: float
    liquidity_24h_delta: float
    price_24h_delta: float
    volume_24h_delta_usd: float
    liquidity_24h_delta_usd: float
    price_24h_delta_usd: float
    timestamp: int

    @classmethod
    def from_domain_model(cls, model) -> 'TokenFinanceModel':
        return cls(
            address=model.address,
            volume_24h=model.volume24h,
            liquidity=model.liquidity,
            volume_24h_usd=model.volume24h_usd,
            liquidity_usd=model.liquidity_usd,
            price_usd=model.price_usd,
            volume_24h_delta=model.volume_change24h,
            liquidity_24h_delta=model.liquidity_change24h,
            price_24h_delta=model.price_eth_change24h,
            volume_24h_delta_usd=model.volume_change24h,
            liquidity_24h_delta_usd=model.liquidity_change24h,
            price_24h_delta_usd=model.price_usd_change24h,
            timestamp=model.timestamp
        )


class TokensFinanceListModel(BaseModel):
    total: int
    data: List[TokenFinanceModel]

    @classmethod
    def from_domain_models(cls, models: List, total: int = 0) -> 'TokensFinanceListModel':
        return cls(data=[TokenFinanceModel.from_domain_model(_) for _ in models], total=total)


# TODO remove zeros after new indexation token_history
class TokenHistory(BaseModel):
    address: str
    volume_24h: float = Field(alias='volume24h_eth')
    liquidity: float
    price: float = Field(alias='price_eth')
    volume_24h_delta: float = 0
    liquidity_24h_delta: float = 0
    price_24h_delta: float = 0
    volume_24h_usd: float = Field(alias='volume24h_usd')
    liquidity_usd: float
    price_usd: float
    volume_24h_delta_usd: float = 0
    liquidity_24h_delta_usd: float = 0
    price_24h_delta_usd: float = 0
    timestamp: int


class TokensHistoryListModel(BaseModel):
    total: int
    data: List[TokenHistory]

    @classmethod
    def from_domain_models(cls, models: List[TokenHistory]) -> 'TokensHistoryListModel':
        return cls(data=[TokenHistory.parse_obj(item) for item in models], total=len(models))
