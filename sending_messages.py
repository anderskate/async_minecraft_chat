import asyncio
import logging
import json


logging.basicConfig(
    format='%(levelname)s:sender:%(message)s',
    level=logging.DEBUG,
)


async def submit_message(reader, writer, message):
    """Submit message to chat"""
    data = await reader.readline()
    logging.info(data)

    writer.write(f'{message}\n\n'.encode())
    await writer.drain()

    data = await reader.readline()
    logging.info(data)


async def authorise(reader, writer, account_hash):
    """Login to chat with user account hash

    If account_hash is incorrect, it return an error,
    if correct, it return user credentials
    """
    data = await reader.readline()
    logging.info(data)

    writer.write(f'{account_hash}\n'.encode())
    await writer.drain()

    credentials = await reader.readline()
    logging.info(credentials)

    assert json.loads(credentials) is not None, \
        'Неизвестный токен. ' \
        'Проверьте его или зарегистрируйте заново.'

    return credentials


async def register(reader, writer, nickname):
    """Register a new user in the chat and get a account_hash"""
    data = await reader.readline()
    logging.info(data)

    writer.write('\n'.encode())
    await writer.drain()

    data = await reader.readline()
    logging.info(data)

    writer.write(f'{nickname}\n'.encode())
    await writer.drain()

    data = await reader.readline()
    logging.info(data)
    user_credentials = json.loads(data)
    account_hash = user_credentials.get('account_hash')

    writer.close()
    await writer.wait_closed()

    return account_hash


async def main():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org',
        5050,
    )
    await authorise(reader, writer, '')
    await submit_message(reader, writer, 'Привет всем!!!!')


if __name__ == '__main__':
    asyncio.run(main())
