# dexguru-sdk.py

![dexguru-logo](https://gblobscdn.gitbook.com/assets%2F-MO2nrmwh_DoxKc1v80n%2F-MTnknohxY_QQWqZ5rp-%2F-MTnm7ZgN7sBW_vNX_z1%2Fhorizontal-logo-white-background.png?alt=media&token=f6e37f23-afd5-4a13-bb6a-162e1d95d18d)

dexguru-sdk.py allows you to access <a href=https://dex.guru>dex.guru</a> public methods
from your async python scripts.

## Installation

To install latest version, just run:

`pip install dexguru-sdk`


## Getting Started
Take API key of your project from <a href=https://developers.dex.guru>developers.dex.guru</a>


```python
import asyncio
from dexguru_sdk import DexGuru

YOUR_API_KEY = 'abc123'

sdk = DexGuru(api_key=YOUR_API_KEY)

async def main():
    response = await sdk.get_chains()
    return response

if __name__ == '__main__':
    asyncio.run(main())
```

## Response

SDK response is Pydantic's models, so you can do whatever <a href=https://pydantic-docs.helpmanual.io/>Pydantic</a> allows with them.

You can find all models at `dexguru_sdk.models`:
```python
class ChainModel(BaseModel):
    chain_id: int
    name: str
    description: str


class ChainsListModel(BaseModel):
    total: int
    data: List[ChainModel]
```

```python
from typing import List
from dexguru_sdk.models import ChainModel, ChainsListModel


response: ChainsListModel
total: int = response.total
data: List[ChainModel] = response.data
```

if you need a simple dict from response, Pydantic can convert it:

```python
response = response.dict()
```

## Usage Examples

Ok, we want to see how your favorite wallets are trading:

```python
import asyncio
from dexguru_sdk import DexGuru

sdk = DexGuru(api_key='my_sweet_key_from_sweet_project')

wallets = ['bot_wallet_address1', 'mistake_wallet_address2', 'heavy_wallet_address3']


async def main():
    wallets_info: WalletsListModel = await sdk.get_wallets_info(
        chain_id=1,
        wallet_addresses=wallets,
    )
    return wallets_info

if __name__ == '__main__':
    asyncio.run(main())
```

`wallets_info.total == 2` because we have mistake in address2 and it was skipped

Print `wallets_info` object:
```python
total=2 data=[
    WalletModel(
        wallet_address='bot_wallet_address1',
        volume_1m_usd=5000.123456,
        txns_1m=999999,
        category='bot',
        timestamp=1621635936 # last tx timestamp
    ),
    WalletModel(
        wallet_address='whale_wallet_address3',
        volume_1m_usd=107382.62431031652,
        txns_1m=8699,
        category='heavy',
        timestamp=1621635936 # last tx timestamp
    )]
```
Wow, they are good traders! Let's see what transactions they made:

```python
wallets = ['bot_wallet_address1', 'mistake_wallet_address2', 'heavy_wallet_address3']

async def get_txs_from_list_of_wallets(wallets: List[str]) -> List:
    result = []
    for wallet in wallets:
        txs = await sdk.get_wallet_transactions(chain_id=1, wallet_address=wallet)
        result.append(txs)
    return result

if __name__ == '__main__':
    result = asyncio.run(get_txs_from_list_of_wallets(wallets))
```
