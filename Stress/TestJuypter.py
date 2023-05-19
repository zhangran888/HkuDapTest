# author: zhangran
# createTime: 2023/5/11 17:07:56
# describe: 登录500个用户并获取对应的jwtToken数据，查询500个用户对应的订单，并打开

import asyncio
import json
import random
import time
from asyncio import as_completed
from concurrent.futures import ThreadPoolExecutor

import requests

# 定义一个字典，用于保存每个用户账户对应的 Token 值
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
import websockets
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


# 500个打开容器
async def taskmain():
    tasks = []
    success_count = 0  # 初始化成功计数器为0
    total_time = 0
    start_time = time.time()
    print(f"开始时间统计到: {start_time:.2f} s")
    # 创建500任务
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


def get_all_users():
    users = []
    with open(r'D:\PycharmProjects\HkuDapTest\user_info.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
async def openContainerUrl_Noheader(user):
    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    # 设置无头浏览器，模拟访问接口
    options.headless = True
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    driver.get("http://120.26.166.101/dap-client/#/Signin")
    time.sleep(1)
    username_email = driver.find_element_by_css_selector('input[placeholder="Email"]')
    username_email.send_keys(username)
    password_email = driver.find_element_by_css_selector('input[placeholder="Password"]')
    # driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Password"]')
    password_email.send_keys(password)
    loginbtn = driver.find_element_by_class_name("el-button--large")
    loginbtn.click()
    time.sleep(1)
    max_try = 1
    # for i in range(max_try):
        # try:
    element_open = driver.find_element_by_xpath(
        '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
    element_open.click()
        # except StaleElementReferenceException:
            # 捕捉StaleElementReferenceException并在控制台输出错误信息
            # print('open不再位于当前页面中，正在进行第{}次尝试...'.format(i + 1))
            # if i == max_try - 1:
            #     print('open已达到最大尝试次数....')
    # else:
    #     print('open已经尝试{}次，但元素仍未找到！'.format(max_try))
    # 获取当前所有窗口的句柄
    handles = driver.window_handles
    # 切换到新打开的窗口
    driver.switch_to.window(handles[-1])
    open_url = driver.current_url
    # print("标题" + driver.title + "访问地址" + open_url)

    # 根据获取的地址，拼接juypter中的文件信息
    new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
    driver.get(new_url)
    # 打印新页面的标题和地址
    print("标题" + driver.title + "初始地址" + open_url + "裁剪后地址" + new_url)

    for i in range(max_try):
        try:
            # 停留一秒，用于获取到运行的功能xpath地址
            time.sleep(1)
            execute_button = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
            execute_button.click()
            # time.sleep(3)

            # 创建WebDriverWait对象，设置最长等待时间为10秒
            wait = WebDriverWait(driver, 10)
            # 查找目标元素
            try:
                ebutton = wait.until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//button[@class="btn btn-default btn-sm btn-danger" and @data-dismiss="modal" and text()="重启并运行所有代码块"]'))
                )
                # 对目标元素执行操作
                ebutton.click()
                # print('成功获取元素！')
            except:
                # print("元素定位失败")
                driver.refresh()  # 刷新页面
                try:
                    ebutton = wait.until(
                        EC.presence_of_element_located((By.XPATH,
                                                        '//button[@class="btn btn-default btn-sm btn-danger" and @data-dismiss="modal" and text()="重启并运行所有代码块"]'))
                    )
                    # 对目标元素执行操作
                    ebutton.click()
                    # print('成功获取元素！')
                except:
                    # print("元素定位失败，无法刷新页面！")
                    continue
            try:
                target_element = driver.find_elements_by_xpath(
                    '//div[contains(@class, "output_text") and @dir="auto"]')
                result = target_element.text
                if result:
                    # print("代码执行完成，目标区域存在" + result)
                    return 200
            except TimeoutException:
                # print("等待超时，目标区域不存在")
                return 500
            # break
        except StaleElementReferenceException:
            # 捕捉StaleElementReferenceException并在控制台输出错误信息
            # print('结果元素不再位于当前页面中，正在进行第{}次尝试...'.format(i + 1))
            if i == max_try - 1:
                print('结果输出已达到最大尝试次数....')
    # else:
    #     print('juypter元素已经尝试{}次，但元素仍未找到！'.format(max_try))
    # console_logs = driver.execute_script('return console.error')
    # print_logs = driver.get_log('browser')
    # print(print_logs)
    # if console_logs:
    #     print('控制台上有{}个错误：'.format(len(console_logs)))
    #     for log in console_logs:
    #         print(log)
    # else:
    #     print('控制台上没有错误信息。')
    return 200


# open打开juypter容器地址
async def openContainerUrl_Header(user):
    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    driver.get("http://120.26.166.101/dap-client/#/Signin")
    time.sleep(1)
    username_email = driver.find_element_by_css_selector('input[placeholder="Email"]')
    username_email.send_keys(username)
    password_email = driver.find_element_by_css_selector('input[placeholder="Password"]')
    # driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Password"]')
    password_email.send_keys(password)
    loginbtn = driver.find_element_by_class_name("el-button--large")
    loginbtn.click()
    time.sleep(1)
    max_try = 1
    # for i in range(max_try):
    #     try:
    element_open = driver.find_element_by_xpath(
        '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
    element_open.click()
        # except StaleElementReferenceException:
        #     # 捕捉StaleElementReferenceException并在控制台输出错误信息
        #     # print('open不再位于当前页面中，正在进行第{}次尝试...'.format(i + 1))
        #     if i == max_try - 1:
        #         print('open已达到最大尝试次数....')
    # else:
    #     print('open已经尝试{}次，但元素仍未找到！'.format(max_try))
    # 获取当前所有窗口的句柄
    handles = driver.window_handles
    # 切换到新打开的窗口
    driver.switch_to.window(handles[-1])
    open_url = driver.current_url
    # print("标题" + driver.title + "访问地址" + open_url)

    # 根据获取的地址，拼接juypter中的文件信息
    new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
    driver.get(new_url)
    # 打印新页面的标题和地址
    print("标题" + driver.title + "初始地址" + open_url + "裁剪后地址" + new_url)

    # for i in range(max_try):
    try:
        # 停留一秒，用于获取到运行的功能xpath地址
        time.sleep(1)
        execute_button = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
        execute_button.click()
        # time.sleep(3)

        # 创建WebDriverWait对象，设置最长等待时间为10秒
        wait = WebDriverWait(driver, 10)
        # 查找目标元素
        try:
            ebutton = wait.until(
                EC.presence_of_element_located((By.XPATH,
                                                '//button[@class="btn btn-default btn-sm btn-danger" and @data-dismiss="modal" and text()="重启并运行所有代码块"]'))
            )
            # 对目标元素执行操作
            ebutton.click()
            # print('成功获取元素！')
        except:
            # print("元素定位失败")
            driver.refresh()  # 刷新页面
            try:
                ebutton = wait.until(
                    EC.presence_of_element_located((By.XPATH,
                                                    '//button[@class="btn btn-default btn-sm btn-danger" and @data-dismiss="modal" and text()="重启并运行所有代码块"]'))
                )
                # 对目标元素执行操作
                ebutton.click()
                # print('成功获取元素！')
            except:
                # print("元素定位失败，无法刷新页面！")
                print()
        # try:
            target_element = driver.find_elements_by_xpath(
                '//div[contains(@class, "output_text") and @dir="auto"]')
            result = target_element.text
            if result:
                # print("代码执行完成，目标区域存在" + result)
                return 200
            # except TimeoutException:
            #     # print("等待超时，目标区域不存在")
            #     return 500
            # break
    except StaleElementReferenceException:
        print()
    #     # 捕捉StaleElementReferenceException并在控制台输出错误信息
    #     # print('结果元素不再位于当前页面中，正在进行第{}次尝试...'.format(i + 1))
    #     if i == max_try - 1:
    #         print('结果输出已达到最大尝试次数....')
    # else:
    #     print('juypter元素已经尝试{}次，但元素仍未找到！'.format(max_try))
    # console_logs = driver.execute_script('return console.error')
    # print_logs = driver.get_log('browser')
    # print(print_logs)
    # if console_logs:
    #     print('控制台上有{}个错误：'.format(len(console_logs)))
    #     for log in console_logs:
    #         print(log)
    # else:
    #     print('控制台上没有错误信息。')
    return 200


async def taskOpenJuypter():
    tasks = []
    users = get_all_users()
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    # 创建500个并发任务
    # 随机选择5个用户并发访问
    for user in random.sample(users, k=10):
        task = asyncio.create_task(openContainerUrl_Header(user))
        tasks.append(task)
    for user in random.sample(users, k=490):
        task = asyncio.create_task(openContainerUrl_Noheader(user))
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
    # for i, (result, duration) in enumerate(zip(results, durations)):
    #     print(f"Task {i}: Result {result}, Duration {duration:.2f}s")
    # 统计总耗时和其他信息
    success_count = sum(1 for result in results if result == 200)
    total_time = time.perf_counter() - start_time
    tps = len(tasks) / total_time if total_time > 0 else 0
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")


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


if __name__ == '__main__':
    asyncio.run(taskmain())
    # asyncio.run(taskOpenJuypter())
    # asyncio.run(taskCloseLab())
    # print()
