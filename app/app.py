import hashlib
import logging
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_swagger import *

from routes import routes


logging.basicConfig(level=logging.DEBUG)

SECRET_KEY = 'veryStrongSecretKey'


middle = [
    session_middleware(EncryptedCookieStorage(hashlib.sha256(bytes(SECRET_KEY, 'utf-8')).digest())),
]
app = web.Application(middlewares=middle)


for route in routes:
    app.router.add_route(route[0], route[1], route[2], name=route[3])

if __name__ == '__main__':
    setup_swagger(app, swagger_from_file="swagger.yaml")
    web.run_app(app)
