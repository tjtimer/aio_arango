"""
test_create_db
author: Tim "tjtimer" Jedro
created: 31.10.18
"""


async def test_create_and_delete_db_valid(admin):
    name = 'test-tmp-db'
    assert name not in admin.databases
    await admin.create_db(name)
    assert name in admin.databases
    await admin.delete_db(name)
    assert name not in admin.databases
