async def cursor(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/cursor", **kwargs)


async def cursor_next(client, cursor_identifier, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/cursor/{cursor_identifier}", **kwargs)


async def cursor_delete(client, cursor_identifier, **kwargs):
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
