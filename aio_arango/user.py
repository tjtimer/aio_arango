async def user(client, user, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/user/{user}", **kwargs)


async def user_list(client, **kwargs):
    return await client._session.request(
        "GET", f"{client.url_prefix}/_api/user/", **kwargs)


async def user_create(client, **kwargs):
    return await client._session.request(
        "POST", f"{client.url_prefix}/_api/user", **kwargs)


async def user_update(client, user, **kwargs):
    return await client._session.request(
        "PATCH", f"{client.url_prefix}/_api/user/{user}", **kwargs)


async def user_replace(client, user, **kwargs):
    return await client._session.request(
        "PUT", f"{client.url_prefix}/_api/user/{user}", **kwargs)


async def user_delete(client, user, **kwargs):
    return await client._session.request(
        "DELETE", f"{client.url_prefix}/_api/user/{user}", **kwargs)


async def user_database(client, user, database, collection, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_api/user/{user}/database/{database}/{collection}",
        **kwargs)


async def user_database_list(client, user, **kwargs):
    return await client._session.request(
        "GET",
        f"{client.url_prefix}/_api/user/{user}/database/",
        **kwargs)


async def user_database_change(client, user, db_name, collection, **kwargs):
    return await client._session.request(
        "PUT",
        f"{client.url_prefix}/_api/user/{user}/database/{db_name}/{collection}",
        **kwargs)


async def user_database_delete(client, user, db_name, collection, **kwargs):
    return await client._session.request(
        "DELETE",
        f"{client.url_prefix}/_api/user/{user}/database/{db_name}/{collection}",
        **kwargs)
