# author: zhangran
# createTime: 2023/5/28 10:44:08
# describe: 查询listpage页面数据
import asyncio

import aiohttp


async def send_post_request(url):
    jwtToken = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzdHVkZW50MUBleGFtcGxlLmNvbSIsImlhdCI6MTY4NTE4MzI3MCwiYWNjb3VudCI6InN0dWRlbnQxQGV4YW1wbGUuY29tIiwianRpIjoiOTIxM2Y5MWQtNmVhNS00YjRiLThiMzQtMTNmODhiOGY0YjgzIn0.4aReDQQLAdVcLle_2K112BkL1OpXMzZOJyAfXuCfz_E"
    data = {
        "pageNo": 1,
        "pageSize": 12,
        "statusList": [
            "Free",
            "Expired",
            "Used Up",
            "Failed"
        ]
    }
    headers = {"jwtToken": f"{jwtToken}", "Content-Type": "application/json;charset=UTF-8"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            while True:
                try:
                    response_json = await response.json()
                    print(f"接收code码: {response_json['code']}")
                    await asyncio.sleep(10)
                except:
                    continue


async def listpagemain():
    tasks = []
    url = "http://120.26.166.101/api/client/myLabs/listPage"
    for i in range(500):
        task = asyncio.create_task(send_post_request(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print("请求listpage页面.")


if __name__ == '__main__':
    asyncio.run(listpagemain())
