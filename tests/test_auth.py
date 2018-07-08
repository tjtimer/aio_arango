# aio_arango test_auth
# created: 04.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
async def test_auth(client, credentials):
    resp = await client.login(*credentials)
    assert client._auth_token == resp
    assert 'Authorization' in client._headers.keys()

