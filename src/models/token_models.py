from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class TokenInventoryModel(BaseModel):
    address: str
    name: str
    symbol: str
    decimals: int


class TokensInventoryListModel(BaseModel):
    total: int
    data: List[TokenInventoryModel]


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

    class SortFields(Enum):
        address = 'address'
        volume_24h = 'volume_24h'
        liquidity = 'liquidity'
        volume_24h_usd = 'volume_24h_usd'
        liquidity_usd = 'liquidity_usd'
        price_usd = 'price_usd'
        volume_24h_delta = 'volume_24h_delta'
        liquidity_24h_delta = 'liquidity_24h_delta'
        price_24h_delta = 'price_24h_delta'
        volume_24h_delta_usd = 'volume_24h_delta_usd'
        liquidity_24h_delta_usd = 'liquidity_24h_delta_usd'
        price_24h_delta_usd = 'price_24h_delta_usd'
        timestamp = 'timestamp'


class TokensFinanceListModel(BaseModel):
    total: int
    data: List[TokenFinanceModel]
    SortFields = TokenFinanceModel.SortFields


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
