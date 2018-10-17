    # aio_arango client
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
    import aiohttp

from typing import Optional, Iterator

from aio_arango.query import QueryCursor, QueryOption
    from typing import Iterator, Optional

    import aiohttp

    from aio_arango.query import QueryCursor, QueryOption


    class ClientError(Exception):
    pass



class ArangoClient:
    _session: aiohttp.ClientSession = None

    def __init__(self,
                 address: Optional[Iterator] = None,
                 path: Optional[str] = None,
                 db_name: Optional[str] = None,
                 scheme: Optional[str]=None):
        if self._session is None:
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
            self._session = aiohttp.ClientSession(connector=connector)
            self.db_name = db_name

    @property
    def url_prefix(self):
        if self.db_name is None:
            return self._url_prefix
        return f'{self._url_prefix}/_db/{self.db_name}'

    async def request(self, method: str, url: str, *,
                      data: Optional[dict]=None,
                      params: Optional[dict]=None,
                      headers: Optional[dict]=None)->aiohttp.ClientResponse:
        cfg = {'headers': self.headers}
        if headers:
            cfg['headers'].update(**headers)
        if data:
            cfg['json'] = data
        if params:
            cfg['params'] = params
        response = await self._session.request(
            method,
            self.url_prefix + url,
            **cfg
        )
        if response.status >= 400:
            raise RuntimeError()
        return response

    async def login(self, username: str, password: str, db_name: str=None):
        response = await self.request(
            'POST', '/_open/auth',
            data={'username': username, 'password': password}
            )
        data = await response.json()
        self.headers['Authorization'] = f"bearer {data['jwt']}"
        self.db_name = db_name
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
                    size: Optional[int]=None,
                    count: Optional[QueryOption]=None):
        return await QueryCursor(query, size=size, count=count)(self)

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
