import asyncio
import logging
import ssl
from typing import AnyStr, Optional
from urllib.parse import urljoin

import aiohttp
import ujson
from aiohttp import ClientTimeout
from pydantic import HttpUrl

import dexguru_sdk
from dexguru_sdk.client.exceptions import RequestException

MAX_RETRY_COUNT = 10
SSL_PROTOCOLS = (asyncio.sslproto.SSLProtocol,)
try:
    import uvloop.loop
except ImportError:
    pass
else:
    SSL_PROTOCOLS = (*SSL_PROTOCOLS, uvloop.loop.SSLProtocol)


class HTTPClient:

    def __init__(self, headers: dict, domain: HttpUrl):
        headers = headers or {}
        default_headers = {
            'User-Agent': f"Python DexGuru SDK v{dexguru_sdk.__version__} ",
            "Content-Type": "application/json",
        }
        self.headers = {**default_headers, **headers}
        self.timeout = ClientTimeout(total=60 * 60, connect=60 * 60, sock_connect=60 * 60, sock_read=60 * 60)
        self.retries_count = 0
        self.retry_sleep = 1.5
        self.domain = domain

    async def get(self, url: AnyStr) -> Optional[dict]:
        url = urljoin(self.domain, url)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False), timeout=self.timeout,
                                         raise_for_status=False) as session:
            logging.debug(f"Fetching {url}")

            async with session.get(url, headers=self.headers, ssl=ssl.SSLContext(),
                                   raise_for_status=False) as response:
                if response.status >= 500:
                    e = await response.json()
                    if self.retries_count == MAX_RETRY_COUNT:
                        raise TimeoutError(RequestException(e))
                    await asyncio.sleep(self.retry_sleep)
                    self.retries_count += 1
                    return await self.get(url)
                if response.status >= 400:
                    t = await response.text()
                    if 'StatementError' in t:
                        if self.retries_count == MAX_RETRY_COUNT:
                            raise TimeoutError(RequestException('sql'))
                        await asyncio.sleep(self.retry_sleep)
                        self.retries_count += 1
                        return await self.get(url)
                    e = await response.json()
                    raise RequestException(e)
                await asyncio.sleep(0.01)
                response_text = await response.text()
                logging.debug(f"Fetched {url}")
                self.retries_count = 0
                return ujson.loads(response_text)

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
