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


class CategoriesChoices(str, Enum, metaclass=ContaineredEnum):
    noob = 'noob'
    casual = 'casual'
    medium = 'medium'
    heavy = 'heavy'
    bot = 'bot'


class TokenTradeDirections(str, Enum):
    _in = 'in'
    _out = 'out'
