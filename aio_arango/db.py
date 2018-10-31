"""
database
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
import enum
from typing import Optional

from aio_arango.client import ArangoClient


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

    async def _update(self):
        for clc in await self.get_collections():
            setattr(self, clc['name'], ArangoCollection(self, clc['name']))

    async def login(self):
        await super().login()
        await self._update()

    async def get_collections(self, exclude_system: bool = None):
        resp = await self.request(
            'GET', f'/_api/collection',
            params={'excludeSystem': str(bool(exclude_system))})
        return (c for c in (await resp.json())['result'])

    async def create_collection(self, name):
        clc = ArangoCollection(self, name)
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


class DocumentType(enum.Enum):
    vertex = 2
    edge = 3


class ArangoCollection:
    URL = '/_api/collection'

    def __init__(self, client: ArangoDB, name: str, doc_type: Optional[DocumentType] = None):
        self._client = client
        self._name = name
        if doc_type is None:
            doc_type = DocumentType.vertex
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
        data = {'name': self._name, 'type': self._doc_type.value}
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
        return await self._client.request('GET', f'{self.doc_url}/{key}')

    async def all(self, result: str = None):
        data = {'collection': self._name}
        if result not in ['id', 'key', 'path']:
            result = 'path'
        data['type'] = result
        resp = await self._client.request('PUT', f'/_api/simple/all-keys', data)
        return (c for c in (await resp.json())['result'])

    async def add(self, data: dict or list):
        await self._client.request(
            'POST', f'{self.doc_url}', data)

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
