import pytest

from src.models import enums
from src.sdk.dg_sdk import DexGuru
from src import models


@pytest.fixture()
def sdk():
    yield DexGuru(api_key='23gttG8WmsS5EYrzNu3ayfRvqAT_JQMwmI3e8SNuCrg',
                  endpoint='https://api-public-stage.prod-euc1.dexguru.net')


@pytest.mark.asyncio
async def test_get_chains(sdk):
    chains = await sdk.get_chains()
    assert isinstance(chains, models.ChainsListModel)


@pytest.mark.asyncio
async def test_get_chain(sdk):
    chains = await sdk.get_chain(chain_id=1)
    assert isinstance(chains, models.ChainModel)
    assert chains.chain_id == 1


@pytest.mark.asyncio
async def test_get_transactions(sdk):
    txs = await sdk.get_transactions(chain_id=1, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_transactions(chain_id=1, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_transactions(chain_id=1, wallet_category=enums.CategoriesChoices.heavy.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.wallet_category == enums.CategoriesChoices.heavy.value


@pytest.mark.asyncio
async def test_get_txs_swaps(sdk):
    txs = await sdk.get_txs_swaps(chain_id=1, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_swaps(chain_id=1, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    # TODO Uncomment merge categories filter fix
    # txs = await sdk.get_txs_swaps(chain_id=1, wallet_category=enums.CategoriesChoices.heavy.value)
    # assert isinstance(txs, models.SwapsBurnsMintsListModel)
    # assert len(txs.data) == 10
    # for item in txs.data:
    #     assert item.wallet_category == enums.CategoriesChoices.heavy.value
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.burn.value


@pytest.mark.asyncio
async def test_get_txs_burns(sdk):
    txs = await sdk.get_txs_burns(chain_id=1, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_burns(chain_id=1, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_burns(chain_id=1)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.burn.value


@pytest.mark.asyncio
async def test_get_txs_mints(sdk):
    txs = await sdk.get_txs_mints(chain_id=1, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_mints(chain_id=1, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_mints(chain_id=1)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.mint.value


@pytest.mark.asyncio
async def test_get_tokens_inventory(sdk):
    tokens = await sdk.get_tokens_inventory(1)
    assert isinstance(tokens, models.TokensInventoryListModel)
