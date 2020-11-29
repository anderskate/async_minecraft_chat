import asyncio


async def echo_client_messages_from_chat():
    while True:
        reader, writer = await asyncio.open_connection(
            'minechat.dvmn.org',
            5000,
        )

        data = await reader.readline()
        print(data.decode())


if __name__ == '__main__':
    asyncio.run(echo_client_messages_from_chat())

