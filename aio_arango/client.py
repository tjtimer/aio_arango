"""
client
author: Tim "tjtimer" Jedro
created: 23.10.18
"""
import asyncio
from typing import Optional

import aiohttp

from query import QueryCursor, QueryOption


async def setup(username: str, password: str):
    cl = ArangoClient()
    await cl.login(username, password)
    return cl


class ClientError(Exception):
    pass


class AccessLevel:
    NONE = ""
    READ = "ro"
    FULL = "rw"


class ArangoClient:
    _session: aiohttp.ClientSession = None
    _headers: dict = {'Accept': 'application/json'}

    def __init__(self,
                 host: Optional[str]=None,
                 port: Optional[int]=None,
                 scheme: Optional[str]=None):
        if scheme not in 'https':
            scheme = 'http'
        if host is None:
            host = 'localhost'
        if port is None:
            port = 8529
        self._base_url = f'{scheme}://{host}:{port}'
        self._db_name = None

    @property
    def url_prefix(self):
        if self._db_name is None:
            return self._base_url
        return f'{self._base_url}/_db/{self._db_name}'

    async def request(self, method: str, url: str,
                      data: Optional[dict]=None, *,
                      params: Optional[dict]=None,
                      headers: Optional[dict]=None)->aiohttp.ClientResponse:
        cfg = {'headers': self._headers}
        if headers:
            cfg['headers'].update(**headers)
        if data:
            cfg['json'] = data
        if params:
            cfg['params'] = params
        resp = await self._session.request(
            method,
            self.url_prefix + url,
            **cfg
        )
        if resp.status < 300:
            return resp
        raise ClientError((await resp.json())['errorMessage'])

    async def login(self, username: str, password: str):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        response = await self.request(
            'POST', '/_open/auth',
            data={'username': username, 'password': password}
            )
        data = await response.json()
        self._headers['Authorization'] = f"bearer {data['jwt']}"

    async def close(self):
        await self._session.close()
        await asyncio.sleep(0.25)
        self._session = None
