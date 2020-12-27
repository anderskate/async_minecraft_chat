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
            assert json.loads(f'{formatted_data}') is not None, \
                'Неизвестный токен. ' \
                'Проверьте его или зарегистрируйте заново.'

        logging.debug(formatted_data)

        writer.write('Hello, I Andrew!!!!\n\n'.encode())
        await writer.drain()

if __name__ == '__main__':
    asyncio.run(login_to_chat('my_token'))
