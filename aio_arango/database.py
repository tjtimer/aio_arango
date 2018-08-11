async def list(client, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/database', **kwargs)

async def list_for_user(client, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/database/user', **kwargs)

async def current(client, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/database/current', **kwargs)

async def create(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/database', **kwargs)

async def delete(client, database_name, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/database/{database_name}', **kwargs)

async def collection(client, exclude_system=None):
    return await client._session.request(
        'GET',
        f'{client.url_prefix}/_api/collection',
        params={'excludeSystem': bool(exclude_system)})

async def collection_create(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/collection', **kwargs)

async def collection_load(client, collection_name, *, count=None, type=None):
    json = {'count': bool(count)}
    if type in [2, 3] or type == [2, 3]:
        json['type'] = type
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{collection_name}/load', json=json)

async def collection_unload(client, collection_name):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{collection_name}/unload')

async def collection_rename(client, collection_name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{collection_name}/rename', **kwargs)

async def collection_rotate(client, collection_name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{collection_name}/rotate', **kwargs)

async def collection_count(client, collection_name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{collection_name}/count', **kwargs)

async def collection_figures(client, collection_name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{collection_name}/figures', **kwargs)

async def collection_revision(client, collection_name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{collection_name}/revision',
        **kwargs)

async def collection_checksum(client, collection_name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{collection_name}/checksum',
        **kwargs)

async def collection_truncate(client, collection_name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{collection_name}/truncate',
        **kwargs)

async def collection_delete(client, collection_name, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/collection/{collection_name}', **kwargs)

async def collection_props(client, collection_name, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/collection/{collection_name}/properties',
        **kwargs)

async def collection_props_update(client, collection_name, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/collection/{collection_name}/properties',
        **kwargs)

async def collection_load_indexes(client, collection_name, **kwargs):
    return await client._session.request(
        'PUT',
        f'{client.url_prefix}/_api/collection/{collection_name}/loadIndexesIntoMemory',
        **kwargs)

async def document(client, document_handle, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/document/{document_handle}', **kwargs)

async def document_create(client, document_handle, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/document/{document_handle}', **kwargs)

async def document_update(client, document_handle, **kwargs):
    return await client._session.request(
        'PATCH', f'{client.url_prefix}/_api/document/{document_handle}', **kwargs)

async def document_replace(client, document_handle, **kwargs):
    return await client._session.request(
        'PUT', f'{client.url_prefix}/_api/document/{document_handle}', **kwargs)

async def document_header(client, document_handle, **kwargs):
    return await client._session.request(
        'HEAD', f'{client.url_prefix}/_api/document/{document_handle}', **kwargs)

async def document_delete(client, document_handle, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/document/{document_handle}', **kwargs)

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

