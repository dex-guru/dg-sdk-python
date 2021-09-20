import pytest

from dexguru_sdk import models
from dexguru_sdk.client.exceptions import RequestException
from dexguru_sdk.models import choices
from dexguru_sdk.sdk.dg_sdk import DexGuru

DEFAULT_DOMAIN = 'https://api.dev.dex.guru'


@pytest.fixture()
def sdk():
    yield DexGuru(api_key='CkGWZAcDE0h5XRqR04DhtvCNofL-dfDB4WvLzKhraho',
                  domain=DEFAULT_DOMAIN)


@pytest.fixture()
def eth_address():
    return '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'


@pytest.fixture()
def btc_address():
    return '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599'


@pytest.fixture()
def eth_wallets():
    return ['0xd68fe83d3834bf35c6e1aa8a9d81c56249a61881', '0x95ff3e600248bba51764913058483e5d743a848e']


@pytest.fixture()
def polygon_wallets():
    return ['0x568315627841754c917ee45a50b26889090e787a', '0x7737d3742ddc67f1443b40cbe6d401d649d3906a']


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
    txs = await sdk.get_transactions(chain_id=1, amm=choices.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_transactions(chain_id=1, amm=choices.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm == choices.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_transactions(chain_id=1, wallet_category=choices.CategoriesChoices.heavy.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.wallet_category == choices.CategoriesChoices.heavy.value


@pytest.mark.asyncio
async def test_get_txs_swaps(sdk):
    txs = await sdk.get_txs_swaps(chain_id=1, amm=choices.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_swaps(chain_id=1, amm=choices.AmmChoices.uniswap.value, limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm == choices.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_swaps(chain_id=1, wallet_category=choices.CategoriesChoices.heavy.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.wallet_category == choices.CategoriesChoices.heavy.value
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == choices.TransactionChoices.swap.value


@pytest.mark.asyncio
async def test_get_txs_burns(sdk):
    txs = await sdk.get_txs_burns(chain_id=choices.ChainChoices.eth.value, amm=choices.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_burns(chain_id=choices.ChainChoices.eth.value, amm=choices.AmmChoices.uniswap.value,
                                  limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm == choices.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_burns(chain_id=choices.ChainChoices.bsc.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 10
    for item in txs.data:
        assert item.transaction_type == choices.TransactionChoices.burn.value


@pytest.mark.asyncio
async def test_get_txs_mints(sdk):
    txs = await sdk.get_txs_mints(chain_id=choices.ChainChoices.eth.value, amm=choices.AmmChoices.quickswap.value)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 0
    txs = await sdk.get_txs_mints(chain_id=choices.ChainChoices.eth.value, amm=choices.AmmChoices.uniswap.value,
                                  limit=2)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 2
    for item in txs.data:
        assert item.amm == choices.AmmChoices.uniswap.value
    assert isinstance(txs.total, int)
    assert txs.total > 0
    txs = await sdk.get_txs_mints(
        chain_id=choices.ChainChoices.polygon.value,
        amm=choices.AmmChoices.quickswap.value,
        sort_by=models.SwapsBurnsMintsListModel.SortFields.timestamp.value,
        limit=1,
        offset=2,
        begin_timestamp=1630934916,
        end_timestamp=1631021316,
    )
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 1
    for item in txs.data:
        assert item.transaction_type == choices.TransactionChoices.mint.value


@pytest.mark.asyncio
async def test_get_tokens_inventory(sdk):
    tokens = await sdk.search_tokens_by_name_or_symbol(1, name='eth')
    assert isinstance(tokens, models.TokensInventoryListModel)
    for token in tokens.data:
        assert isinstance(token, models.TokenInventoryModel)
    with pytest.raises(Exception, match='Specify name'):
        await sdk.search_tokens_by_name_or_symbol(1)


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
    with pytest.raises(RequestException, match='token_address'):
        # at least 40 symbols
        await sdk.get_token_inventory(1, 'invalid')
    with pytest.raises(RequestException, match='Token not found'):
        await sdk.get_token_inventory(1, eth_address + 'x')


@pytest.mark.asyncio
async def test_get_token_finance(sdk, eth_address):
    token = await sdk.get_token_finance(1, eth_address)
    assert isinstance(token, models.TokenFinanceModel)
    assert token.address == eth_address
    with pytest.raises(RequestException, match='token_address'):
        # at least 40 symbols
        await sdk.get_token_inventory(1, 'invalid')
    with pytest.raises(RequestException, match='Token not found'):
        await sdk.get_token_inventory(1, eth_address + 'x')


@pytest.mark.asyncio
async def test_get_token_transactions(sdk, eth_address):
    wallet_category = choices.CategoriesChoices.heavy.value
    amm = choices.AmmChoices.sushiswap.value
    txs = await sdk.get_token_transactions(1, token_address=eth_address,
                                           wallet_category=wallet_category,
                                           limit=5, amm=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm == amm


@pytest.mark.asyncio
async def test_get_token_swaps(sdk, eth_address):
    wallet_category = choices.CategoriesChoices.heavy.value
    amm = choices.AmmChoices.sushiswap.value
    txs = await sdk.get_token_swaps(1, token_address=eth_address,
                                    wallet_category=wallet_category,
                                    limit=5, amm=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.wallet_category == wallet_category
        assert tx.amm == amm
        assert tx.transaction_type == choices.TransactionChoices.swap


@pytest.mark.asyncio
async def test_get_token_burns(sdk, eth_address):
    amm = choices.AmmChoices.sushiswap.value
    txs = await sdk.get_token_burns(1, token_address=eth_address,
                                    limit=5, amm=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.amm == amm
        assert tx.transaction_type == choices.TransactionChoices.burn


@pytest.mark.asyncio
async def test_get_token_mints(sdk, eth_address):
    amm = choices.AmmChoices.sushiswap.value
    txs = await sdk.get_token_mints(1, token_address=eth_address,
                                    limit=5, amm=amm)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert len(txs.data) == 5
    for tx in txs.data:
        assert tx.amm == amm
        assert tx.transaction_type == choices.TransactionChoices.mint


@pytest.mark.asyncio
async def test_get_token_market_history(sdk, eth_address):
    txs = await sdk.get_token_market_history(1, token_address=eth_address)
    assert isinstance(txs, models.TokensHistoryListModel)
    assert txs.total != 0
    for tx in txs.data:
        assert tx.address == eth_address
        assert isinstance(tx, models.TokenHistoryModel)

    with pytest.raises(RequestException, match='Token not found'):
        await sdk.get_token_market_history(1, ('i' * 42))


@pytest.mark.asyncio
async def test_get_wallets_info(sdk, eth_wallets, polygon_wallets):
    info = await sdk.get_wallets_info(1, wallet_addresses=eth_wallets + polygon_wallets)
    assert isinstance(info, models.WalletsListModel)
    assert info.total != 0
    for wallet in info.data:
        assert isinstance(wallet, models.WalletModel)
    assert len(info.data) == 4
    with pytest.raises(RequestException, match='Wallets not found'):
        await sdk.get_wallets_info(1, wallet_addresses=['invalid'])


@pytest.mark.asyncio
async def test_get_wallet_info(sdk, eth_wallets, polygon_wallets):
    wallet = await sdk.get_wallet_info(1, wallet_address=eth_wallets[0])
    assert isinstance(wallet, models.WalletModel)
    wallet = await sdk.get_wallet_info(1, wallet_address=polygon_wallets[0])
    assert wallet.category
    assert wallet.volume_1m_usd is None
    with pytest.raises(RequestException, match='Wallet not found'):
        await sdk.get_wallet_info(1, wallet_address='invalid')


@pytest.mark.asyncio
async def test_get_wallet_transactions(sdk, eth_wallets, polygon_wallets):
    txs = await sdk.get_wallet_transactions(1, wallet_address=eth_wallets[0])
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == eth_wallets[0]
    txs = await sdk.get_wallet_transactions(1, wallet_address='invalid')
    assert txs.total == 0
    assert txs.data == []


@pytest.mark.asyncio
async def test_get_wallet_swaps(sdk, eth_wallets):
    txs = await sdk.get_wallet_swaps(1, wallet_address=eth_wallets[0], limit=7)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert 0 < len(txs.data) == 7
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == eth_wallets[0]
        assert tx.transaction_type == choices.TransactionChoices.swap


@pytest.mark.asyncio
async def test_get_wallet_burns(sdk):
    txs = await sdk.get_wallet_burns(1, wallet_address='0x935d2fd458fdf41b6f7b62471f593797866a3ce6', limit=6)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert 0 < len(txs.data) <= 6
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == '0x935d2fd458fdf41b6f7b62471f593797866a3ce6'
        assert tx.transaction_type == choices.TransactionChoices.burn


@pytest.mark.asyncio
async def test_get_wallet_mints(sdk):
    txs = await sdk.get_wallet_mints(1, wallet_address='0x935d2fd458fdf41b6f7b62471f593797866a3ce6', limit=5)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert 0 < len(txs.data) <= 5
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_address == '0x935d2fd458fdf41b6f7b62471f593797866a3ce6'
        assert tx.transaction_type == choices.TransactionChoices.mint


@pytest.mark.asyncio
async def test_get_amms_swaps(sdk, eth_address):
    amm = choices.AmmChoices.uniswap_v3.value
    wallet_category = choices.CategoriesChoices.noob.value
    txs = await sdk.get_amms_swaps(1, amms=amm, token_address=eth_address, wallet_category=wallet_category, limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_category == wallet_category
        assert tx.transaction_type == choices.TransactionChoices.swap
        assert eth_address == tx.tokens_in[0]['address'] or eth_address == tx.tokens_out[0]['address']
        assert tx.amm == amm


@pytest.mark.asyncio
async def test_get_amms_burns(sdk, eth_address):
    amms = [choices.AmmChoices.uniswap_v3.value, choices.AmmChoices.uniswap.value]
    txs = await sdk.get_amms_burns(1, amms=amms, token_address=eth_address, limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == choices.TransactionChoices.burn
        assert eth_address in [item.get('address') for item in tx.tokens_in + tx.tokens_out]
        assert tx.amm in amms


@pytest.mark.asyncio
async def test_get_amms_mints(sdk, eth_address):
    amm = choices.AmmChoices.uniswap_v3.value
    txs = await sdk.get_amms_mints(1, amms=amm, token_address=eth_address, limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == choices.TransactionChoices.mint
        assert eth_address in [item.get('address') for item in tx.tokens_in + tx.tokens_out]
        assert tx.amm == amm


@pytest.mark.asyncio
async def test_get_amm_swaps(sdk, eth_address):
    amm = choices.AmmChoices.uniswap.value
    chain = choices.ChainChoices.eth.value
    wallet_category = choices.CategoriesChoices.noob.value
    txs = await sdk.get_amm_swaps(chain, amm=amm, token_address=eth_address, wallet_category=wallet_category,
                                  limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.wallet_category == wallet_category
        assert tx.transaction_type == choices.TransactionChoices.swap
        assert eth_address == tx.tokens_in[0]['address'] or eth_address == tx.tokens_out[0]['address']
        assert tx.amm == amm


@pytest.mark.asyncio
async def test_get_amm_burns(sdk):
    amm = choices.AmmChoices.quickswap.value
    chain = choices.ChainChoices.polygon.value
    txs = await sdk.get_amm_burns(chain, amm=amm, limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == choices.TransactionChoices.burn
        assert tx.amm == amm


@pytest.mark.asyncio
async def test_get_amm_mints(sdk):
    amm = choices.AmmChoices.pancakeswap.value
    chain = choices.ChainChoices.bsc.value
    txs = await sdk.get_amm_mints(chain, amm=amm, limit=8)
    assert isinstance(txs, models.SwapsBurnsMintsListModel)
    assert txs.total > 0
    assert len(txs.data) == 8
    for tx in txs.data:
        assert isinstance(tx, models.SwapBurnMintModel)
        assert tx.transaction_type == choices.TransactionChoices.mint
        assert tx.amm == amm


@pytest.mark.asyncio
async def test_get_all_amm_inventory(sdk):
    chain = choices.ChainChoices.eth.value
    amms = await sdk.get_all_amm_inventory(chain)
    assert amms
    assert len(amms.data) > 0
    assert isinstance(amms, models.AmmListModel)
    for amm in amms.data:
        assert isinstance(amm, models.AmmModel)


@pytest.mark.asyncio
async def test_get_amm_inventory(sdk):
    chain = choices.ChainChoices.eth.value
    amm_ = choices.AmmChoices.uniswap_v3.value
    amm = await sdk.get_amm_inventory(chain, amm_)
    assert isinstance(amm, models.AmmModel)
