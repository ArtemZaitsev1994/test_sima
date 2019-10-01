import json
import pytest
import hashlib

from aiohttp import web, BasicAuth
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from routes import routes


SECRET_KEY = 'veryStrongSecretKey'

@pytest.fixture
def cli(loop, aiohttp_client):
    middle = [
        session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
    ]
    app = web.Application(middlewares=middle)
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    return loop.run_until_complete(aiohttp_client(app))


async def test_ping_server(cli):
    # пингуем сервер
    resp = await cli.get('/ping_server')
    assert resp.status == 200
    answer = json.loads(await resp.text())
    assert "pong" == answer['message']


async def test_auth_with_wrong_password(cli):
    # тест с неверным паролем
    auth_data = BasicAuth(login='login', password='wrong_pass')
    resp = await cli.get('/auth', auth=auth_data)
    assert resp.status == 401

async def test_auth_with_wrong_login(cli):
    # тест с неверным паролем
    auth_data = BasicAuth(login='wrong_login', password='password')
    resp = await cli.get('/auth', auth=auth_data)
    assert resp.status == 401

async def test_auth(cli):
    # авторизация с правильными данными
    auth_data = BasicAuth(login='login', password='password')
    resp = await cli.get('/auth', auth=auth_data)
    assert resp.status == 200
    answer = json.loads(await resp.text())
    assert "authed" == answer['message']
