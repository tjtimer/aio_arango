# aio_arango endpoints
# created: 02.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import aiohttp


class RequestConfig:
    __slots__ = ('method', 'url', 'kwargs', '_required', '_options')

    def __init__(self, method: str=None, url:str=None,
                 required: dict=None, options:dict=None):
        if method is None:
            method = 'GET'
        self.method = method
        self.url = url
        self.kwargs = {}
        self._required = required
        self._options = options

    def __call__(self, **kwargs):
        self.method = kwargs.pop('method', self.method)
        self.url = (f"{kwargs.pop('url_prepend', '')}"
                    f"{kwargs.pop('url', self.url)}"
                    f"{kwargs.pop('url_append', '')}")
        self.kwargs.update(**kwargs)

    def __str__(self):
        return (f'<RequestConfig {self.method} {self.url} '
                f'{self._required != dict()} {self._options != dict()}>')
    @property
    def required(self):
        return self._required


auth_token = RequestConfig('POST', '/_open/auth')

db_base = '/_api/database'
db_list_all = RequestConfig(url=db_base)
db_list_allowed = RequestConfig(url=f'{db_base}/user')
db_current = RequestConfig(url=f'{db_base}/current')
db_create = RequestConfig('POST', url=db_base, required={'json': 'name'})
db_delete = RequestConfig('DELETE', url=db_base, required={'url_append': 'name'})

clt_base = '/_db/$$db/_api/collection'
clt_create = RequestConfig('POST', clt_base)
clt_load = RequestConfig('PUT', clt_base)
clt_get = RequestConfig('GET', clt_base)
clt_delete = RequestConfig('DELETE', clt_base)

# GRAPH
g_base = '/$$db/_api/gharial'
create_edge = RequestConfig('POST', f'{g_base}/$$g/edge/$$cn')
