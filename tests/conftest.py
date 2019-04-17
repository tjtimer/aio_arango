"""
conftest
author: Tim "tjtimer" Jedro
created: 24.10.18
"""
import string

import pytest

from aio_arango.client import ArangoAdmin
from aio_arango.db import ArangoDB, DocumentType

alphabet = [*string.ascii_letters, string.digits, '-', '_']


@pytest.fixture
async def test_db(loop):
    async with ArangoAdmin('root', 'arango-pw') as admin:
        await admin.create_db('test-db')
        async with ArangoDB('root', 'arango-pw', 'test-db') as db:
            yield db
        await admin.delete_db('test-db')


@pytest.fixture
async def graph_db(loop):
    async with ArangoAdmin('root', 'arango-pw') as admin:
        if 'graph-db' in admin.databases:
            await admin.delete_db('graph-db')
        await admin.create_db('graph-db')
        async with ArangoDB('root', 'arango-pw', 'graph-db') as db:
            await db.create_collection('person')
            await db.create_collection('bike')
            await db.create_collection('knows', doc_type=DocumentType.EDGE)
            await db.create_collection('rides', doc_type=DocumentType.EDGE)
            await db.create_graph(
                'knows_n_rides',
                [{'collection': 'knows', 'from': ['person'], 'to': ['person']},
                 {'collection': 'rides', 'from': ['person'], 'to': ['bike']}]
            )
            yield db
        await admin.delete_db('graph-db')
