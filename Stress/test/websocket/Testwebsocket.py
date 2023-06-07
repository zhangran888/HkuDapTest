# author: zhangran
# createTime: 2023/5/28 10:44:24
# describe: 压测单个的websocket连接
import asyncio

import aiohttp
import websockets


async def awebsocket(uri):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        message = '{"content": "heart","msgType": "103"}'
                        await websocket.send(message)
                        print(f"Sent message: {message}")

                        response = await websocket.recv()
                        print(f"Received response: {response}")
                        await asyncio.sleep(5)  # 等待5秒后重新连接
                    except websockets.ConnectionClosedError as e:
                        print(f"Connection closed unexpectedly: {e.reason}")
                        await asyncio.sleep(5)  # 等待5秒后重新连接
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            await asyncio.sleep(5)  # 等待5秒后重新连接
            continue


async def main():
    tasks = []
    for i in range(200):
        uri = "ws://120.26.166.101/api/webSocket/webSocket/1662346690114945027/eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzdHVkZW50MkBleGFtcGxlLmNvbSIsImlhdCI6MTY4NTY5MDQ5MiwiYWNjb3VudCI6InN0dWRlbnQyQGV4YW1wbGUuY29tIiwianRpIjoiZmVmMGI5MTMtZmI4OS00N2Q3LTlmNTUtNmE3MWVjZGU1ZjJiIn0.jP0Pe9kvIA8K-3dhubSaVWWKANFs1WvKA_375KoX1Yc/null"
        task = asyncio.create_task(awebsocket(uri))
        tasks.append(task)
        # await asyncio.sleep(0)  # 等待一小段时间，以防止程序过度占用 CPU 资源

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
