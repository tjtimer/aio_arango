import enum
from collections import namedtuple
from typing import Optional

QueryResult = namedtuple('QueryResult', 'data meta')


class QueryOption(enum.Enum):
    COUNT = 1
    FULL_COUNT = 2


class Query:

    def __init__(self):
        self._value = []

    def __repr__(self):
        return ' '.join(self._value)

    def for_in(self, identifier: str, collection: str):
        self._value.append(f"FOR {identifier} IN {collection}")
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


class QueryCursor:
    _endpoint: tuple = ('POST', "/_api/cursor")
    __slots__ = ('_request', '_has_more', '_data')

    def __init__(self, query_string: str, *,
                 size: Optional[int]=None,
                 count: Optional[QueryOption]=None):
        self._request = {'query': query_string}
        if count in [QueryOption.COUNT, QueryOption.FULL_COUNT]:
            self._request['count'] = True
            if count is QueryOption.FULL_COUNT:
                self._request['options'] = {'fullCount': True}
        if size:
            self._request['batchSize'] = size

    async def __call__(self, client):
        meth, url = 'POST', "/_api/cursor"
        response = await client.request(
            meth, url,
            data=self._request
        )
        while True:
            data = await response.json()
            if response.status not in [200, 201]:
                yield data['errorMessage']
                break




async def fetch(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/cursor", **kwargs)


async def next(client, cursor_identifier, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/cursor/{cursor_identifier}", **kwargs)


async def delete(client, cursor_identifier, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/cursor/{cursor_identifier}", **kwargs)


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
