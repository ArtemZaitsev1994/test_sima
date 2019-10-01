import aiohttp
import asyncio
import json

from typing import Any


COMMANDS = ('Ping server - 1\n'
            'Auth        - 2\n'
            'Exit        - 3\n'
            '---------------')

HOST = 'http://0.0.0.0:8080'


def print_answer(answer: Any):
    print(f'#------------------------#\n{answer}\n#------------------------#')


async def ping_server(session: aiohttp.ClientSession):
    try:
        async with session.get(f'{HOST}/ping_server') as req:
            if req.status == 200:
                data = json.loads(await req.text())
                print_answer(f'Server is available.\n{data["message"]}')
    except aiohttp.client_exceptions.ClientConnectorError:
        print_answer('Server is not available.')


async def auth(session: aiohttp.ClientSession) -> bool:
    async with session.get(f'{HOST}/auth') as req:
        if req.status == 200:
            data = json.loads(await req.text())
            print_answer(data["message"])
            return True
        elif req.status == 401:
            print_answer('Wrong login or password, try again.')
            return False


async def main():
    while True:
            # пытаемся установить сессию с верным логином и паролем
        login, password = input('\nEnter login: '), input('Enter password: ')
        auth_data = aiohttp.BasicAuth(login=login, password=password, encoding='utf-8')
        headers = {"Authorization": auth_data.encode()}
        async with aiohttp.ClientSession(headers=headers) as session:
            if not await auth(session):
                continue
            command = None
            # если сессия установлена, то доступны две команды:
            # пинг сервера и проверка авторизации
            while command != '3':
                print(f'\nAvailible commands:\n{COMMANDS}')
                command = input('Enter a number: ')
                if command == '1':
                    await ping_server(session)
                elif command == '2':
                    await auth(session)
            print('Bye!')
            break


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
