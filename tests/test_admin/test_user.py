"""
test_create_db
author: Tim "tjtimer" Jedro
created: 31.10.18
"""
from aio_arango.client import ArangoAdmin


async def test_create_and_delete_user_valid():
    name = 'test-user'
    passwd = 'test-pw'
    async with ArangoAdmin('root', 'arango-pw') as admin:
        await admin.create_user(name, passwd)
        users = await admin.get_users()
        assert name in [usr['user'] for usr in users]
        await admin.delete_user(name)
        users = await admin.get_users()
        assert name not in [usr['user'] for usr in users]
