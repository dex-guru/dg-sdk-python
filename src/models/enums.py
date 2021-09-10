from enum import Enum, EnumMeta


class ContaineredEnum(EnumMeta):

    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True

    def list(self) -> list:
        return [v.value for k, v in self.__members__.items()]


class AmmChoices(str, Enum, metaclass=ContaineredEnum):
    uniswap_v3 = 'uniswap_v3'
    uniswap = 'uniswap'
    pancakeswap = 'pancakeswap'
    sushiswap = 'sushiswap'
    quickswap = 'quickswap'


class ChainChoices(str, Enum, metaclass=ContaineredEnum):
    eth = 1
    bsc = 56
    polygon = 137


class TransactionChoices(str, Enum, metaclass=ContaineredEnum):
    swap = 'swap'
    burn = 'burn'
    mint = 'mint'


class OrderChoices(str, Enum):
    asc = 'asc'
    desc = 'desc'


class SortChoices(str, Enum):
    id = 'id'
    address = 'address'
    symbol = 'symbol'
    name = 'name'
    description = 'description'
    txns24h = 'txns24h'
    txns24h_change = 'txns24hChange'
    verified = 'verified'
    decimals = 'decimals'
    volume24h = 'volume24h'
    volume24h_usd = 'volume24hUSD'
    volume24h_eth = 'volume24hETH'
    volumechange24h = 'volumeChange24h'
    liquidity_usd = 'liquidityUSD'
    liquidity_eth = 'liquidityETH'
    liquidity_change24h = 'liquidityChange24h'
    price_usd = 'priceUSD'
    price_eth = 'priceETH'
    price_usd_change24h = 'priceUSDChange24h'
    price_eth_change24h = 'priceETHChange24h'
    timestamp = 'timestamp'
    block_number = 'blockNumber'
    amm = 'amm'
    network = 'network'


class CategoriesChoices(str, Enum, metaclass=ContaineredEnum):
    noob = 'noob'
    casual = 'casual'
    medium = 'medium'
    heavy = 'heavy'
    bot = 'bot'


class TokenTradeDirections(str, Enum):
    _in = 'in'
    _out = 'out'
