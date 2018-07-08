# aio_arango endpoints
# created: 02.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
from pprint import pprint

import aiohttp


class Request:

    def __init__(self, client, method: str=None, url:str=None,
                 required: dict=None, options:dict=None, help: dict = None):
        self.client = client
        self._method = method
        self._url = url
        self._required = required
        self._options = options
        self._help = help

    async def __call__(self, *args, **kwargs):
        db_name = kwargs.pop('db_name', self.client.db)
        if db_name is None:
            db_name = ''
        else:
            db_name = f'/_db/{db_name}'
        prefix = self.client._url_prefix + db_name
        url = kwargs.pop('url', self._url)
        for pl, rep in kwargs.pop('url_vars', {}).items():
            orig = '{' + pl.replace('_', '-') + '}'
            url = url.replace(orig, rep)
        method = kwargs.pop('method', self._method)
        headers = kwargs.pop('headers', self.client.headers)
        return await self.client._session.request(method, prefix+url, headers=headers, **kwargs)

    def __str__(self):
        return (f'<Request {self._method} {self._url} '
                f'{self._required != dict()} {self._options != dict()}>')

    @property
    def help(self):
        return self._help
