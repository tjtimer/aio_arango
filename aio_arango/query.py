import asyncio
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
        self._value = []
        self._identifiers = []

    def __repr__(self):
        return ' '.join(self._value)

    def __str__(self):
        return ' '.join(self._value)

    @property
    def query(self):
        return str(self)

    def for_in(self, identifier: str, collection: str):
        self._value.append(f"FOR {identifier} IN {collection}")
        self._identifiers.append(identifier)
        return self

    def filter(self):
        self._value.append(f"FILTER")
        return self

    def eq(self, left: str, right: str):
        self._value.append(f"{left} == {right}")
        return self

    def gt(self, left: str, right: str):
        self._value.append(f"{left} > {right}")
        return self

    def gte(self, left: str, right: str):
        self._value.append(f"{left} >= {right}")
        return self

    def _and(self):
        self._value.append("AND")
        return self

    def _or(self):
        self._value.append("OR")
        return self

    def ret(self):
        self._value.append(f"RETURN")


async def query(client: ArangoClient, query_str: str, *,
                size: Optional[int] = None, count: Optional[QueryOption] = None):
    data = {'query': query_str}
    if count in [QueryOption.COUNT, QueryOption.FULL_COUNT]:
        data['count'] = True
        if count is QueryOption.FULL_COUNT:
            data['options'] = {'fullCount': True}
    if size:
        data['batchSize'] = size
    queue = asyncio.Queue()
    fetch_task = asyncio.create_task(fetch(client, data, queue))
    while True:
        obj = await queue.get()
        yield obj
        if fetch_task.done() and queue.empty():
            raise StopAsyncIteration()


async def fetch(client, data, queue):
    resp = await client.request('POST', "/_api/cursor", data)
    while True:
        resp_data = await resp.json()
        for obj in resp_data['result']:
            await queue.put(obj)
        if resp_data['has_more'] is True:
            resp = await next_batch(client, resp_data['id'])
        else:
            return


async def next_batch(client, cursor_identifier, **kwargs):
    return await client.request(
        "PUT", f'/_api/cursor/{cursor_identifier}')


async def delete(client, cursor_identifier, **kwargs):
    return await client.request(
        'DELETE', f'/_api/cursor/{cursor_identifier}')

"""
async def query(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/query", **kwargs)


async def query_explain(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/explain", **kwargs)


async def query_properties(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/query/properties", **kwargs)


async def query_properties_change(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/query/properties", **kwargs)


async def query_current(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/query/current", **kwargs)


async def query_slow(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/query/slow", **kwargs)


async def query_slow_delete(client, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/query/slow", **kwargs)


async def query_delete(client, query_id, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/query/{query_id}", **kwargs)


async def query_cache_properties(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/query-cache/properties", **kwargs)


async def query_cache_properties_update(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/query-cache/properties", **kwargs)


async def simple(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/first_example", **kwargs)


async def simple_all(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/all", **kwargs)


async def simple_any(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/any", **kwargs)


async def simple_range(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/range", **kwargs)


async def simple_near(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/near", **kwargs)


async def simple_within(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/within", **kwargs)


async def simple_fulltext(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/simple/fulltext", **kwargs)
"""
