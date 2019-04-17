"""
conftest
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
import string

import pytest

from aio_arango.client import ArangoAdmin
from aio_arango.db import ArangoDB

alphabet = [*string.ascii_letters, string.digits, '-', '_']


@pytest.fixture
async def test_db(loop):
    async with ArangoAdmin('root', 'arango-pw') as admin:
        await admin.create_db('test-db')
        async with ArangoDB('root', 'arango-pw', 'test-db') as db:
            yield db
        await admin.delete_db('test-db')
