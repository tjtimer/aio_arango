# aio_arango client
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import asyncio
import typing
from pprint import pprint

import aiohttp

from aio_arango.api import ArangoAPI


class ArangoClient:
    def __init__(self,
                 address: typing.Tuple[str, int]=None,
                 path: str=None,
                 database: str = None,
                 loop: asyncio.AbstractEventLoop=None):
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
        self._api = ArangoAPI(self)
        self.headers = {'Content-Type': 'application/json'}
        self.db = database

    async def login(self, username: str, password: str):
        self._session = aiohttp.ClientSession(connector=self._connector)
        resp = await self._session.request(
                'POST',
                self._url_prefix + '/_open/auth',
                json={'username': username, 'password': password}
        )
        data = await resp.json()
        if resp.status < 300:
            self._auth_token = data['jwt']
            self.headers['Authorization'] = f'bearer {self._auth_token}'
        return data

    async def close(self):
        await self._session.close()
