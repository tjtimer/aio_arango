async def graph(client, graph_name, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/gharial/{graph_name}", **kwargs)


async def graph_create(client, *,
                       name: str = None, edge_def: dict = None,
                       orph: list = None):
    json = {'name': name, 'edgeDefinition': edge_def}
    if isinstance(orph, list):
        json['orphanCollections'] = orph
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/gharial", json=json)


async def graph_delete(client, graph_name, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/gharial/{graph_name}", **kwargs)


async def graph_vertex(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def graph_vertex_create(client, graph_name, collection_name, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}",
        **kwargs)


async def graph_vertex_update(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "PATCH",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def graph_vertex_replace(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "PUT",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def graph_vertex_delete(client, graph_name, collection_name, vertex_key, **kwargs):
    return await client._session.request(
        "DELETE",
        f"{client.url_prefix}/_api/gharial/{graph_name}/vertex/{collection_name}/{vertex_key}",
        **kwargs)


async def graph_edge(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)


async def graph_edge_create(client, graph_name, collection_name, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}",
        **kwargs)


async def graph_edge_update(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "PATCH",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)


async def graph_edge_replace(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "PUT",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)


async def graph_edge_delete(client, graph_name, collection_name, edge_key, **kwargs):
    return await client._session.request(
        "DELETE",
        f"{client.url_prefix}/_api/gharial/{graph_name}/edge/{collection_name}/{edge_key}",
        **kwargs)

