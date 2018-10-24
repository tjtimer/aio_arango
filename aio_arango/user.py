"""
user
author: Tim "tjtimer" Jedro
created: 23.10.18
"""
from typing import Optional, Generator

from client import ArangoClient, ClientError, AccessLevel

URL = '{URL}'


async def create(client: ArangoClient,
                 name: str, password: str, *,
                 extra: dict=None, active: bool=None):
    data = dict(user=name, password=password)
    if isinstance(extra, dict):
        data['extra'] = extra
    if active is None:
        active = True
    data['active'] = active
    await client.request('POST', URL, data)


async def update(client: ArangoClient, name: str, data: dict):
    await client.request('PATCH', f'{URL}/{name}', data)
    # resp_data = await resp.json()
    # return {k: v for k, v in resp_data
    #         if k in ['user', 'active', 'extra', 'password']}


async def replace(client: ArangoClient, name: str, data: dict):
    await client.request('PUT', f'{URL}/{name}', data)


async def delete(client: ArangoClient, name: str):
    await client.request('DELETE', f'{URL}/{name}')


async def available_dbs(client: ArangoClient, name: str)->Generator:
    resp = await client.request('GET', f'{URL}/{name}/database')
    return (db for db in (await resp.json())['result'])


async def get_access_level(client: ArangoClient, name: str, db_name: str,
                           col_name: Optional[str]=None)->AccessLevel:
    url = f'{URL}/{name}/database'
    handle = db_name
    if col_name:
        handle = f"{db_name}/{col_name}"
    resp = await client.request('GET', f"{url}/{handle}")
    return (await resp.json())[handle]


async def set_access_level(client: ArangoClient,
                           name: str, db_name: str, col_name: str,
                           level: AccessLevel):
    url = f'{URL}/{name}/database'
    handle = db_name
    if col_name:
        handle = f"{db_name}/{col_name}"
    await client.request('PUT', f"{url}/{handle}", data={'grant': level})


async def reset_access_level(client: ArangoClient, name: str, db_name: str, col_name: str):
    url = f'{URL}/{name}/database'
    handle = db_name
    if col_name:
        handle = f"{db_name}/{col_name}"
    await client.request('DELETE', f"{url}/{handle}")

