"""
client
author: Tim "tjtimer" Jedro
created: 23.10.18
"""
import asyncio
from typing import Generator, Optional

import aiohttp

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    print("using uvloop!")
except ImportError:
    uvloop = None
    print("not using uvloop!")


class ClientError(Exception):
    pass


class AccessLevel:
    NONE = ""
    READ = "ro"
    FULL = "rw"


DB_URL = '/_api/database'


class ArangoClient:


    def __init__(self,
                 username: str, password: str, *,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 scheme: Optional[str] = None):
        if scheme not in ['http', 'https']:
            scheme = 'http'
        if host is None:
            host = 'localhost'
        if port is None:
            port = 8529
        self.__credentials = (username, password)
        self._base_url = f'{scheme}://{host}:{port}'
        self._is_authenticated = False
        self._session = None
        self._headers = {'Accept': 'application/json'}
        self._cancelled = []
        self.db = None
        self._request_counter = 0

    @property
    def url_prefix(self):
        if self.db is None:
            return self._base_url
        return f'{self._base_url}/_db/{self.db}'

    @property
    def is_authenticated(self):
        return self._headers.get('Authorization') is not None

    @property
    def request_count(self):
        return self._request_counter

    async def __aenter__(self):
        await self.login()
        return self

    async def __aexit__(self, *exc):
        await self.close()

    async def request(self, method: str, url: str,
                      data: Optional[dict] = None, *,
                      params: Optional[dict] = None,
                      headers: Optional[dict] = None) -> aiohttp.ClientResponse:
        self._request_counter += 1
        cfg = {'headers': self._headers}
        if headers:
            cfg['headers'].update(**headers)
        if data:
            cfg['json'] = data
        if params:
            cfg['params'] = params
        resp = await self._session.request(
            method,
            f'{self.url_prefix}{url}',
            **cfg
        )
        if resp.status < 300:
            return resp
        body = await resp.json()
        # pprint(body)
        raise ClientError(body['errorMessage'])

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
        try:
            await self._session.close()
            await asyncio.sleep(0.5)
        except AttributeError as er:
            print(er)
        finally:
            self._session = None


class ArangoAdmin(ArangoClient):

    def __init__(self, username: str, password: str, *,
                 host: str = None, port: int = None, scheme: str = None):
        super().__init__(username, password, host=host, port=port, scheme=scheme)
        self._databases = []

    async def login(self):
        await super().login()
        self._databases = list(await self.get_dbs())

    async def create_db(self, name: str, *, users: Optional[list] = None):
        data = {'name': name}
        if users:
            data['users'] = users
        await self.request('POST', DB_URL, data)
        self._databases = list(await self.get_dbs())

    async def get_dbs(self) -> Generator:
        resp = await self.request('GET', DB_URL)
        return (db for db in (await resp.json())['result'])

    async def current_db(self) -> str:
        resp = await self.request('GET', f'{DB_URL}/current')
        return (await resp.json())['result']

    async def delete_db(self, name: str):
        await self.request('DELETE', f'{DB_URL}/{name}')
        self._databases = list(await self.get_dbs())

    async def create_user(self,
                          name: str, password: str,
                          active: Optional[bool] = None,
                          extra: Optional[dict] = None):
        user_data = dict(user=name, passwd=password)
        if active is None:
            active = True
        user_data['active'] = active
        if isinstance(extra, dict):
            user_data['extra'] = extra
        return await self.request(
            'POST', f'/_api/user', data=user_data)

    async def get_user(self, name):
        resp = await self.request('GET', f'/_api/user/{name}')
        return (await resp.json())['result']

    async def get_users(self):
        resp = await self.request('GET', f'/_api/user/')
        return (await resp.json())['result']

    async def update_user(self, name: str, data: dict):
        await self.request('PATCH', f'/_api/user/{name}', data)

    async def replace_user(self, name: str, data: dict):
        await self.request('PUT', f'/_api/user/{name}', data)

    async def delete_user(self, name: str):
        await self.request('DELETE', f'/_api/user/{name}')

    async def get_user_dbs(self, name: str) -> Generator:
        resp = await self.request('GET', f'/_api/user/{name}/database')
        return (db for db in (await resp.json())['result'])

    async def get_access_level(self, name: str, db: str,
                               collection: Optional[str] = None) -> AccessLevel:
        url = f'/_api/user/{name}/database'
        handle = db
        if collection:
            handle = f"{db}/{collection}"
        resp = await self.request('GET', f"{url}/{handle}")
        return (await resp.json())[handle]

    async def set_access_level(self,
                               name: str, db: str, collection: Optional[str] = None,
                               level: AccessLevel = None):
        if level is None:
            level = AccessLevel.READ
        url = f'/_api/user/{name}/database'
        handle = db
        if collection:
            handle = f"{db}/{collection}"
        await self.request('PUT', f"{url}/{handle}", data={'grant': level})

    async def reset_access_level(self, name: str, db: str, collection: Optional[str] = None):
        url = f'/_api/user/{name}/database'
        handle = db
        if collection:
            handle = f"{db}/{collection}"
        await self.request('DELETE', f"{url}/{handle}")
