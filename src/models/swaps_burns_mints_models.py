from typing import List, Optional

from pydantic import BaseModel, constr

from src.models.enums import TransactionChoices, ChainChoices, TokenTradeDirections


class SwapBurnMintModel(BaseModel):
    amm_id: str
    chain_id: ChainChoices
    direction: Optional[TokenTradeDirections]
    transaction_address: str
    timestamp: int
    block_number: int
    to: str
    sender: str
    amount_usd: float
    tokens_in: List[dict]
    tokens_out: List[dict]
    pair_address: str
    wallet_address: str
    wallet_category: constr(to_lower=True)
    transaction_type: TransactionChoices


class SwapsBurnsMintsListModel(BaseModel):
    total: int
    data: List[SwapBurnMintModel]
