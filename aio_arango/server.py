async def shutdown(client, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_admin/shutdown", **kwargs)


async def log(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/log", **kwargs)


async def log_level(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/log/level", **kwargs)


async def log_level_update(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_admin/log/level", **kwargs)


async def aqlfunction(client, **kwargs):
    return await client._session.request(
        'GET', f'{client.url_prefix}/_api/aqlfunction', **kwargs)


async def aqlfunction_create(client, **kwargs):
    return await client._session.request(
        'POST', f'{client.url_prefix}/_api/aqlfunction', **kwargs)


async def aqlfunction_delete(client, name, **kwargs):
    return await client._session.request(
        'DELETE', f'{client.url_prefix}/_api/aqlfunction/{name}', **kwargs)


async def test(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_admin/test", **kwargs)


async def echo(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/echo", **kwargs)


async def execute(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_admin/execute", **kwargs)


async def status(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/status", **kwargs)


async def time(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/time", **kwargs)

async def job(client, job_id, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/job/{job_id}", **kwargs)

async def job_cancel(client, job_id, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/job/{job_id}/cancel", **kwargs)

async def job_delete(client, type, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/job/{type}", **kwargs)

async def job_get(client, job_id, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/job/{job_id}", **kwargs)

async def job_list(client, type, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/job/{type}", **kwargs)

async def tasks(client, id, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/tasks/{id}", **kwargs)

async def tasks_create(client, id, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/tasks/{id}", **kwargs)

async def tasks_delete(client, id, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/tasks/{id}", **kwargs)


async def wal_flush(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_admin/wal/flush", **kwargs)


async def wal_properties(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/wal/properties", **kwargs)


async def wal_properties_configure(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_admin/wal/properties", **kwargs)


async def wal_transactions(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/wal/transactions", **kwargs)


async def routing_reload(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_admin/routing/reload", **kwargs)


async def statistics(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/statistics", **kwargs)


async def _get(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/statistics-description", **kwargs)


async def server_role(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/server/role", **kwargs)


async def server_id(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/server/id", **kwargs)


async def server_availability(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/server/availability", **kwargs)


async def cluster_statistics(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/clusterStatistics", **kwargs)


async def cluster_endpoints(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/cluster/endpoints", **kwargs)


async def cluster_health(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_admin/cluster/health", **kwargs)


async def cluster_check_port(client, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_admin/clusterCheckPort",
        **kwargs)


async def cluster_test(client, method, json: dict = None):
    if json is None:
        json = {'key': 'value'}
    return await client._session.request(
        method, f"{client.url_prefix}/_admin/cluster-test", json=json)

async def replication(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/replication/applier-state", **kwargs)


async def replication_inventory(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/replication/inventory", **kwargs)


async def replication_batch(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/replication/batch", **kwargs)


async def replication_batch_delete(client, id, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/replication/batch/{id}", **kwargs)


async def replication_batch_prolong(client, id, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/replication/batch/{id}", **kwargs)


async def replication_dump(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/replication/dump", **kwargs)


async def replication_sync(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/replication/sync", **kwargs)


async def replication_cluster_inventory(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/replication/clusterInventory", **kwargs)


async def replication_put(client, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/replication/make-slave", **kwargs)
