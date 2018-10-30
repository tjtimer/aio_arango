"""
database
author: Tim "tjtimer" Jedro
created: 24.10.18
"""

from typing import Generator, Optional

from aio_arango.client import ArangoClient

INDEX_TYPES = ['fulltext', 'general', 'geo', 'hash', 'persistent', 'skiplist']
URL = '/_api/database'


async def create(client: ArangoClient, name: str, *, users: Optional[list]=None):
    data = {'name': name}
    if users:
        data['users'] = users
    await client.request('POST', f'{URL}', data)


async def available(client)->Generator:
    resp = await client.request('GET', URL)
    return (db for db in (await resp.json())['result'])


async def current(client)->str:
    resp = await client.request('GET', f'{URL}/current')
    return (await resp.json())['result']


async def delete(client, name: str):
    await client.request('DELETE', f'{URL}/{name}')


async def index(client, **kwargs):
    return await client.request(
        'GET', f'/_api/index', **kwargs)

async def create_index(client, type, **kwargs):
    if type not in INDEX_TYPES:
        raise ValueError(f'type must be one of {INDEX_TYPES}')
    return await client.request(
        'POST', f'/_api/index#{type}', **kwargs)

async def delete_index(client, index_handle, **kwargs):
    return await client.request(
        'DELETE', f'/_api/index/{index_handle}', **kwargs)

async def import_document(client, **kwargs):
    return await client.request(
        'POST', f'/_api/import#document', **kwargs)

async def import_json(client, **kwargs):
    return await client.request(
        'POST', f'/_api/import#json', **kwargs)

async def export(client, **kwargs):
    return await client.request(
        'POST', f'/_api/export', **kwargs)

async def user(client, user, **kwargs):
    return await client.request(
        'GET', f'/_api/user/{user}', **kwargs)

async def list_user(client, **kwargs):
    return await client.request(
        'GET', f'/_api/user/', **kwargs)

