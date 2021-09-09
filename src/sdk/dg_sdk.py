import asyncio
from typing import List, Optional

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

    async def get_token_transactions(
            self,
            chain_id: int,
            token_address: str,
            amm_id: AmmChoices = None,
            wallet_category: CategoriesChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/transactions/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_swaps(
            self,
            chain_id: int,
            token_address: str,
            amm_id: AmmChoices = None,
            wallet_category: CategoriesChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/transactions/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_burns(
            self,
            chain_id: int,
            token_address: str,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/transactions/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_mints(
            self,
            chain_id: int,
            token_address: str,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/transactions/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_market_history(
            self,
            chain_id: int,
            token_address: str,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.TokensHistoryListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/tokens/{token_address}/market/history/?{query}')
        return models.TokensHistoryListModel.parse_obj(response)

    async def get_wallets_info(
            self,
            chain_id: int,
            wallet_address: List[str]  # todo _addresses
    ) -> models.WalletsListModel:
        wallet_address = ','.join(wallet_address)
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/wallets/?{query}')
        return models.WalletsListModel.parse_obj(response)

    async def get_wallet_info(
            self,
            chain_id: int,
            wallet_address: str
    ) -> models.WalletModel:
        response: dict = await self.client.get(f'/{chain_id}/wallets/{wallet_address}')
        return models.WalletModel.parse_obj(response)

    async def get_wallet_transactions(
            self,
            chain_id: int,
            wallet_address: str,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/wallets/{wallet_address}/transactions/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_wallet_swaps(
            self,
            chain_id: int,
            wallet_address: str,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/wallets/{wallet_address}/transactions/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_wallet_burns(
            self,
            chain_id: int,
            wallet_address: str,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/wallets/{wallet_address}/transactions/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_wallet_mints(
            self,
            chain_id: int,
            wallet_address: str,
            amm_id: AmmChoices = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/wallets/{wallet_address}/transactions/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amms_swaps(
            self,
            # TODO add amms param then add filter in PA
            chain_id: int,
            token_address: Optional[str] = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/amms/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amms_burns(
            self,
            # TODO add amms param then add filter in PA
            chain_id: int,
            token_address: Optional[str] = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/amms/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amms_mints(
            self,
            # TODO add amms param then add filter in PA
            chain_id: int,
            token_address: Optional[str] = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/amms/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amm_swaps(
            self,
            chain_id: int,
            amm_id: AmmChoices,
            token_address: Optional[str] = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/amms/{amm_id}/swaps?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amm_burns(
            self,
            chain_id: int,
            amm_id: AmmChoices,
            token_address: Optional[str] = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/amms/{amm_id}/burns?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amm_mints(
            self,
            chain_id: int,
            amm_id: AmmChoices,
            token_address: Optional[str] = None,
            sort_by: SortChoices = SortChoices.timestamp.value,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self.client.get(f'/{chain_id}/amms/{amm_id}/mints?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_all_amm_inventory(self, chain_id: int) -> models.AmmListModel:
        response: dict = await self.client.get(f'/{chain_id}/amms')
        return models.AmmListModel.parse_obj(response)

    async def get_amm_inventory(self, chain_id: int, amm_id: AmmChoices) -> models.AmmModel:
        response: dict = await self.client.get(f'/{chain_id}/amms/{amm_id}')
        return models.AmmModel.parse_obj(response)


sdk = DexGuru(api_key='-ER8PuY9iBB_x5n-_AYJCtF9aTRDxn2OAJtfhWMCxrU',
              endpoint='https://api-public-stage.prod-euc1.dexguru.net')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    d = loop.run_until_complete(
        sdk.get_wallets_info(1, wallet_address=['0x5452ee47f16ead43a6984f101d2dfc7ec2e714e3',
                                                '0xb7b25f87fb87bb0f4a833499cb8ce58a01184943']))
    print(d)
    print(type(d))
