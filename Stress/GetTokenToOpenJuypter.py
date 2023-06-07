# author: zhangran
# createTime: 2023/5/11 17:07:56
# describe: 登录500个用户并获取对应的jwtToken数据，查询500个用户对应的订单，并打开

import asyncio
import json
import time
from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor

import requests

# 定义一个字典，用于保存每个用户账户对应的 Token 值
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
import websockets

global_token_dict = {}
container_url_dict = {}


# 登录并定义字典，存储不同用户的jwtToken数据
def login():
    # 从 txt 文件中读取用户名和密码
    with open(r'D:\PycharmProjects\HkuDapTest\user_info.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            # 构造登录请求的参数
            url = 'http://120.26.166.101/api/client/student/user/login'
            headers = {"Content-Type": "application/json;charset=UTF-8"}

            data = {
                'username': username,
                'password': password
            }
            json_data = json.dumps(data)

            # 发送登录请求
            response = requests.post(url, data=json_data, headers=headers)
            # 检查响应是否成功
            if response.json()['code'] == 0:
                # 获取返回的 token 数据
                jwtToken = response.json()['data']
                global_token_dict[username] = jwtToken
                # print(f'{username} 成功获取到 jwtToken：{jwtToken}')
            else:
                print(f'jwtToken获取失败：{jwtToken}')


# 根据不同用户的jwtToken数据获取对应的lab订单列表的第一笔数据
def get_laborder_byuser_jwttoken(jwtToken):
    url = "http://120.26.166.101/api/client/myLabs/listPage"
    headers = {"jwtToken": f"{jwtToken}", "Content-Type": "application/json;charset=UTF-8"}
    data = {
        "pageNo": 1,
        "pageSize": 10,
        "statusList": [
            "Free",
            "Expired",
            "Used Up",
            "Failed"
        ]
    }
    json_data = json.dumps(data)
    # print(jwtToken)
    response = requests.post(url, data=json_data, headers=headers)
    # print(response.json())
    if response.json()['code'] == 0:
        laborder = response.json()
        # print(laborder)
        if laborder:
            return laborder['data']['records'][0]['labSubscriptionId']
        else:
            print('当前账户没有任何订单')
            return None
    else:
        print(f'请求失败，错误码：{response.json()["code"]}')
        return None


# 启动订单容器
async def open_lab():
    login()
    for username, jwtToken in global_token_dict.items():
        labSubscriptionId = get_laborder_byuser_jwttoken(jwtToken)
        if labSubscriptionId:
            print(f'用户 {username} 的第一个订单是：{labSubscriptionId}')
            url = "http://120.26.166.101/api/client/myLabs/labStart"
            data = {
                "labSubscriptionId": labSubscriptionId
            }
            json_data = json.dumps(data)
            headers = {"jwtToken": f"{jwtToken}", "Content-Type": "application/json;charset=UTF-8"}
            response = requests.post(url, data=json_data, headers=headers)
            print(response.json())
            if response.json()['code'] == 0:
                print(f'订单{labSubscriptionId}，lab容器打开成功')
            else:
                print(f'订单{labSubscriptionId}，lab容器打开失败')


# 关闭已经打开的容器
async def close_lab():
    login()
    for username, jwtToken in global_token_dict.items():
        labSubscriptionId = get_laborder_byuser_jwttoken(jwtToken)
        if labSubscriptionId:
            print(f'用户 {username} 的第一个订单是：{labSubscriptionId}')
            url = "http://120.26.166.101/api/client/myLabs/labStop"
            data = {
                "labSubscriptionId": labSubscriptionId
            }
            json_data = json.dumps(data)
            headers = {"jwtToken": f"{jwtToken}", "Content-Type": "application/json;charset=UTF-8"}
            response = requests.post(url, data=json_data, headers=headers)
            print(response.json())
            if response.json()['code'] == 0:
                print(f'订单{labSubscriptionId}，lab容器关闭成功')
            else:
                print(f'订单{labSubscriptionId}，lab容器关闭失败')


# 关闭已经打开的容器
async def taskCloseLab():
    tasks = []
    success_count = 0
    total_time = 0
    start_time = time.time()
    # 创建500个并发任务
    for i in range(1):
        task = asyncio.create_task(close_lab())
        tasks.append(task)
    # 等待所有任务完成后获取结果
    for coro in asyncio.as_completed(tasks):
        result = await coro  # 注意这里是await
        success_count += 1
        total_time += time.time() - start_time
        print(result)
    tps = len(tasks) / total_time
    qps = success_count / total_time
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")
    print(f"QPS: {qps:.2f}")


# 500个并发同时打开容器
async def taskmain():
    tasks = []
    success_count = 0  # 初始化成功计数器为0
    total_time = 0
    start_time = time.time()
    print(f"开始时间统计到: {start_time:.2f} s")
    # 创建500个并发任务
    for i in range(1):
        task = asyncio.create_task(open_lab())
        tasks.append(task)
        # 等待所有任务完成后获取结果
    for coro in asyncio.as_completed(tasks):
        try:
            result = await coro  # 注意这里是await
            success_count += 1  # 成功计数器加1
        except Exception as e:
            print(f"打开容器失败，继续执行下个任务: {coro}, error: {e}")
            continue  # 忽略该任务，并继续执行下一个任务
        current_time = time.time()
        total_time += current_time - start_time
        start_time = current_time  # 更新start_time
        print(result)
    if total_time == 0:
        tps = 0  # total_time为0，则tps为0
    else:
        tps = len(tasks) / total_time
    qps = success_count / total_time
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")
    print(f"QPS: {qps:.2f}")


# 获取打开juypter的地址
def getContainerUrl():
    login()
    for username, jwtToken in global_token_dict.items():
        labSubscriptionId = get_laborder_byuser_jwttoken(jwtToken)
        # print("获取容器地址的用户-" + jwtToken)
        # print(r"获取到的id数据为" + labSubscriptionId)
        url = "http://120.26.166.101/api/client/myLabs/listPage"
        headers = {"jwtToken": f"{jwtToken}", "Content-Type": "application/json;charset=UTF-8"}
        data = {
            "pageNo": 1,
            "pageSize": 10,
            "statusList": [
                "Free",
                "Expired",
                "Used Up",
                "Failed"
            ]
        }
        json_data = json.dumps(data)
        # print(f"labSubscriptionId获取的对应token {labSubscriptionId}-->" + jwtToken)
        response = requests.post(url, data=json_data, headers=headers)
        # print(response.json())
        if response.json()['code'] == 0:
            laborder = response.json()["data"]
            print(laborder)
            for recode in laborder['records']:
                # if recode['labSubscriptionId'] is not None and recode['containerStatus'] is not None and labSubscriptionId is not None:
                #     print(recode['labSubscriptionId'] + "---->" + recode[
                #         'containerStatus'] + "获取的订单id" + labSubscriptionId)
                if recode['labSubscriptionId'] == labSubscriptionId and recode['containerStatus'] == '2':
                    # print(recode['labSubscriptionId'] + recode['containerStatus'])
                    print(recode['containerUrl'])
                    containerUrl = recode['containerUrl']
                    container_url_dict[labSubscriptionId] = containerUrl
                else:
                    print('未获取到juypter地址')
        else:
            print(f'请求失败，错误码：{response.json()["code"]}')


# open打开juypter容器地址
async def openContainerUrl(containerUrl):
    # 这里是异步任务的具体实现
    print("打印的url地址-->" + containerUrl)
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    # 设置无头浏览器，模拟访问接口
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    # open打开容器获取新开浏览器地址
    driver.get(containerUrl)
    open_url = driver.current_url
    # 根据获取的地址，拼接juypter中的文件信息
    new_url = open_url.replace('/tree?', '') + '/notebooks/solution/test.ipynb'
    driver.get(new_url)
    # 打印新页面的标题和地址
    print("标题" + driver.title + "初始地址" + open_url + "裁剪后地址" + new_url)

    # 停留一秒，用于获取到运行的功能xpath地址
    time.sleep(1)
    execute_button = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
    execute_button.click()
    time.sleep(3)
    max_try = 3
    for i in range(max_try):
        try:
            ebutton = driver.find_element_by_class_name("btn-danger")
            ebutton.click()
            print('成功获取元素！')
            time.sleep(1)
            target_element = driver.find_element_by_class_name(
                'output_stdout')
            if target_element:
                print("代码执行完成，目标区域存在" + target_element.text)
            else:
                print("目标区域不存在")
            break
        except StaleElementReferenceException:
            # 捕捉StaleElementReferenceException并在控制台输出错误信息
            print('元素不再位于当前页面中，正在进行第{}次尝试...'.format(i + 1))
            if i == max_try - 1:
                print('已达到最大尝试次数....')
    else:
        print('已经尝试{}次，但元素仍未找到！'.format(max_try))
    console_logs = driver.execute_script('return console.error')
    print_logs = driver.get_log('browser')
    print(print_logs)
    if console_logs:
        print('控制台上有{}个错误：'.format(len(console_logs)))
        for log in console_logs:
            print(log)
    else:
        print('控制台上没有错误信息。')
    print("结束-->" + containerUrl)
    return 200


# 并发打开500个juypter的代码地址文件
# async def taskOpenJuypter():
#     tasks = []
#     success_count = 0
#     total_time = 0
#     start_time = time.time()
#     print(f"开始时间统计到: {start_time:.2f} s")
#     # 创建500个并发任务
#     for container_url in container_url_dict.values():
#         task = asyncio.create_task(openContainerUrl(container_url))
#         tasks.append(task)
#     # 等待所有任务完成后获取结果
#     for coro in asyncio.as_completed(tasks):
#         try:
#             result = await coro  # 注意这里是await
#             if result == 200:
#                 success_count += 1
#         except Exception as e:
#             print(f"Exception occurs in coroutine: {coro}, error: {e}")
#             continue  # 忽略该任务，并继续执行下一个任务
#     current_time = time.time()
#     total_time += current_time - start_time
#     if total_time == 0:
#         tps = 0  # total_time为0，则tps为0
#     else:
#         tps = len(tasks) / total_time
#     print(f"总耗时: {total_time:.2f} s")
#     print(f"总请求: {len(tasks)}")
#     print(f"成功请求: {success_count}")
#     print(f"TPS: {tps:.2f}")
async def taskOpenJuypter():
    tasks = []
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    # 创建500个并发任务
    for container_url in container_url_dict.values():
        task = asyncio.create_task(openContainerUrl(container_url))
        tasks.append(task)
    results = []
    durations = []
    for task in tasks:
        start_timestamp = time.perf_counter()
        result = await task
        end_timestamp = time.perf_counter()
        results.append(result)
        durations.append(end_timestamp - start_timestamp)
    # 输出每个任务的执行结果和耗时
    for i, (result, duration) in enumerate(zip(results, durations)):
        print(f"Task {i}: Result {result}, Duration {duration:.2f}s")
    # 统计总耗时和其他信息
    success_count = sum(1 for result in results if result == 200)
    total_time = time.perf_counter() - start_time
    tps = len(tasks) / total_time if total_time > 0 else 0
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")


# async def taskOpenJuypter():
#     tasks = []
#     success_count = 0
#     total_time = 0
#     start_time = time.time()
#     print(f"开始时间统计到: {start_time:.2f} s")
#     # 创建500个并发任务
#     for i in range(500):
#         task = asyncio.create_task(openContainerUrl())
#         tasks.append(task)
#     # 等待所有任务完成后获取结果
#     for coro in asyncio.as_completed(tasks):
#         try:
#             result = await coro  # 注意这里是await
#         except Exception as e:
#             print(f"Exception occurs in coroutine: {coro}, error: {e}")
#             continue  # 忽略该任务，并继续执行下一个任务
#         current_time = time.time()
#         total_time += current_time - start_time
#         start_time = current_time  # 更新start_time
#         # print(f"耗时统计到: {total_time:.2f} s")
#         # success_count += (result == 200)
#
#         print(result)
#     if total_time == 0:
#         tps = 0  # total_time为0，则tps为0
#     else:
#         tps = len(tasks) / total_time
#     # qps = success_count / total_time
#     print(f"总耗时: {total_time:.2f} s")
#     print(f"总请求: {len(tasks)}")
#     print(f"成功请求: {success_count}")
#     print(f"TPS: {tps:.2f}")
#     # print(f"QPS: {qps:.2f}")

# 建立websocket连接，直到连接不上
async def send_messages(websocket):
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
            continue


async def awebsocket(uri):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                await send_messages(websocket)
                await asyncio.sleep(5)  # 等待5秒后发送
        except Exception as e:
            print(f"Unexpected error occurred: {e}")
            await asyncio.sleep(5)  # 等待5秒后重新连接
            continue


async def websoketmain():
    uri = "ws://120.26.166.101/api/client/webSocket/1662346690114945026/eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzdHVkZW50MUBleGFtcGxlLmNvbSIsImlhdCI6MTY4NTE4MzI3MCwiYWNjb3VudCI6InN0dWRlbnQxQGV4YW1wbGUuY29tIiwianRpIjoiOTIxM2Y5MWQtNmVhNS00YjRiLThiMzQtMTNmODhiOGY0YjgzIn0.4aReDQQLAdVcLle_2K112BkL1OpXMzZOJyAfXuCfz_E/null"
    tasks = [asyncio.create_task(awebsocket(uri)) for _ in range(1500)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    # asyncio.run(taskmain())

    # getContainerUrl()
    # asyncio.run(taskOpenJuypter())

    # 运行测试WebSocket连接
    asyncio.run(websoketmain())

    # asyncio.run(taskCloseLab())
