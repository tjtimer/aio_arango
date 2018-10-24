"""
document
author: Tim "tjtimer" Jedro
created: 24.10.18
"""

URL = '_api/document'


async def get(client, handle):
    return await client.request('GET', f'{URL}/{handle}')


async def create(client, collection, *, data: dict or list = None):
    await client.request('POST', f'{URL}/{collection}', data)


async def update(client, handle, data: dict):
    return await client.request('PATCH', f'{URL}/{handle}', data)


async def replace(client, handle, data: dict):
    return await client.request('PUT', f'{URL}/{handle}', data)


async def delete(client, handle):
    return await client.request('DELETE', f'{URL}/{handle}')


async def header(client, handle):
    return await client.request('HEAD', f'{URL}/{handle}')
