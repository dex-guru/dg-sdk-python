# dex-guru-sdk.py

![](https://pbs.twimg.com/profile_images/1311323925545062402/lQGCxH5M_400x400.jpg)

dex-guru-sdk.py allows you to access dex.guru public methods
from your async python scripts.

## Installation

To install latest version, just run:

`pip install dex-guru-sdk`

## Getting Started

```python
import asyncio
from src import DexGuru

YOUR_API_KEY = 'abc123'

sdk = DexGuru(api_key=YOUR_API_KEY)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    response = loop.run_until_complete(sdk.get_amm_mints(chain_id=1, amm='uniswap_v3'))
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