import asyncio
import logging
import json
import argparse
from get_connection import get_connection


logger = logging.getLogger(__file__)


class UnknownTokenException(Exception):
    """Called when user token is unknown."""
    pass


async def submit_message(reader, writer, message):
    """Submit message to chat."""
    data = await reader.readline()
    logger.info(data)

    formatted_message = message.replace('\n', '')
    writer.write(f'{formatted_message}\n\n'.encode())
    await writer.drain()

    data = await reader.readline()
    logger.info(data)


async def authorise(reader, writer, account_hash):
    """Login to chat with user account hash.

    If account_hash is incorrect, it return an error,
    if correct, it return user credentials.
    """
    data = await reader.readline()
    logger.info(data)

    writer.write(f'{account_hash}\n'.encode())
    await writer.drain()

    credentials = await reader.readline()
    logger.info(credentials)

    if json.loads(credentials) is None:
        raise UnknownTokenException(
            'Неизвестный токен. '
            'Проверьте его или зарегистрируйте заново.'
            )

    return credentials


async def register(host, port, nickname):
    """Register a new user in the chat and get a account_hash."""

    async with get_connection(host, port) as connection:
        reader, writer = connection

        data = await reader.readline()
        logger.info(data)

        writer.write('\n'.encode())
        await writer.drain()

        data = await reader.readline()
        logger.info(data)

        formatted_nickname = nickname.replace('\n', '')
        writer.write(f'{formatted_nickname}\n'.encode())
        await writer.drain()

        data = await reader.readline()
        logger.info(data)
        user_credentials = json.loads(data)
        account_hash = user_credentials.get('account_hash')

        writer.close()
        await writer.wait_closed()

        return account_hash


async def main():
    """Main function from which the necessary components are launched.

    Configure logging, parsing incoming user data, 
    as well as a function for sending a user message.
    """
    logging.basicConfig(
        format='%(levelname)s:sender:%(message)s',
        level=logging.DEBUG,
    )

    parser = argparse.ArgumentParser(
        description='Program for authorization and sending messages in chat'
    )
    parser.add_argument(
        '--host',
        help='Host to connect',
        default='minechat.dvmn.org'
    )
    parser.add_argument(
        '--port',
        help='Port to connect',
        type=int,
        default=5050
    )
    parser.add_argument(
        '--token',
        help='Authorization token',
        default=None
    )
    parser.add_argument(
        '--username',
        help='Username for register a new user',
        default=''
    )
    parser.add_argument(
        '--message',
        help='Message for chat',
        required=True
    )
    args = parser.parse_args()
    host = args.host
    port = args.port
    token = args.token
    username = args.username
    message = args.message
    
    async with get_connection(host, port) as connection:
        reader, writer = connection

        if not token:
            token = await register(host, port, username)
        await authorise(reader, writer, token)
        await submit_message(reader, writer, message)


if __name__ == '__main__':
    asyncio.run(
        main()
    )
