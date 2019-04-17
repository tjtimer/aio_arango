import enum
from collections import namedtuple
from dataclasses import dataclass
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


@dataclass
class QueryRequestOptions:
    """
    "options": {
        "failOnWarning": true,
        "fullCount": true,
        "intermediateCommitCount": 0,
        "intermediateCommitSize": 0,
        "maxPlans": 0,
        "maxTransactionSize": 0,
        "maxWarningCount": 0,
        "optimizer.rules": [
          "string"
        ],
        "profile": 0,
        "satelliteSyncWait": true,
        "skipInaccessibleCollections": true,
        "stream": true
      },
    """

    def __init__(self,
                 fail_on_warning: bool = None,
                 full_count: bool = None,
                 intermediate_commit_count: int = None,
                 intermediate_commit_size: int = None,
                 max_warning_count: int = None,
                 profile: int = None,
                 satellite_sync_wait: bool = None,
                 skip_inaccessible_collections: bool = None,
                 stream: bool = None):
        self.fail_on_warning = fail_on_warning or False
        self.full_count = full_count or False
        self.intermediate_commit_count = intermediate_commit_count or 0
        self.intermediate_commit_size = intermediate_commit_size or 0
        self.max_warning_count = max_warning_count or 0
        self.profile = profile or 0
        self.satellite_sync_wait = satellite_sync_wait or False
        self.skip_inaccessible_collections = skip_inaccessible_collections or True
        self.stream = stream or False

    class Optimizer:
        rules = []

    @property
    def optimizer(self):
        return self.Optimizer


class QueryRequest:
    """
    example: {
      "batchSize": 0,
      "bindVars": [
        {}
      ],
      "cache": true,
      "count": true,
      "memoryLimit": 0,
      "options": {
        "failOnWarning": true,
        "fullCount": true,
        "intermediateCommitCount": 0,
        "intermediateCommitSize": 0,
        "maxPlans": 0,
        "maxTransactionSize": 0,
        "maxWarningCount": 0,
        "optimizer.rules": [
          "string"
        ],
        "profile": 0,
        "satelliteSyncWait": true,
        "skipInaccessibleCollections": true,
        "stream": true
      },
      "query": "string",
      "ttl": 0
    }
    """

    def __init__(self,
                 query: QueryBuilder,
                 bind_vars: list or tuple = None,
                 batch_size: int = None,
                 cache: bool = None,
                 count: bool = None,
                 memory_limit: int = None,
                 options: QueryRequestOptions = None):
        self._query = query
        self._bind_vars = bind_vars or []
        self._batch_size = batch_size or 25
        self._cache = cache or False
        self._count = count or False
        self._memory_limit = memory_limit or int(5 * 1024 * 1024)  # 5 MegaByte
        self._options = options or QueryRequestOptions()


class ArangoQuery:
    __slots__ = (
        '_id', '_request', '_result',
        '_page_info', '_error', '_code'
    )

    def __init__(self):
        self._id = None
        self._request = None
        self._result = None
        self._page_info = None


async def query(
        client: ArangoClient,
        query_str: str, *,
        size: int = None,
        count: bool = None,
        full_count: bool = None):

    data = {
        'query': query_str,
        'batchSize': size or 25,
        'count': count or False,
        'options': {
            'fullCount': full_count or False
        }
    }
    resp = await client.request('POST', "/_api/cursor", data)
    while True:
        resp_data = await resp.json()
        yield resp_data
        if resp_data['hasMore'] is False:
            return
        cancelled = resp_data['id'] in client._cancelled
        if cancelled:
            await delete(client, resp_data['id'])
            return
        resp = await client.request('PUT', f"/_api/cursor/{resp_data['id']}")


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


async def delete(client, cursor_id):
    resp = await client.request(
        'DELETE', f'/_api/cursor/{cursor_id}')
    client._cancelled.remove(cursor_id)
    return resp

