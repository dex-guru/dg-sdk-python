import pytest

from src.models import enums
from src.sdk.dg_sdk import DexGuru
from src import models


@pytest.fixture()
def sdk():
    yield DexGuru(api_key='23gttG8WmsS5EYrzNu3ayfRvqAT_JQMwmI3e8SNuCrg',
                  endpoint='https://api-public-stage.prod-euc1.dexguru.net')


@pytest.fixture()
def eth_address():
    return '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'


@pytest.fixture()
def btc_address():
    return '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'


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
    txs = await sdk.get_txs_swaps(chain_id=1, wallet_category=enums.CategoriesChoices.heavy.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.wallet_category == enums.CategoriesChoices.heavy.value
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.swap.value


@pytest.mark.asyncio
async def test_get_txs_burns(sdk):
    txs = await sdk.get_txs_burns(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_burns(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_burns(chain_id=enums.ChainChoices.bsc.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.burn.value


@pytest.mark.asyncio
async def test_get_txs_mints(sdk):
    txs = await sdk.get_txs_mints(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_mints(chain_id=enums.ChainChoices.eth.value, amm_id=enums.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm_id == enums.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_mints(
        chain_id=enums.ChainChoices.polygon.value,
        amm_id=enums.AmmChoices.quickswap.value,
        sort_by=enums.SortChoices.timestamp.value,
        limit=1,
        offset=2,
        begin_timestamp=1630934916,
        end_timestamp=1631021316,
    )
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 1
    for item in txs.data:
        assert item.transaction_type == enums.TransactionChoices.mint.value


@pytest.mark.asyncio
async def test_get_tokens_inventory(sdk):
    tokens = await sdk.get_tokens_inventory(1, name='eth')
    assert isinstance(tokens, models.TokensInventoryListModel)
    for token in tokens.data:
        assert isinstance(token, models.TokenInventoryModel)
    with pytest.raises(Exception, match='Specify name'):
        await sdk.get_tokens_inventory(1)


@pytest.mark.asyncio
async def test_get_tokens_finance(sdk, btc_address, eth_address):
    tokens = await sdk.get_tokens_finance(1, limit=5)
    assert isinstance(tokens, models.TokensFinanceListModel)
    assert len(tokens.data) == 5
    for token in tokens.data:
        assert isinstance(token, models.TokenFinanceModel)
    token_addresses = [btc_address, eth_address]
    tokens = await sdk.get_tokens_finance(1, token_addresses=token_addresses, limit=10)
    assert len(tokens.data) == 2
    for token in tokens.data:
        assert token.address in token_addresses


@pytest.mark.asyncio
async def test_get_token_inventory(sdk, eth_address):
    token = await sdk.get_token_inventory(1, eth_address)
    assert isinstance(token, models.TokenInventoryModel)
    assert token.address == eth_address
    with pytest.raises(Exception, match='Token not found'):
        await sdk.get_token_inventory(1, 'invalid')


@pytest.mark.asyncio
async def test_get_token_finance(sdk, eth_address):
    token = await sdk.get_token_finance(1, eth_address)
    assert isinstance(token, models.TokenFinanceModel)
    assert token.address == eth_address
    with pytest.raises(Exception, match='Not found token finance'):
        await sdk.get_token_finance(1, 'invalid')


@pytest.mark.asyncio
async def test_get_token_transactions(sdk, eth_address):
    wallet_category = enums.CategoriesChoices.heavy.value
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_transactions(1, token_address=eth_address,
                                           wallet_category=wallet_category,
                                           limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm_id == amm


@pytest.mark.asyncio
async def test_get_token_swaps(sdk, eth_address):
    wallet_category = enums.CategoriesChoices.heavy.value
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_swaps(1, token_address=eth_address,
                                    wallet_category=wallet_category,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.swap


@pytest.mark.asyncio
async def test_get_token_swaps(sdk, eth_address):
    wallet_category = enums.CategoriesChoices.heavy.value
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_swaps(1, token_address=eth_address,
                                    wallet_category=wallet_category,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.swap


@pytest.mark.asyncio
async def test_get_token_burns(sdk, eth_address):
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_burns(1, token_address=eth_address,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.burn


@pytest.mark.asyncio
async def test_get_token_mints(sdk, eth_address):
    amm = enums.AmmChoices.sushiswap.value
    txs = await sdk.get_token_mints(1, token_address=eth_address,
                                    limit=5, amm_id=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.amm_id == amm
        assert tx.transaction_type == enums.TransactionChoices.mint