import enum
from collections import namedtuple
from typing import Optional

from aio_arango.client import ArangoClient

QueryResult = namedtuple('QueryResult', 'data meta')


class QueryOption(enum.Enum):
    COUNT = 1
    FULL_COUNT = 2


class QueryBuilder:

    def __init__(self):
        self._expressions = []
        self._identifiers = []

    @property
    def statement(self):
        return ' '.join(self._expressions)

    def fi(self, identifier: str, collection: str):
        self._expressions.append(f"FOR {identifier} IN {collection}")
        self._identifiers.append(identifier)
        return self

    def f(self, prop):
        self._expressions.append(f'FILTER {prop}')
        return self

    def and_(self, prop):
        self._expressions.append(f'AND {prop}')
        return self

    def or_(self, prop):
        self._expressions.append(f'OR {prop}')
        return self

    def lt(self, value):
        self._expressions.append(f'< {value}')
        return self

    def lte(self, value):
        self._expressions.append(f'<= {value}')
        return self

    def eq(self, value):
        self._expressions.append(f'== {value}')
        return self

    def neq(self, value):
        self._expressions.append(f'!= {value}')
        return self

    def like(self, value):
        self._expressions.append(f'LIKE {value}')
        return self

    def limit(self, size: int, offset: int = None):
        if offset is None:
            offset = 0
        self._expressions.append(f'LIMIT {abs(int(offset))}, {abs(int(size))}')
        return self

    def asc(self, field):
        self._expressions.append(f'SORT {field} ASC')
        return self

    def desc(self, field):
        self._expressions.append(f'SORT {field} DESC')
        return self

    def ret(self, ):
        self._expressions.append(f"RETURN")
        return self


async def query(client: ArangoClient, query_str: str, *,
                size: Optional[int] = None, count: Optional[QueryOption] = None):
    data = {'query': query_str}
    if count in [QueryOption.COUNT, QueryOption.FULL_COUNT]:
        data['count'] = True
        if count is QueryOption.FULL_COUNT:
            data['options'] = {'fullCount': True}
    if size:
        data['batchSize'] = size
    resp = await client.request('POST', "/_api/cursor", data)
    while True:
        resp_data = await resp.json()
        for obj in resp_data['result']:
            yield obj
        if resp_data['hasMore'] is True:
            resp = await fetch_next(client, resp_data['id'])
        else:
            return


async def fetch(client: ArangoClient, query_str: str, *,
                size: Optional[int] = None, count: Optional[QueryOption] = None):
    data = {'query': query_str}
    if count in [QueryOption.COUNT, QueryOption.FULL_COUNT]:
        data['count'] = True
        if count is QueryOption.FULL_COUNT:
            data['options'] = {'fullCount': True}
    if size:
        data['batchSize'] = size
    resp = await client.request('POST', "/_api/cursor", data)
    resp_data = await resp.json()
    return resp_data.get('id', None), resp_data['result']


async def fetch_next(client, cursor_id):
    resp = await client.request(
        "PUT", f'/_api/cursor/{cursor_id}')
    resp_data = await resp.json()
    return resp_data.get('id', None), resp_data['result']


async def delete(client, cursor_identifier, **kwargs):
    return await client.request(
        'DELETE', f'/_api/cursor/{cursor_identifier}')

