"""
database
author: Tim "tjtimer" Jedro
created: 24.10.18
"""

from typing import Generator, Optional

from aio_arango.client import ArangoClient
from aio_arango.collection import ArangoCollection


class IndexType:
    FULL_TEXT = 'fulltext'
    GENERAL = 'general'
    GEO = 'geo'
    HASH = 'hash'
    PERSISTENT = 'persistent'
    SKIP_LIST = 'skiplist'


class ArangoDB(ArangoClient):
    def __init__(self, username: str, password: str, db_name: str, *,
                 host: str=None, port: int=None, scheme: str=None):
        super().__init__(username, password, host=host, port=port, scheme=scheme)
        self.db = db_name

    async def collections(self, exclude_system: bool = None):
        resp = await self.request('GET', f'/_api/collection', params={'excludeSystem': bool(exclude_system)})
        return (c for c in (await resp.json())['result'])

    async def create_collection(self, name):
        clc = ArangoCollection(self, name)
        await clc.create()
        setattr(self, name, clc)

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
    
    async def user(self, user, **kwargs):
        return await self.request(
            'GET', f'/_api/user/{user}', **kwargs)
    
    async def list_user(self, **kwargs):
        return await self.request(
            'GET', f'/_api/user/', **kwargs)