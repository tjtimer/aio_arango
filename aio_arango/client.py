# aio_arango client
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import asyncio
import typing
from pathlib import Path
from pprint import pprint

import aiohttp
import yaml

from aio_arango import endpoints as ep


class ArangoClient:
    def __init__(self,
                 address: typing.Tuple[str, int]=None,
                 path: str=None,
                 loop: asyncio.AbstractEventLoop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        if path is None:
            con = aiohttp.TCPConnector(loop=loop)
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
        self._headers = {'Content-Type': 'application/json'}
        self._auth_token = None
        self._session = None
        self._db = None
        with open(Path(__file__).parent.parent / 'url_conf.yaml', 'r') as conf:
            self._api = yaml.load(conf)
        pprint(self._api.keys())

    def db_url(self, db=None, collection=None, graph=None, id=None, v=False, e=False):
        return

    async def setup(self):
        self._session = aiohttp.ClientSession(connector=self._connector)

    async def query(self, config: ep.RequestConfig, **kwargs)-> aiohttp.ClientResponse:
        config(**kwargs)
        self._headers.update(**config.kwargs.pop('headers', {}))
        config.kwargs['headers'] = self._headers
        return await self._session.request(
                config.method, self._url_prefix + config.url,
                **config.kwargs)

    async def get_auth_token(self, username: str, password: str):
        resp = await self._session.request(
                ep.auth_token.method,
                self._url_prefix + ep.auth_token.url,
                json={'username': username, 'password': password}
        )
        data = await resp.json()
        self._auth_token = data['jwt']
        self._headers['Authorization'] = f'bearer {self._auth_token}'
        return self._auth_token

    async def db_list_all(self):
        resp = await self.query(ep.db_list_all)
        data = await resp.json()
        return data['result']

    async def db_list_allowed(self):
        resp = await self.query(ep.db_list_allowed)
        data = await resp.json()
        self._dbs_allowed = data['result']
        return data['result']

    async def db_current(self):
        resp = await self.query(ep.db_current)
        data = await resp.json()
        return data

    async def clt_create(self):
        pass

    async def clt_get(self):
        pass

    async def clt_update(self):
        pass

    async def clt_delete(self):
        pass

    async def graph(self):
        pass
