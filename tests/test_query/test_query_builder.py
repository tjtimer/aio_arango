"""
test_query_builder
author: Tim "tjtimer" Jedro
created: 31.10.18
"""
from aio_arango.query import QueryBuilder


def test_builder_simple():
    q = QueryBuilder()
    q.for_in('u', 'users')
    assert 'FOR u IN users' == q.statement
    q.for_in('u2', 'users')
    assert 'FOR u IN users FOR u2 IN users' == q.statement
    q.filter().eq('u._id', 'u2._id')
    assert 'FOR u IN users FOR u2 IN users FILTER u._id == u2._id' == q.statement
