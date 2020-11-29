import asyncio
import aiofiles
import datetime


async def save_data_to_log_file(data):
    """Save data to a log file with date and time"""
    async with aiofiles.open('log.txt', mode='a') as f:
        current_datetime = datetime.datetime.now()
        formatting_current_datetime = current_datetime.strftime(
            "%d.%m.%y %H:%M"
        )
        log_data = f'[{formatting_current_datetime}] {data} \n'
        await f.write(log_data)


async def echo_client_messages_from_chat():
    """Show messages from chat"""
    await save_data_to_log_file('Установлено соединение')
    while True:
        reader, writer = await asyncio.open_connection(
            'minechat.dvmn.org',
            5000,
        )

        data = await reader.readline()
        await save_data_to_log_file(data.decode())
        print(data.decode())


if __name__ == '__main__':
    asyncio.run(echo_client_messages_from_chat())

