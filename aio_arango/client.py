"""
client
author: Tim "tjtimer" Jedro
created: 23.10.18
"""
import asyncio
from typing import Optional, Generator

import aiohttp


class ClientError(Exception):
    pass


class AccessLevel:
    NONE = ""
    READ = "ro"
    FULL = "rw"

DB_URL = '/_api/database'

class ArangoClient:
    _session: aiohttp.ClientSession = None
    _headers: dict = {'Accept': 'application/json'}

    def __init__(self,
                 username: str, password: str, *,
                 host: Optional[str]=None,
                 port: Optional[int]=None,
                 scheme: Optional[str]=None):
        if scheme not in ['http', 'https']:
            scheme = 'http'
        if host is None:
            host = 'localhost'
        if port is None:
            port = 8529
        self._base_url = f'{scheme}://{host}:{port}'
        self.__credentials = (username, password)
        self._is_authenticated = False
        self.db = None

    @property
    def url_prefix(self):
        if self.db is None:
            return self._base_url
        return f'{self._base_url}/_db/{self.db}'

    @property
    def is_authenticated(self):
        return self._headers.get('Authorization') is not None

    async def __aenter__(self):
        await self.login()
        return self

    async def __aexit__(self, *exc):
        await self.close()

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

    async def login(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        response = await self.request(
            'POST', '/_open/auth',
            data={'username': self.__credentials[0], 'password': self.__credentials[1]}
            )
        data = await response.json()
        self._headers['Authorization'] = f"bearer {data['jwt']}"

    async def close(self):
        self._headers.pop('Authorization', None)
        await self._session.close()
        await asyncio.sleep(0.25)
        self._session = None

    async def create_db(self, name: str, *, users: Optional[list] = None):
        self.db = None
        data = {'name': name}
        if users:
            data['users'] = users
        await self.request('POST', DB_URL, data)

    async def get_dbs(self) -> Generator:
        resp = await self.request('GET', DB_URL)
        return (db for db in (await resp.json())['result'])

    async def current_db(self) -> str:
        resp = await self.request('GET', f'{DB_URL}/current')
        return (await resp.json())['result']

    async def delete_db(self, name: str):
        await self.request('DELETE', f'{DB_URL}/{name}')

    async def create_user(self,
                          name: str, password: str,
                          active: Optional[bool]=None,
                          extra: Optional[dict]=None):
        user_data = dict(user=name, passwd=password)
        if active is None:
            active = True
        user_data['active'] = active
        if isinstance(extra, dict):
            user_data['extra'] = extra
        return await self.request(
            'POST', f'/_api/user', data=user_data)

    async def update_user(self, name: str, data: dict):
        await self.request('PATCH', f'/_api/user/{name}', data)

    async def replace_user(self, name: str, data: dict):
        await self.request('PUT', f'/_api/user/{name}', data)

    async def delete_user(self, name: str):
        await self.request('DELETE', f'/_api/user/{name}')

    async def get_user_dbs(self, name: str)->Generator:
        resp = await self.request('GET', f'/_api/user/{name}/database')
        return (db for db in (await resp.json())['result'])

    async def get_access_level(self, name: str, db: str,
                               col_name: Optional[str]=None)->AccessLevel:
        url = f'/_api/user/{name}/database'
        handle = db
        if col_name:
            handle = f"{db}/{col_name}"
        resp = await self.request('GET', f"{url}/{handle}")
        return (await resp.json())[handle]

    async def set_access_level(self,
                               name: str, db: str, col_name: str,
                               level: AccessLevel):
        url = f'/_api/user/{name}/database'
        handle = db
        if col_name:
            handle = f"{db}/{col_name}"
        await self.request('PUT', f"{url}/{handle}", data={'grant': level})

    async def reset_access_level(self, name: str, db: str, col_name: str):
        url = f'/_api/user/{name}/database'
        handle = db
        if col_name:
            handle = f"{db}/{col_name}"
        await self.request('DELETE', f"{url}/{handle}")
