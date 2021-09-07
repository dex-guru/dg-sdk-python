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


class AmmIDChoices(str, Enum, metaclass=ContaineredEnum):
    uniswap_v2 = 1
    uniswap_v3 = 2
    sushiswap = 3
    pancakeswap = 4
    quickswap = 5


class NetworkChoices(str, Enum, metaclass=ContaineredEnum):
    eth = 'eth'
    bsc = 'bsc'
    polygon = 'polygon'


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


class CurrencyChoices(str, Enum, metaclass=ContaineredEnum):
    USD = 'USD'
    ETH = 'ETH'


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


class Periods(str, Enum):
    minute = 'minute'
    hour = 'hour'
    day = 'day'
    week = 'week'
    month = 'month'
    year = 'year'


class NotificatorChoises(str, Enum):
    tg_bot = 'tg'
    webpush = 'wp'


class NativeTokenAddresses(str, Enum):
    eth = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'      # ETH
    polygon = '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270'  # MATIC
    bsc = '0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c'      # BNB

    @classmethod
    def is_native(cls, network: NetworkChoices, address: str):
        return cls[network].lower() == address.lower()


class CategoriesChoices(str, Enum, metaclass=ContaineredEnum):
    noob = 'noob'
    casual = 'casual'
    medium = 'medium'
    heavy = 'heavy'
    bot = 'bot'


class BotActionsChoices(str, Enum, metaclass=ContaineredEnum):
    add = 'add'
    change = 'change'
    remove = 'remove'


class BotDirectionsChoices(str, Enum, metaclass=ContaineredEnum):
    gt = '>'
    lt = '<'


class TokenTradeDirections(str, Enum):
    _in = 'in'
    _out = 'out'
