# aio_arango client
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import asyncio
import typing

import aiohttp


class ArangoClient:
    def __init__(self,
                 address: typing.Tuple[str, int] = None,
                 path: str = None,
                 db_name: str = None,
                 loop: asyncio.AbstractEventLoop = None):
        if loop is None:
            loop = asyncio.get_event_loop()
        if path is None:
            con = aiohttp.TCPConnector(loop=loop)
            if address is None:
                address = ('localhost', 8529)
            self._address = address
            self._url_prefix = f'http://{address[0]}:{address[1]}'
            self._path = None
        else:
            con = aiohttp.UnixConnector(path=path, loop=loop)
            self._path = path
            self._address = None
            self._url_prefix = ''
        self._loop = loop
        self._connector = con
        self._auth_token = None
        self._session = None
        self.headers = {'Content-Type': 'application/json'}
        self.db_name = db_name

    @property
    def url_prefix(self):
        if self.db_name is None:
            return self._url_prefix
        return f'{self._url_prefix}/_db/{self.db_name}'

    async def login(self, username: str, password: str):
        self._session = aiohttp.ClientSession(
            connector=self._connector)
        resp = await self._session.request(
            'POST',
            self.url_prefix + '/_open/auth',
            json={'username': username, 'password': password}
            )
        data = await resp.json()
        if resp.status < 300:
            self._auth_token = data['jwt']
            self.headers['Authorization'] = f'bearer {self._auth_token}'
            self._session._default_headers.update(**self.headers)
        return data

    async def close(self):
        await self._session.close()

    async def edges(self, collection_id, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/edges/{collection_id}", **kwargs)

    async def traversal(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/traversal", **kwargs)

    async def transaction(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/transaction", **kwargs)

    async def version(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/version", **kwargs)

    async def engine(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/engine", **kwargs)

    async def batch(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/batch", **kwargs)

    # root user only!
