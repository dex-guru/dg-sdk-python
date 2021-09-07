import asyncio
import ssl
import logging
from typing import Union, List, Optional
from pydantic import HttpUrl

import aiohttp
import ujson
from aiohttp import ClientConnectionError, ClientTimeout, ClientOSError, ClientResponseError, InvalidURL

URL_PREFIX = 'https://api-public-stage.prod-euc1.dexguru.net/'
SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol,)
try:
    import uvloop.loop
except ImportError:
    pass
else:
    SSL_PROTOCOLS = (*SSL_PROTOCOLS, uvloop.loop.SSLProtocol)


class HTTPClient:

    def __init__(self, headers: Optional[dict] = None, retry_sleep: int = 60, url_prefix: HttpUrl = URL_PREFIX):
        headers = headers or {}
        default_headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                          " (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
            "Content-Type": "application/json"
        }
        self.headers = {**default_headers, **headers}
        self.timeout = ClientTimeout(total=60 * 60, connect=60 * 60, sock_connect=60 * 60, sock_read=60 * 60)
        self.retries_count = 0
        self.retry_sleep = retry_sleep
        self.url_prefix = url_prefix
        # TODO add some health_check and/or auth_check

    async def get(self, url: str, retry_sleep: Optional[int] = None) -> Union[dict, None]:
        url = self.url_prefix + '/v1/chain' + url
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=self.timeout,
                                         raise_for_status=False) as session:
            try:
                logging.debug(f"Fetching {url}")

                async with session.get(url, headers=self.headers, ssl=ssl.SSLContext(),
                                       raise_for_status=False) as response:
                    # TODO exc details
                    await asyncio.sleep(0.01)
                    response_text = await response.text()
                    logging.debug(f"Fetched {url}")
                    return ujson.loads(response_text)
            except (ClientOSError, ValueError, ClientConnectionError, InvalidURL) as e:
                logging.error(f"Error fetching {url}, {e}")
                return None
            except ClientResponseError as e:
                if e.status == 404:
                    logging.error(f"Not found {url}, {e}")
                    return None
                elif e.status == 429:
                    logging.debug(f"Got rate limited, sleeping for a minute and retry {url}")
                    await asyncio.sleep(retry_sleep or self.retry_sleep)
                    return await self.get(url)
                else:
                    logging.error(f"Error fetching {url}, {e}")
                    return None

    async def fetch_raw(self, url: str, retry_sleep: Optional[int] = None) -> Union[bytes, None]:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=self.timeout,
                                         raise_for_status=True) \
                as session:
            try:
                logging.debug(f"Fetching {url}")
                async with session.get(url, headers=self.headers, ssl=ssl.SSLContext(),
                                       raise_for_status=True) as response:
                    await asyncio.sleep(0.01)
                    response_bytes = await response.read()
                    logging.debug(f"Fetched {url}")
                    return response_bytes
            except (ClientOSError, ValueError, ClientConnectionError, InvalidURL) as e:
                logging.error(f"Error fetching {url}, {e}")
                return None
            except ClientResponseError as e:
                if e.status == 404:
                    logging.error(f"Not found {url}, {e}")
                    return None
                elif e.status == 429:
                    logging.debug(f"Got rate limited, sleeping for a minute and retry {url}")
                    await asyncio.sleep(retry_sleep or self.retry_sleep)
                    return await self.fetch_raw(url)
                else:
                    logging.error(f"Error fetching {url}, {e}")
                    return None

    @staticmethod
    def ignore_aiohttp_ssl_error(loop):
        """Ignore aiohttp #3535 / cpython #13548 issue with SSL data after close

        There is an issue in Python 3.7 up to 3.7.3 that over-reports a
        ssl.SSLError fatal error (ssl.SSLError: [SSL: KRB5_S_INIT] application data
        after close notify (_ssl.c:2609)) after we are already done with the
        connection. See GitHub issues aio-libs/aiohttp#3535 and
        python/cpython#13548.

        Given a loop, this sets up an exception handler that ignores this specific
        exception, but passes everything else on to the previous exception handler
        this one replaces.

        Checks for fixed Python versions, disabling itself when running on 3.7.4+
        or 3.8.

        """
        orig_handler = loop.get_exception_handler()

        def ignore_ssl_error(loop, context):
            if context.get("message") in {
                "SSL error in data received",
                "Fatal error on transport",
            }:
                # validate we have the right exception, transport and protocol
                exception = context.get('exception')
                protocol = context.get('protocol')
                if (
                        isinstance(exception, ssl.SSLError)
                        and exception.reason == 'KRB5_S_INIT'
                        and isinstance(protocol, SSL_PROTOCOLS)
                ):
                    if loop.get_debug():
                        asyncio.log.logger.debug('Ignoring asyncio SSL KRB5_S_INIT error')
                    return
            if orig_handler is not None:
                orig_handler(loop, context)
            else:
                loop.default_exception_handler(context)

        loop.set_exception_handler(ignore_ssl_error)

    async def get_all(self, urls: List[str], assert_fetched: bool = True) -> List[dict]:
        get_tasks = []
        for url in urls:
            get_tasks.append(asyncio.create_task(self.get(url)))
        results = await asyncio.gather(*get_tasks)
        # removing nones from results
        results = list(filter(None, results))
        if assert_fetched:
            assert len(results) == len(urls)
        return results
