"""
collection
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
import enum
from typing import Optional

from aio_arango.client import ArangoClient

class DocumentType(enum.Enum):
    vertex = 2
    edge = 3

class ArangoCollection:
    URL = '/_api/collection'

    def __init__(self, client: ArangoClient, name: str, doc_type: Optional[DocumentType]=None):
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

    async def rotate(self):
        return await self._client.request(
            'PUT', f'{self.url}/rotate')

    async def truncate(self):
        return await self._client.request(
            'PUT', f'{self.url}/truncate')

    async def delete(self):
        return await self._client.request(
            'DELETE', f'{self.url}')

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

    async def all(self, result: str=None):
        data = {'collection': self._name}
        if result not in ['id', 'key', 'path']:
            result = 'path'
        data['type'] = result
        return await self._client.request('GET', f'/_api/simple/all-keys', data)

    async def add(self, *, data: dict or list = None):
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
