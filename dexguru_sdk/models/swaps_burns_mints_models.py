from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, constr

from dexguru_sdk.models.choices import TransactionChoices, ChainChoices, TokenTradeDirections, AmmChoices


class SwapBurnMintModel(BaseModel):
    amm: str
    chain_id: int
    direction: Optional[TokenTradeDirections]
    transaction_address: str
    timestamp: int
    block_number: int
    to: Optional[str] = None
    sender: Optional[str] = None
    amount_usd: float
    tokens_in: List[dict]
    tokens_out: List[dict]
    pair_address: str
    wallet_address: str
    wallet_category: Optional[constr(to_lower=True)] = None
    transaction_type: TransactionChoices

    class SortFields(Enum):
        transaction_address = 'transaction_address'
        timestamp = 'timestamp'
        block_number = 'block_number'
        to = 'to'
        sender = 'sender'
        amount_usd = 'amount_usd'
        pair_address = 'pair_address'
        wallet_address = 'wallet_address'


class SwapsBurnsMintsListModel(BaseModel):
    SortFields = SwapBurnMintModel.SortFields
    total: int
    data: List[SwapBurnMintModel]
