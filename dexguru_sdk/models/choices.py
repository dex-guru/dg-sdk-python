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
    all = 'all'
    uniswap_v3 = 'uniswap_v3'
    uniswap = 'uniswap'
    uniswap_v2 = 'uniswap_v2'
    pancakeswap = 'pancakeswap'
    sushiswap = 'sushiswap'
    quickswap = 'quickswap'
    pangolin = 'pangolin'
    traderjoe = 'traderjoe'
    ubeswap = 'ubeswap'
    spookyswap = 'spookyswap'
    spiritswap = 'spiritswap'
    kyber = 'kyber'
    lydia = 'lydia'


class ChainChoices(int, Enum, metaclass=ContaineredEnum):
    eth = 1
    optimism = 10
    bsc = 56
    gnosis = 100
    polygon = 137
    fantom = 250
    arbitrum = 42161
    celo = 42220
    avalanche = 43114
    nova = 42170
    canto = 7700

class TransactionChoices(str, Enum, metaclass=ContaineredEnum):
    swap = 'swap'
    burn = 'burn'
    mint = 'mint'


class OrderChoices(str, Enum):
    asc = 'asc'
    desc = 'desc'


class CategoriesChoices(str, Enum, metaclass=ContaineredEnum):
    noob = 'noob'
    casual = 'casual'
    medium = 'medium'
    heavy = 'heavy'
    bot = 'bot'


class TokenTradeDirections(str, Enum):
    _in = 'in'
    _out = 'out'
