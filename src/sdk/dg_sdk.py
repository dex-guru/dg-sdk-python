import asyncio
from pydantic import HttpUrl

from src.client.aiohttp_client import HTTPClient
from src.models.chain_models import RestChainsListModel


class DgSDK:
    def __init__(self, api_key: str, endpoint: HttpUrl):
        self.client = HTTPClient(headers={'Authorization': f'Bearer {api_key}'}, url_prefix=endpoint)

    async def get_chains(self) -> RestChainsListModel:
        response: dict = await self.client.get('v1/chain/')
        print(response)
        return RestChainsListModel.parse_obj(response)


sdk = DgSDK(api_key='5UOakVpK8YTQHdOS_R8nInB84kk1ZwJzsAlufhp1t0M',
            endpoint='https://api-public-stage.prod-euc1.dexguru.net/')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    d = loop.run_until_complete(sdk.get_chains())
    print(d)
