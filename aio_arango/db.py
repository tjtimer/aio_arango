"""
database
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
import enum
from typing import Optional

from aio_arango.client import ArangoClient
from aio_arango.query import fetch, fetch_next, query


class DocumentType(enum.Enum):
    VERTEX = 2
    EDGE = 3


class IndexType:
    FULL_TEXT = 'fulltext'
    GENERAL = 'general'
    GEO = 'geo'
    HASH = 'hash'
    PERSISTENT = 'persistent'
    SKIP_LIST = 'skiplist'


class ArangoDB(ArangoClient):
    def __init__(self, username: str, password: str, db: str, *,
                 host: str = None, port: int = None, scheme: str = None):
        super().__init__(username, password, host=host, port=port, scheme=scheme)
        self.db = db
        self._collections = {}

    def __getattr__(self, item):
        return self._collections[item]

    def __getitem__(self, item):
        return self._collections[item]

    async def _update(self):
        for clc in await self.get_collections():
            if clc['name'] not in self._collections.keys():
                self._collections[clc['name']] = ArangoCollection(self, clc['name'])

    async def login(self):
        await super().login()
        await self._update()

    async def get_collections(self, exclude_system: bool = None):
        if exclude_system is None:
            exclude_system = True
        resp = await self.request(
            'GET', f'/_api/collection',
            params={'excludeSystem': str(bool(exclude_system))})
        return (c for c in (await resp.json())['result'])

    async def create_collection(self, name, doc_type: Optional[DocumentType] = None):
        clc = ArangoCollection(self, name, doc_type)
        if name not in self._collections.keys():
            await clc.create()
            await self._update()

    async def index(self, **kwargs):
        return await self.request(
            'GET', f'/_api/index', **kwargs)

    async def create_index(self, idx_type: IndexType, **kwargs):
        return await self.request(
            'POST', f'/_api/index#{idx_type}', **kwargs)

    async def delete_index(self, index_handle, **kwargs):
        return await self.request(
            'DELETE', f'/_api/index/{index_handle}', **kwargs)

    async def import_document(self, **kwargs):
        return await self.request(
            'POST', f'/_api/import#document', **kwargs)

    async def import_json(self, **kwargs):
        return await self.request(
            'POST', f'/_api/import#json', **kwargs)

    async def export(self, **kwargs):
        return await self.request(
            'POST', f'/_api/export', **kwargs)

    async def query(self, query_str: str, options: dict = None):
        if options is None:
            options = {}
        async for obj in query(self, query_str, **options):
            yield obj

    async def fetch(self, query_str: str, options: dict = None):
        if options is None:
            options = {}
        return await fetch(self, query_str, **options)

    async def fetch_next(self, cursor_id):
        return await fetch_next(self, cursor_id)


class ArangoCollection():
    URL = '/_api/collection'

    def __init__(self, client: ArangoDB, name: str, doc_type: Optional[DocumentType] = None):
        self._client = client
        self._name = name
        if doc_type is None:
            doc_type = DocumentType.VERTEX
        self._doc_type = doc_type

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return f'{self.URL}/{self._name}'

    @property
    def doc_url(self):
        return f'/_api/document/{self._name}'

    async def create(self):
        data = {'name': self._name}
        if self._doc_type == DocumentType.EDGE:
            data['type'] = 3
        await self._client.request('POST', f'{self.URL}', data)

    async def load(self, *, count=None, col_type=None):
        data = {'count': bool(count)}
        if col_type in [2, 3]:
            data['type'] = col_type
        resp = await self._client.request('PUT', f'{self.url}/load', data)
        return {k: v for k, v in (await resp.json()) if k not in ['error', 'code']}

    async def unload(self):
        await self._client.request('PUT', f'{self.url}/unload')

    async def rename(self, new_name: str):
        await self._client.request(
            'PUT', f'{self.url}/rename', {'name': new_name})
        self._name = new_name
        await self._client._update()

    async def rotate(self):
        await self._client.request(
            'PUT', f'{self.url}/rotate')

    async def truncate(self):
        return await self._client.request(
            'PUT', f'{self.url}/truncate')

    async def delete(self):
        await self._client.request('DELETE', f'{self.url}')
        await self._client._update()

    async def count(self):
        return await self._client.request(
            'GET', f'{self.url}/count')

    async def stats(self):
        return await self._client.request(
            'GET', f'{self.url}/figures')

    async def revision(self):
        return await self._client.request(
            'GET', f'{self.url}/revision')

    async def checksum(self):
        return await self._client.request(
            'GET', f'{self.url}/checksum')

    async def properties(self):
        return await self._client.request(
            'GET', f'{self.url}/properties')

    async def update_properties(self):
        return await self._client.request(
            'PUT', f'{self.url}/properties')

    async def load_indexes(self):
        return await self._client.request(
            'PUT', f'{self.url}/loadIndexesIntoMemory')

    # documents

    async def get(self, key):
        resp = await self._client.request('GET', f'{self.doc_url}/{key}')
        return await resp.json()


    async def all(self):
        data = {'collection': self._name}
        resp = await self._client.request('PUT', f'/_api/simple/all', data)
        return (c for c in (await resp.json())['result'])

    async def add(self, data: dict or list):
        resp = await (await self._client.request(
            'POST', f'{self.doc_url}', data)).json()
        return resp

    async def update(self, key, data: dict):
        return await self._client.request(
            'PATCH', f'{self.doc_url}/{key}', data)

    async def replace(self, key, data: dict):
        return await self._client.request(
            'PUT', f'{self.doc_url}/{key}', data)

    async def remove(self, key):
        return await self._client.request('DELETE', f'{self.doc_url}/{key}')

    async def head(self, key):
        return await self._client.request('HEAD', f'{self.doc_url}/{key}')
