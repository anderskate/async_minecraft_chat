import asyncio


async def login_to_chat():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org',
        5050,
    )
    print('Authenticate in chat')
    token = 'your_token\n'
    writer.write(token.encode())
    await writer.drain()

    while True:
        data = await reader.readline()
        print(f'Received: {data.decode()!r}')

        writer.write('Hello, I Andrew!!!!\n\n'.encode())
        await writer.drain()

if __name__ == '__main__':
    asyncio.run(login_to_chat())
