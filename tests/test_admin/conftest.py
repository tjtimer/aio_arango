"""
conftest.py
author: Tim "tjtimer" Jedro
created: 17.04.19
"""
import pytest

from aio_arango.client import ArangoAdmin


@pytest.fixture
async def admin(loop):
    async with ArangoAdmin('root', 'arango-pw') as db:
        yield db