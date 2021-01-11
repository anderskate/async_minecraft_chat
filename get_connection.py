from contextlib import asynccontextmanager
import asyncio
import socket
import logging


logger = logging.getLogger(__file__)


def chat_is_available(host, port):
    """Check the chat connection for the given host and port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        # Shutdown both halves of the connection
        s.shutdown(2)
        return True
    except socket.gaierror:
        return False


@asynccontextmanager
async def get_connection(host, port, timeout=10):
    """Get reader and writer objects.

    At the end of the work, be sure to close the writer object connection.
    """

    while not chat_is_available(host, port):
        chat_is_available(host, port)

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
