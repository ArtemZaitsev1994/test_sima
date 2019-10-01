from server import (
    ping_server,
    auth
)


routes = [
    ('GET', '/ping_server', ping_server, 'ping_server'),
    ('GET', '/auth', auth, 'auth')
]
