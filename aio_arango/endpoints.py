# aio_arango endpoints
# created: 02.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import aiohttp


class RequestConfig:
    __slots__ = ('method', 'url', 'kwargs', '_required', '_options')
    def __init_subclass__(cls, **kwargs):
        base = ''
        if '_base' in cls.__dict__.keys():
            base = cls.__dict__['_base']
        cls._base = base
        cls.url = cls._base

    def __init__(self, method: str=None, url:str=None,
                 required: dict=None, options:dict=None):
        if method is None:
            method = 'GET'
        self.method = method
        self.url += '' if url is None else url
        self.kwargs = {}
        self._required = required
        self._options = options

    async def __call__(self, session:aiohttp.ClientSession, **kwargs):
        self.method = kwargs.pop('method', self.method)
        self.url = (f"{kwargs.pop('url_prepend', '')}"
                    f"{kwargs.pop('url', self.url)}"
                    f"{kwargs.pop('url_append', '')}")
        self.kwargs.update(**kwargs)
        return session.request(self.method, self.url, **self.kwargs)

    def __str__(self):
        return (f'<RequestConfig {self.method} {self.url} '
                f'{self._required != dict()} {self._options != dict()}>')
    @property
    def required(self):
        return self._required


auth_token = RequestConfig('POST', '/_open/auth')

class DBConfig(RequestConfig):
    base = '/_api/database'
    db_list_all = RequestConfig()
    db_list_allowed = RequestConfig(url=f'/user')
    db_current = RequestConfig(url='/current')
    db_create = RequestConfig(required={'json': 'name'})
    db_delete = RequestConfig(required={'url_append': 'name'})

class CollectionConfig(RequestConfig):
    base = '/_db/$$db/_api/collection'
    collection_create = RequestConfig('POST')
    collection_load = RequestConfig('PUT')
    collection_get = RequestConfig('GET')
    collection_delete = RequestConfig('DELETE')

# GRAPH
g_base = '/$$db/_api/gharial'
create_edge = RequestConfig('POST', f'/$$g/edge/$$cn')
