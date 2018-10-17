from typing import Iterator


async def list(client):
    return await client.request(
        'GET', f'{client.url_prefix}/_api/database')

async def list_for_user(client, user):
    return await client._session.request(
        'GET',
        f'{client.url_prefix}/_api/user/{user}/database/')

async def current(client):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/database/current')

async def create(client, name: str, *, users: Iterator[dict]=None):
    json = {'name': name}
    if isinstance(users, Iterator):
        json['users'] = [*users]
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/database', json=json)

async def delete(client, name: str):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/database/{name}')

async def collection_list(client, exclude_system: bool=None):
    return await client._session.request(
        'GET',
        f'{client.url_prefix}/_api/collection',
        params={'excludeSystem': bool(exclude_system)})

async def collection_create(client, json: dict):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/collection', json=json)

async def collection_load(client, name, *, count=None, type=None):
    json = {'count': bool(count)}
    if type in [2, 3] or type == [2, 3]:
        json['type'] = type
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{name}/load', json=json)

async def collection_unload(client, name):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{name}/unload')

async def collection_rename(client, name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{name}/rename', **kwargs)

async def collection_rotate(client, name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{name}/rotate', **kwargs)

async def collection_size(client, name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{name}/count', **kwargs)

async def collection_stats(client, name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{name}/figures', **kwargs)

async def collection_revision(client, name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{name}/revision',
        **kwargs)

async def collection_checksum(client, name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{name}/checksum',
        **kwargs)

async def collection_truncate(client, name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{name}/truncate',
        **kwargs)

async def collection_delete(client, name, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/collection/{name}', **kwargs)

async def collection_props(client, name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{name}/properties',
        **kwargs)

async def collection_props_update(client, name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{name}/properties',
        **kwargs)

async def collection_load_indexes(client, name, **kwargs):
    return await client._session.request(
        'PUT',
        f'{client.url_prefix}/_api/collection/{name}/loadIndexesIntoMemory',
        **kwargs)

async def document(client, handle, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/document/{handle}', **kwargs)

async def document_create(client, collection, *, json: dict = None):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/document/{collection}', json=json)

async def document_update(client, handle, **kwargs):
    return await client._session.request(
        'PATCH', f'{client.url_prefix}/_api/document/{handle}', **kwargs)

async def document_replace(client, handle, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/document/{handle}', **kwargs)

async def document_header(client, handle, **kwargs):
    return await client._session.request(
        'HEAD', f'{client.url_prefix}/_api/document/{handle}', **kwargs)

async def document_delete(client, handle, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/document/{handle}', **kwargs)

async def index(client, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/index', **kwargs)

INDEX_TYPES = ['fulltext', 'general', 'geo', 'hash', 'persistent', 'skiplist']
async def index_create(client, type, **kwargs):
    if type not in INDEX_TYPES:
        raise ValueError(f'type must be one of {INDEX_TYPES}')
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/index#{type}', **kwargs)

async def index_delete(client, index_handle, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/index/{index_handle}', **kwargs)

async def import_document(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/import#document', **kwargs)


async def import_json(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/import#json', **kwargs)


async def export(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/export', **kwargs)


async def user(client, user, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/user/{user}', **kwargs)


async def user_list(client, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/user/', **kwargs)


async def user_create(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/user', **kwargs)


async def user_update(client, user, **kwargs):
    return await client._session.request(
        'PATCH', f'{client.url_prefix}/_api/user/{user}', **kwargs)


async def user_replace(client, user, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/user/{user}', **kwargs)


async def user_delete(client, user, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/user/{user}', **kwargs)


async def user_database(client, user, database, collection, **kwargs):
    return await client._session.request(
        'GET',
        f'{client.url_prefix}/_api/user/{user}/database/{database}/{collection}',
        **kwargs)



async def user_access_update(client, user, db_name, collection, **kwargs):
    return await client._session.request(
        'PUT',
        f'{client.url_prefix}/_api/user/{user}/database/{db_name}/{collection}',
        **kwargs)


async def user_access_clear(client, user, db_name, collection, **kwargs):
    return await client._session.request(
        'DELETE',
        f'{client.url_prefix}/_api/user/{user}/database/{db_name}/{collection}',
        **kwargs)
