    # aio_arango client
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import enum
from typing import Optional, Tuple

import aiohttp


class ClientError(Exception):
    pass


class QueryOption(enum.Enum):
    COUNT = 1
    FULL_COUNT = 2


class ArangoClient:
    def __init__(self,
                 address: Optional[Tuple, list][str, int] = None,
                 path: Optional[str] = None,
                 db_name: Optional[str] = None,
                 scheme: Optional[str]=None):
        if path is None:
            connector = aiohttp.TCPConnector()
            if address is None:
                address = ('localhost', 8529)
            self._address = (*address, scheme)
            self._url_prefix = f'{scheme}://{address[0]}:{address[1]}'
            self._path = None
        else:
            connector = aiohttp.UnixConnector(path=path)
            self._path = path
            self._address = None
            self._url_prefix = ''
        self._auth_token = None
        self.headers = {'Content-Type': 'application/json'}
        self._session =  aiohttp.ClientSession(connector=connector)
        self.db_name = db_name

    @property
    def url_prefix(self):
        if self.db_name is None:
            return self._url_prefix
        return f'{self._url_prefix}/_db/{self.db_name}'

    async def _request(self, endpoint: tuple[str, str], config: dict=None)->aiohttp.ClientResponse:
        cfg = config or {}
        response = await self._session.request(
            endpoint[0],
            self.url_prefix + endpoint[1],
            headers=self.headers,
            **cfg
        )
        return response

    async def login(self, username: str, password: str):
        resp = await self._request(
            ('POST', '/_open/auth'),
            config={'json': {'username': username, 'password': password}}
            )
        data = await resp.json()
        if resp.status < 300:
            self.headers['Authorization'] = f"bearer {data['jwt']}"
        return data

    async def stream(self):
        pass

    async def close(self):
        await self._session.close()

    async def edges(self, collection_id, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/edges/{collection_id}", **kwargs)

    async def traversal(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/traversal", **kwargs)

    async def query(self, query: str, *,
                    id: Optional[str, int]=None,
                    size: Optional[int]=None,
                    count: Optional[int, QueryOption]=None):
        config = {'json': {'query': query}}
        endpoint = ('POST', "/_api/cursor")
        if id:
            endpoint = (endpoint[0], f"{endpoint[1]}/{id}")
        if size is None and count is None:
            return await self._request(endpoint, config)
        if count is QueryOption.COUNT:
            config['json']['count'] = True
        if count is QueryOption.FULL_COUNT:
            config['json']['fullCount'] = True
        if size:
            config['json']['batchSize'] = size
        return await self._request(endpoint, config)

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
