from contextlib import asynccontextmanager
import asyncio
import socket
import requests
import logging


logger = logging.getLogger(__file__)


def chat_is_available(host, port):
    """Check the chat connection for the given host and port."""
    try:
        response = requests.get(f'http://{host}:{port}')
        return True
    except requests.exceptions.ConnectionError:
        return False


@asynccontextmanager
async def get_connection(host, port, timeout=0):
    """Get reader and writer objects.

    At the end of the work, be sure to close the writer object connection.
    """

    while not chat_is_available(host, port):
        chat_is_available(host, port)

        # After an unsuccessful chat connection, 
        # add another 10 seconds of timeout.
        timeout += 10

        logger.warning(
            f'No chat connection. Reconnect after {timeout} seconds.'
            )
        await asyncio.sleep(timeout)

    reader, writer = await asyncio.open_connection(
            host,
            port,
        )

    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()
