# aio_arango client
# created: 01.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import asyncio
import typing
from pprint import pprint

import aiohttp


class ArangoClient:
    def __init__(self,
                 address: typing.Tuple[str, int]=None,
                 path: str=None,
                 db_name: str = None,
                 loop: asyncio.AbstractEventLoop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        if path is None:
            con = aiohttp.TCPConnector(loop=loop)
            if address is None:
                address = ('localhost', 8529)
            self._address = address
            self._url_prefix = f'http://{address[0]}:{address[1]}'
            self._path = None
        else:
            con = aiohttp.UnixConnector(path=path, loop=loop)
            self._path = path
            self._address = None
            self._url_prefix = ''
        self._loop = loop
        self._connector = con
        self._auth_token = None
        self._session = None
        self.headers = {'Content-Type': 'application/json'}
        self.db_name = db_name

    @property
    def url_prefix(self):
        if self.db_name is None:
            return self._url_prefix
        return f'{self._url_prefix}/_db/{self.db_name}'

    async def login(self, username: str, password: str):
        self._session = aiohttp.ClientSession(
            connector=self._connector)
        resp = await self._session.request(
                'POST',
                self.url_prefix + '/_open/auth',
                json={'username': username, 'password': password}
        )
        data = await resp.json()
        if resp.status < 300:
            self._auth_token = data['jwt']
            self.headers['Authorization'] = f'bearer {self._auth_token}'
            self._session._default_headers.update(**self.headers)
        return data

    async def close(self):
        await self._session.close()

    async def database(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/database", **kwargs)

    async def database_current(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/database/current", **kwargs)

    async def database_user(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/database/user", **kwargs)

    async def database_create(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/database", **kwargs)

    async def database_delete(self, database_name, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/database/{database_name}", **kwargs)

    async def user(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/user", **kwargs)

    async def user_database(self, user, dbname, collection, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/user/{user}/database/{dbname}/{collection}",
            **kwargs)

    async def user_database_delete(self, user, dbname, collection, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/user/{user}/database/{dbname}/{collection}",
            **kwargs)

    async def user_database_list(self, user, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/user/{user}/database/", **kwargs)

    async def user_database_get(self, user, database, collection, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/user/{user}/database/{database}/{collection}",
            **kwargs)

    async def user_replace(self, user, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/user/{user}", **kwargs)

    async def user_update(self, user, **kwargs):
        return await self._session.request(
            "PATCH", f"{self.url_prefix}/_api/user/{user}", **kwargs)

    async def user_delete(self, user, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/user/{user}", **kwargs)

    async def user_get(self, user, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/user/{user}", **kwargs)

    async def user_list(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/user/", **kwargs)

    async def collection(self, exclude_system=None):
        excl_sys = 0 if exclude_system is None else 1
        return await self._session.request(
            "GET",
            f"{self.url_prefix}/_api/collection",
            params={'excludeSystem': excl_sys})

    async def collection_create(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/collection", **kwargs)

    async def collection_load(self, collection_name, *, count=None, type=None):
        json = {'count': True if count is None else count}
        if type in [2, 3] or type == [2, 3]:
            json['type'] = type
        print(json)
        pprint(vars(self))
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/collection/{collection_name}/load", json=json)

    async def collection_unload(self, collection_name):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/collection/{collection_name}/unload")

    async def collection_load_indexes_into_memory(self, collection_name, **kwargs):
        return await self._session.request(
            "PUT",
            f"{self.url_prefix}/_api/collection/{collection_name}/loadIndexesIntoMemory",
            **kwargs)

    async def collection_properties(self, collection_name, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/collection/{collection_name}/properties",
            **kwargs)

    async def collection_properties_update(self, collection_name, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/collection/{collection_name}/properties",
            **kwargs)

    async def collection_rename(self, collection_name, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/collection/{collection_name}/rename", **kwargs)

    async def collection_rotate(self, collection_name, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/collection/{collection_name}/rotate", **kwargs)

    async def collection_count(self, collection_name, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/collection/{collection_name}/count", **kwargs)

    async def collection_figures(self, collection_name, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/collection/{collection_name}/figures", **kwargs)

    async def collection_revision(self, collection_name, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/collection/{collection_name}/revision",
            **kwargs)

    async def collection_checksum(self, collection_name, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/collection/{collection_name}/checksum",
            **kwargs)

    async def collection_truncate(self, collection_name, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/collection/{collection_name}/truncate",
            **kwargs)

    async def collection_delete(self, collection_name, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/collection/{collection_name}", **kwargs)

    async def document(self, document_handle, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/document/{document_handle}", **kwargs)

    async def document_head(self, document_handle, **kwargs):
        return await self._session.request(
            "HEAD", f"{self.url_prefix}/_api/document/{document_handle}", **kwargs)

    async def document_create(self, document_handle, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/document/{document_handle}", **kwargs)

    async def document_update(self, document_handle, **kwargs):
        return await self._session.request(
            "PATCH", f"{self.url_prefix}/_api/document/{document_handle}", **kwargs)

    async def document_replace(self, document_handle, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/document/{document_handle}", **kwargs)

    async def document_delete(self, document_handle, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/document/{document_handle}", **kwargs)

    async def edges(self, collection_id, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/edges/{collection_id}", **kwargs)

    async def graph(self, graph_name, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/gharial/{graph_name}", **kwargs)

    async def graph_create(self, *,
                           name: str=None, edge_def: dict=None,
                           orph: list=None):
        json={'name': name, 'edgeDefinition': edge_def}
        if isinstance(orph, list):
            json['orphanCollections'] = orph
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/gharial", json=json)

    async def graph_delete(self, graph_name, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/gharial/{graph_name}", **kwargs)

    async def graph_vertex(self, graph_name, collection_name, vertex_key, **kwargs):
        return await self._session.request(
            "GET",
            f"{self.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def graph_vertex_create(self, graph_name, collection_name, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}",
            **kwargs)

    async def graph_vertex_update(self, graph_name, collection_name, vertex_key, **kwargs):
        return await self._session.request(
            "PATCH",
            f"{self.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def graph_vertex_replace(self, graph_name, collection_name, vertex_key, **kwargs):
        return await self._session.request(
            "PUT",
            f"{self.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def graph_vertex_delete(self, graph_name, collection_name, vertex_key, **kwargs):
        return await self._session.request(
            "DELETE",
            f"{self.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
            **kwargs)

    async def graph_edge(self, graph_name, collection_name, edge_key, **kwargs):
        return await self._session.request(
            "GET",
            f"{self.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def graph_edge_create(self, graph_name, collection_name, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}",
            **kwargs)

    async def graph_edge_update(self, graph_name, collection_name, edge_key, **kwargs):
        return await self._session.request(
            "PATCH",
            f"{self.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def graph_edge_replace(self, graph_name, collection_name, edge_key, **kwargs):
        return await self._session.request(
            "PUT",
            f"{self.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def graph_edge_delete(self, graph_name, collection_name, edge_key, **kwargs):
        return await self._session.request(
            "DELETE",
            f"{self.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
            **kwargs)

    async def cursor(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/cursor", **kwargs)

    async def cursor_next(self, cursor_identifier, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/cursor/{cursor_identifier}", **kwargs)

    async def cursor_delete(self, cursor_identifier, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/cursor/{cursor_identifier}", **kwargs)

    async def import_document(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/import#document", **kwargs)

    async def import_json(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/import#json", **kwargs)

    async def export(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/export", **kwargs)

    async def job(self, job_id, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/job/{job_id}", **kwargs)

    async def job_cancel(self, job_id, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/job/{job_id}/cancel", **kwargs)

    async def job_delete(self, type, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/job/{type}", **kwargs)

    async def job_get(self, job_id, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/job/{job_id}", **kwargs)

    async def job_list(self, type, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/job/{type}", **kwargs)

    async def traversal(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/traversal", **kwargs)

    async def query(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/query", **kwargs)

    async def query_explain(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/explain", **kwargs)

    async def query_properties(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/query/properties", **kwargs)

    async def query_properties_change(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/query/properties", **kwargs)

    async def query_current(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/query/current", **kwargs)

    async def query_slow(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/query/slow", **kwargs)

    async def query_slow_delete(self, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/query/slow", **kwargs)

    async def query_delete(self, query_id, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/query/{query_id}", **kwargs)

    async def query_cache_properties(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/query-cache/properties", **kwargs)

    async def query_cache_properties_update(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/query-cache/properties", **kwargs)

    async def tasks(self, id, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/tasks/{id}", **kwargs)

    async def tasks_create(self, id, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/tasks/{id}", **kwargs)

    async def tasks_delete(self, id, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/tasks/{id}", **kwargs)

    async def transaction(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/transaction", **kwargs)

    async def version(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/version", **kwargs)

    async def engine(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/engine", **kwargs)

    async def simple(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/first_example", **kwargs)

    async def simple_all(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/all", **kwargs)

    async def simple_any(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/any", **kwargs)

    async def simple_range(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/range", **kwargs)

    async def simple_near(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/near", **kwargs)

    async def simple_within(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/within", **kwargs)

    async def simple_fulltext(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/simple/fulltext", **kwargs)

    async def index(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/index", **kwargs)

    async def index_general(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/index#general", **kwargs)

    async def index_hash(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/index#hash", **kwargs)

    async def index_persistent(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/index#persistent", **kwargs)

    async def index_fulltext(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/index#fulltext", **kwargs)

    async def index_skiplist(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/index#skiplist", **kwargs)

    async def index_geo(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/index#geo", **kwargs)

    async def index_delete(self, index_handle, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/index/{index_handle}", **kwargs)

    async def batch(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/batch", **kwargs)

    async def aqlfunction(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/aqlfunction", **kwargs)

    async def aqlfunction_create(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/aqlfunction", **kwargs)

    async def aqlfunction_delete(self, name, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/aqlfunction/{name}", **kwargs)

    # root user only!
    async def shutdown(self, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_admin/shutdown", **kwargs)

    async def test(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_admin/test", **kwargs)

    async def execute(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_admin/execute", **kwargs)

    async def echo(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/echo", **kwargs)

    async def status(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/status", **kwargs)

    async def time(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/time", **kwargs)

    async def wal_flush(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_admin/wal/flush", **kwargs)

    async def wal_properties(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/wal/properties", **kwargs)

    async def wal_properties_configure(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_admin/wal/properties", **kwargs)

    async def wal_transactions(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/wal/transactions", **kwargs)

    async def log(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/log", **kwargs)

    async def log_level(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/log/level", **kwargs)

    async def log_level_update(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_admin/log/level", **kwargs)

    async def routing_reload(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_admin/routing/reload", **kwargs)

    async def statistics(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/statistics", **kwargs)

    async def _get(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/statistics-description", **kwargs)

    async def server_role(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/server/role", **kwargs)

    async def server_id(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/server/id", **kwargs)

    async def server_availability(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/server/availability", **kwargs)

    async def cluster_statistics(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/clusterStatistics", **kwargs)

    async def cluster_endpoints(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/cluster/endpoints", **kwargs)

    async def cluster_health(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/cluster/health", **kwargs)

    async def cluster_check_port(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_admin/clusterCheckPort", **kwargs)

    async def cluster_test(self, method, json:dict=None):
        if json is None:
            json = {'key': 'value'}
        return await self._session.request(
            method, f"{self.url_prefix}/_admin/cluster-test", dict)

    async def replication(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/replication/applier-state", **kwargs)

    async def replication_inventory(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/replication/inventory", **kwargs)

    async def replication_batch(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/replication/batch", **kwargs)

    async def replication_batch_delete(self, id, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/replication/batch/{id}", **kwargs)

    async def replication_batch_prolong(self, id, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/replication/batch/{id}", **kwargs)

    async def replication_dump(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/replication/dump", **kwargs)

    async def replication_sync(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/replication/sync", **kwargs)

    async def replication_cluster_inventory(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/replication/clusterInventory", **kwargs)

    async def replication_put(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/replication/make-slave", **kwargs)

"""
    async def foxx(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx", **kwargs)

    async def foxx_configuration(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx/configuration", **kwargs)

    async def foxx_configuration_update(self, **kwargs):
        return await self._session.request(
            "PATCH", f"{self.url_prefix}/_api/foxx/configuration", **kwargs)

    async def foxx_configuration_replace(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/foxx/configuration", **kwargs)

    async def foxx_dependencies(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx/dependencies", **kwargs)

    async def foxx_dependencies_update(self, **kwargs):
        return await self._session.request(
            "PATCH", f"{self.url_prefix}/_api/foxx/dependencies", **kwargs)

    async def foxx_dependencies_replace(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/foxx/dependencies", **kwargs)

    async def foxx_service(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx/service", **kwargs)

    async def foxx_service_install(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/foxx", **kwargs)

    async def foxx_service_uninstall(self, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/foxx/service", **kwargs)

    async def foxx_service_replace(self, **kwargs):
        return await self._session.request(
            "PUT", f"{self.url_prefix}/_api/foxx/service", **kwargs)

    async def foxx_service_update(self, **kwargs):
        return await self._session.request(
            "PATCH", f"{self.url_prefix}/_api/foxx/service", **kwargs)

    async def foxx_scripts(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx/scripts", **kwargs)

    async def foxx_scripts_post(self, name, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/foxx/scripts/{name}", **kwargs)

    async def foxx_tests(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/foxx/tests", **kwargs)

    async def foxx_development(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/foxx/development", **kwargs)

    async def foxx_development_delete(self, **kwargs):
        return await self._session.request(
            "DELETE", f"{self.url_prefix}/_api/foxx/development", **kwargs)

    async def foxx_readme(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx/readme", **kwargs)

    async def foxx_swagger(self, **kwargs):
        return await self._session.request(
            "GET", f"{self.url_prefix}/_api/foxx/swagger", **kwargs)

    async def foxx_download(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/foxx/download", **kwargs)

    async def foxx_commit(self, **kwargs):
        return await self._session.request(
            "POST", f"{self.url_prefix}/_api/foxx/commit", **kwargs)

"""
