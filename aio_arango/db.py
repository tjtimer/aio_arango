"""
database
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
import asyncio
import enum
from typing import Optional

from aio_arango.client import ArangoClient
from aio_arango.graph import ArangoGraph
from aio_arango.query import delete, fetch, fetch_next, query


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
        self._db = db
        self._collections = {}
        self._graphs = {}

    def __getattr__(self, item):
        if item in self._graphs.keys():
            return self._graphs[item]
        return self._collections[item]

    def __getitem__(self, item):
        if item in self._graphs.keys():
            return self._graphs[item]
        return self._collections[item]

    async def _update(self):
        collections, graphs = await asyncio.gather(*(
            self.get_collections(),
            ArangoGraph.all(self)
        ))
        for clc in collections:
            if clc['name'] not in self._collections.keys():
                self._collections[clc['name']] = ArangoCollection(self, clc['name'])
        for gr in graphs:
            if gr['_key'] not in self._graphs.keys():
                self._graphs[gr['_key']] = ArangoGraph(self,
                                                       gr['_key'],
                                                       gr['edgeDefinitions'],
                                                       gr['orphanCollections'])

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
        if name not in self._collections.keys():
            clc = ArangoCollection(self, name, doc_type)
            await clc.create()
            await self._update()

    async def create_graph(self, name, edge_definitions: list):
        if name not in self._graphs.keys():
            gr = ArangoGraph(self, name, edge_definitions)
            await gr.create()
            await self._update()

    async def index(self, **kwargs):
        return await self.request(
            'GET', f'/_api/index', **kwargs)

    async def create_index(self, collection: str, cfg: dict):
        resp = await self.request(
            'POST', f'/_api/index?collection={collection}', cfg)
        return await resp.json()

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
            results = obj.get('result', None)
            if results:
                for item in results:
                    yield item

    async def fetch(self, query_str: str, options: dict = None):
        if options is None:
            options = {}
        return await fetch(self, query_str, **options)

    async def fetch_one(self, query_str: str, options: dict = None):
        if options is None:
            options = {}
        try:
            c_id, data = await fetch(self, query_str, size=1, **options)
            if len(data) <= 1:
                return data or {}
            return data[0]
        finally:
            if c_id != '' and c_id is not None:
                await delete(self, c_id)

    async def fetch_next(self, cursor_id):
        return await fetch_next(self, cursor_id)


class ArangoCollection:
    URL = '/_api/collection'

    def __init__(self, client: ArangoDB, name: str, doc_type: Optional[DocumentType] = None):
        self.__collection_name = name
        if doc_type is None:
            doc_type = DocumentType.VERTEX
        self._doc_type = doc_type
        self._client = client

    @property
    def name(self):
        return self.__collection_name

    @property
    def url(self):
        return f'{self.URL}/{self.__collection_name}'

    @property
    def doc_url(self):
        return f'/_api/document/{self.__collection_name}'

    async def create(self):
        data = {'name': self.__collection_name}
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
        self.__collection_name = new_name
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
        data = {'collection': self.__collection_name}
        resp = await self._client.request('PUT', f'/_api/simple/all', data)
        return (c for c in (await resp.json())['result'])

    async def add(self, data: dict or list, params: dict = None):
        resp = await self._client.request(
            'POST', f'{self.doc_url}', data, params=params)
        return await resp.json()

    async def update(self, key, data: dict, params: dict = None):
        resp = await self._client.request(
            'PATCH', f'{self.doc_url}/{key}', data, params=params)
        return await resp.json()

    async def replace(self, key, data: dict):
        resp = await self._client.request(
            'PUT', f'{self.doc_url}/{key}', data)
        return await resp.json()

    async def remove(self, key):
        resp = await self._client.request('DELETE', f'{self.doc_url}/{key}')
        return await resp.json()

    async def head(self, key):
        resp = await self._client.request('HEAD', f'{self.doc_url}/{key}')
        return await resp.json()
