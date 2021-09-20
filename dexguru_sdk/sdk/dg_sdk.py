import urllib.parse
from typing import List, Optional, Union

from pydantic import HttpUrl, conint

from dexguru_sdk import models
from dexguru_sdk.client.aiohttp_client import HTTPClient
from dexguru_sdk.models.choices import *
from dexguru_sdk.utils.get_query import get_query_from_params

START_BLOCK_TIMESTAMP = 1588723228
DEFAULT_DOMAIN = 'https://api.dev.dex.guru'
API_VERSION = 'v1/'


class DexGuru:
    """Main class for getting data.

    For initialization, pass the api key of your project.
    If you have especial domain address, put it into 'domain' arg.

    Read more about methods and args on https://docs.dex.guru/api.

    Args:
        api_key (str): API key of dev.dex.guru project.
        domain (str, optional): Especial API domain address.
    """

    def __init__(self, api_key: str, domain: Optional[HttpUrl] = DEFAULT_DOMAIN):
        domain = urllib.parse.urljoin(domain, API_VERSION)
        self._client = HTTPClient(headers={'api-key': api_key}, domain=domain)
        self._chain_prefix = 'chain'

    async def get_chains(self) -> models.ChainsListModel:
        response: dict = await self._client.get(f'{self._chain_prefix}')
        return models.ChainsListModel.parse_obj(response)

    async def get_chain(self, chain_id: int) -> models.ChainModel:
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}')
        return models.ChainModel.parse_obj(response)

    async def get_transactions(
            self,
            chain_id: int,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/transactions?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_txs_swaps(
            self,
            chain_id: int,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/transactions/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_txs_burns(
            self,
            chain_id: int,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/transactions/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_txs_mints(
            self,
            chain_id: int,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/transactions/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def search_tokens_by_name_or_symbol(
            self,
            chain_id: int,
            name: str = None,
            symbol: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            verified: bool = True,
    ) -> models.TokensInventoryListModel:
        if not name and not symbol:
            raise ValueError('Specify name or symbol for search')
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/?{query}')
        return models.TokensInventoryListModel.parse_obj(response)

    async def get_tokens_finance(
            self,
            chain_id: int,
            token_addresses: List[str] = None,
            verified: bool = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
    ) -> models.TokensFinanceListModel:
        if token_addresses:
            token_addresses = ','.join(token_addresses)
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/market/?{query}')
        return models.TokensFinanceListModel.parse_obj(response)

    async def get_token_inventory(
            self,
            chain_id: int,
            token_address: str,
    ) -> models.TokenInventoryModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/?{query}')
        return models.TokenInventoryModel.parse_obj(response)

    async def get_token_finance(
            self,
            chain_id: int,
            token_address: str,
    ) -> models.TokenFinanceModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/market/?{query}')
        return models.TokenFinanceModel.parse_obj(response)

    async def get_token_transactions(
            self,
            chain_id: int,
            token_address: str,
            amm: AmmChoices = None,
            wallet_category: CategoriesChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/transactions/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_swaps(
            self,
            chain_id: int,
            token_address: str,
            amm: AmmChoices = None,
            wallet_category: CategoriesChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/transactions/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_burns(
            self,
            chain_id: int,
            token_address: str,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/transactions/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_mints(
            self,
            chain_id: int,
            token_address: str,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/transactions/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_token_market_history(
            self,
            chain_id: int,
            token_address: str,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.TokensHistoryListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/tokens/{token_address}/market/history/?{query}')
        return models.TokensHistoryListModel.parse_obj(response)

    async def get_wallets_info(
            self,
            chain_id: int,
            wallet_addresses: List[str]
    ) -> models.WalletsListModel:
        wallet_addresses = ','.join(wallet_addresses)
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/wallets/?{query}')
        return models.WalletsListModel.parse_obj(response)

    async def get_wallet_info(
            self,
            chain_id: int,
            wallet_address: str
    ) -> models.WalletModel:
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/wallets/{wallet_address}')
        return models.WalletModel.parse_obj(response)

    async def get_wallet_transactions(
            self,
            chain_id: int,
            wallet_address: str,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/wallets/{wallet_address}/transactions/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_wallet_swaps(
            self,
            chain_id: int,
            wallet_address: str,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/wallets/{wallet_address}/transactions/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_wallet_burns(
            self,
            chain_id: int,
            wallet_address: str,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/wallets/{wallet_address}/transactions/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_wallet_mints(
            self,
            chain_id: int,
            wallet_address: str,
            amm: AmmChoices = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/wallets/{wallet_address}/transactions/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amms_swaps(
            self,
            chain_id: int,
            amms: List[str] = None,
            token_address: Optional[str] = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        if isinstance(amms, list):
            amms = ','.join(amms)
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/swaps/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amms_burns(
            self,
            chain_id: int,
            amms: Union[List[str], str] = None,
            token_address: Optional[str] = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        if isinstance(amms, list):
            amms = ','.join(amms)
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/burns/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amms_mints(
            self,
            chain_id: int,
            amms: Union[List[str], str] = None,
            token_address: Optional[str] = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        if isinstance(amms, list):
            amms = ','.join(amms)
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/mints/?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amm_swaps(
            self,
            chain_id: int,
            amm: AmmChoices,
            token_address: Optional[str] = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
            wallet_category: CategoriesChoices = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/{amm}/swaps?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amm_burns(
            self,
            chain_id: int,
            amm: AmmChoices,
            token_address: Optional[str] = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/{amm}/burns?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_amm_mints(
            self,
            chain_id: int,
            amm: AmmChoices,
            token_address: Optional[str] = None,
            sort_by: str = None,
            limit: conint(gt=0, le=100) = 10,
            offset: conint(ge=0) = 0,
            begin_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = START_BLOCK_TIMESTAMP,
            end_timestamp: conint(ge=START_BLOCK_TIMESTAMP) = None,
    ) -> models.SwapsBurnsMintsListModel:
        query = get_query_from_params(**locals())
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/{amm}/mints?{query}')
        return models.SwapsBurnsMintsListModel.parse_obj(response)

    async def get_all_amm_inventory(self, chain_id: int) -> models.AmmListModel:
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms')
        return models.AmmListModel.parse_obj(response)

    async def get_amm_inventory(self, chain_id: int, amm: AmmChoices) -> models.AmmModel:
        response: dict = await self._client.get(f'{self._chain_prefix}/{chain_id}/amms/{amm}')
        return models.AmmModel.parse_obj(response)
