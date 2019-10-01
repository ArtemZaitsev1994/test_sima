from aiohttp import BasicAuth, web, hdrs
from aiohttp.web_request import Request
from aiohttp_session import get_session


LOGIN = 'login'
PASSWORD = 'password'


async def ping_server(request: Request):
    return web.json_response({'message': 'pong'})


async def auth(request: Request):
    session = await get_session(request)
    auth_header = request.headers.get(hdrs.AUTHORIZATION)
    data = BasicAuth.decode(auth_header=auth_header)
    if data.login == LOGIN and data.password == PASSWORD:
        return web.json_response({'message': 'authed'})
    return web.HTTPUnauthorized()
