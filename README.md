# DexGuruSDK.py

![](//https://pbs.twimg.com/profile_images/1311323925545062402/lQGCxH5M_400x400.jpg)

DexGuruSDK.py allows you to async access public methods
from your python scripts asynchronously.

## Installation

To install latest version, just run:

`pip install DexGuru-SDK`

## Getting Started

```python
import asyncio
from src import DexGuru
from pydantic import BaseModel
YOUR_API_KEY = 'abc123'

sdk = DexGuru(api_key=YOUR_API_KEY)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    response: BaseModel = loop.run_until_complete(sdk.get_amm_mints(chain_id=1, amm='uniswap_v3'))
```

## Response

The response is Pydantic's models, so you can do whatever Pydantic allows with them.

```python
class ChainModel(BaseModel):
    chain_id: int
    name: str
    description: str


class ChainsListModel(BaseModel):
    total: int
    data: List[ChainModel]

```

if you need a simple dict, you can make it from the response:

```python
response = response.dict()
```