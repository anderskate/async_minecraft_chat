import asyncio
import logging
import json


logging.basicConfig(
    format='%(levelname)s:sender:%(message)s',
    level=logging.DEBUG,
)


async def login_to_chat(user_token):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org',
        5050,
    )
    print('Authenticate in chat')
    token = user_token + '\n'
    writer.write(token.encode())
    await writer.drain()

    while True:
        data = await reader.readline()
        formatted_data = data.decode().strip()

        if formatted_data == 'null':
            assert json.loads(formatted_data) is not None, \
                'Неизвестный токен. ' \
                'Проверьте его или зарегистрируйте заново.'

        logging.debug(formatted_data)

        writer.write('Hello, I Andrew!!!!\n\n'.encode())
        await writer.drain()


async def register(host, port):
    """Register a new user in the chat and get a token"""
    reader, writer = await asyncio.open_connection(
        host,
        port,
    )
    writer.write('\n\n'.encode())
    await writer.drain()

    while True:
        data = await reader.readline()
        try:
            user_credentials = json.loads(data)
            account_hash = user_credentials.get('account_hash')

            writer.close()
            await writer.wait_closed()

            return account_hash

        except json.decoder.JSONDecodeError:
            logging.warning('Invalid format to json')


if __name__ == '__main__':
    # asyncio.run(login_to_chat(''))
    asyncio.run(register('minechat.dvmn.org', 5050))
