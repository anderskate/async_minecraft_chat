import asyncio
import aiofiles
import datetime
import argparse


async def save_data_to_log_file(data, file_path):
    """Save data to a log file with date and time"""

    async with aiofiles.open(file_path, mode='a') as f:
        current_datetime = datetime.datetime.now()
        formatting_current_datetime = current_datetime.strftime(
            "%d.%m.%y %H:%M"
        )
        log_data = f'[{formatting_current_datetime}] {data} \n'
        await f.write(log_data)


async def echo_client_messages_from_chat(host, port, history_path):
    """Show messages from chat"""
    await save_data_to_log_file('Установлено соединение', history_path)
    while True:
        reader, writer = await asyncio.open_connection(
            host,
            port,
        )

        data = await reader.readline()
        await save_data_to_log_file(data.decode(), history_path)
        print(data.decode())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Program for streaming and logging messages in chat'
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
        default=5000
    )
    parser.add_argument(
        '--history',
        help='The path to the file with the storage of messages',
        default='log.txt'
    )
    args = parser.parse_args()
    host = args.host
    port = args.port
    history_path = args.history

    asyncio.run(echo_client_messages_from_chat(host, port, history_path))
