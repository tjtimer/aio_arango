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
        method = kwargs.pop('method', self._method)
        db_name = kwargs.pop('db_name', self.client._db)
        if 'headers' in kwargs.keys():
            kwargs['headers'].update(**self.client._headers)
        else:
            kwargs['headers'] = self.client._headers
        if db_name is None:
            db_name = ''
        else:
            db_name = f'/_db{db_name}'
        prefix = self.client._url_prefix + db_name
        url = (f"{kwargs.pop('url_prepend', '')}"
               f"{kwargs.pop('url', self._url)}"
               f"{kwargs.pop('url_append', '')}")
        for pl, rep in kwargs.pop('url_vars', {}).items():
            orig = '{' + pl.replace('_', '-') + '}'
            url = url.replace(orig, rep)
        if kwargs.pop('debug', None) is True:
            print('vars request')
            pprint(kwargs)
            print(method, prefix+url)
        return await self.client._session.request(method, prefix+url, **kwargs)

    def __str__(self):
        return (f'<Request {self._method} {self._url} '
                f'{self._required != dict()} {self._options != dict()}>')

    @property
    def help(self):
        return self._help
