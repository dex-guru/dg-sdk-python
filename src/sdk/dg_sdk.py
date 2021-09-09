import asyncio
from typing import List

from pydantic import HttpUrl, conint

from src import models
from src.client.aiohttp_client import HTTPClient
from src.models.enums import *
from src.utils.get_query import get_query_from_params

START_BLOCK_TIMESTAMP = 1588723228


class DexGuru:
    def __init__(self, api_key: str, endpoint: HttpUrl):
        self.client = HTTPClient(headers={'api-key': api_key}, url_prefix=endpoint)

    async def get_chains(self) -> models.ChainsListModel:
        response: dict = await self.client.get('/')
        return models.ChainsListModel.parse_obj(response)

    async def get_chain(self, chain_id: int) -> models.ChainModel:
        response: dict = await self.client.get(f'/{chain_id}')
        return models.ChainModel.parse_obj(response)

    async def get_transactions(
            self,
            chain_id: int,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/transactions?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_txs_swaps(
            self,
            chain_id: int,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/transactions/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_txs_burns(
            self,
            chain_id: int,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/transactions/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_txs_mints(
            self,
            chain_id: int,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/transactions/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_tokens_inventory(
            self,
            chain_id: int,
            name: str = None,
            symbol: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            verified: bool = True,
    ) -> models.TokensInventoryListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/?{query}')

        return models.TokensInventoryListModel.parse_obj(response)

    async def get_tokens_finance(
            self,
            chain_id: int,
            token_addresses: List[str] = None,
            verified: bool = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
    ) -> models.TokensFinanceListModel:
        if token_addresses:
            token_addresses = ','.join(token_addresses)
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/market/?{query}')
        return models.TokensFinanceListModel.parse_obj(response)

    async def get_token_inventory(
            self,
            chain_id: int,
            token_address: str,
    ) -> models.TokenInventoryModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/?{query}')
        return models.TokenInventoryModel.parse_obj(response)

    async def get_token_finance(
            self,
            chain_id: int,
            token_address: str,
    ) -> models.TokenFinanceModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/market/?{query}')
        return models.TokenFinanceModel.parse_obj(response)




sdk = DexGuru(api_key='23gttG8WmsS5EYrzNu3ayfRvqAT_JQMwmI3e8SNuCrg',
              endpoint='https://api-public-stage.prod-euc1.dexguru.net')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    d = loop.run_until_complete(sdk.get_tokens_finance(1,    token_addresses = ['0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2']
))
    print(d)
    print(type(d))
