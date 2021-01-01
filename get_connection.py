from contextlib import asynccontextmanager
import asyncio
import socket


@asynccontextmanager
async def get_connection(host, port):
    """Get reader and writer objects.

    At the end of the work, be sure to close the writer object connection.
    """
    reader, writer = await asyncio.open_connection(
        host,
        port,
    )
    
    try:
        yield reader, writer
    finally:
        writer.close()
        await writer.wait_closed()
