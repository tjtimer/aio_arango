"""
collection
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
from aio_arango.client import ArangoClient

URL = '/_api/collection'


async def available(client: ArangoClient, exclude_system: bool=None):
    resp = await client.request('GET', f'{URL}', params={'excludeSystem': bool(exclude_system)})
    return (c for c in (await resp.json())['result'])


async def create(client: ArangoClient, data: dict):
    await client.request('POST', f'{URL}', data)


async def load(client: ArangoClient, name: str, *, count=None, col_type=None):
    data = {'count': bool(count)}
    if col_type in [2, 3]:
        data['type'] = col_type
    resp = await client.request('PUT', f'{URL}/{name}/load', data)
    return {k: v for k, v in (await resp.json()) if k not in ['error', 'code']}


async def unload(client: ArangoClient, name):
    await client.request('PUT', f'{URL}/{name}/unload')


async def rename(client: ArangoClient, name, **kwargs):
    return await client.request(
        'PUT', f'{URL}/{name}/rename', **kwargs)


async def rotate(client: ArangoClient, name, **kwargs):
    return await client.request(
        'PUT', f'{URL}/{name}/rotate', **kwargs)


async def truncate(client: ArangoClient, name, **kwargs):
    return await client.request(
        'PUT', f'{URL}/{name}/truncate',
        **kwargs)


async def delete(client: ArangoClient, name, **kwargs):
    return await client.request(
        'DELETE', f'{URL}/{name}', **kwargs)


async def count(client: ArangoClient, name, **kwargs):
    return await client.request(
        'GET', f'{URL}/{name}/count', **kwargs)


async def stats(client: ArangoClient, name, **kwargs):
    return await client.request(
        'GET', f'{URL}/{name}/figures', **kwargs)


async def revision(client: ArangoClient, name, **kwargs):
    return await client.request(
        'GET', f'{URL}/{name}/revision',
        **kwargs)


async def checksum(client: ArangoClient, name, **kwargs):
    return await client.request(
        'GET', f'{URL}/{name}/checksum',
        **kwargs)


async def properties(client: ArangoClient, name, **kwargs):
    return await client.request(
        'GET', f'{URL}/{name}/properties',
        **kwargs)

async def update_properties(client: ArangoClient, name, **kwargs):
    return await client.request(
        'PUT', f'{URL}/{name}/properties',
        **kwargs)


async def load_indexes(client: ArangoClient, name, **kwargs):
    return await client.request(
        'PUT',
        f'{URL}/{name}/loadIndexesIntoMemory',
        **kwargs)
