# author: zhangran
# createTime: 2023/5/18 8:54:46
# describe:
# author: zhangran
# createTime: 2023/5/11 17:07:56
# describe: 登录500个用户并获取对应的jwtToken数据，查询500个用户对应的订单，并打开

import asyncio
import concurrent
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
executor = concurrent.futures.ThreadPoolExecutor()


# 登录并定义字典，存储不同用户的jwtToken数据
def login():
    # 从 txt 文件中读取用户名和密码
    with open(r'D:\PycharmProjects\HkuDapTest\user.txt', 'r') as f:
        tasks = []
        for line in f:
            tasks.append(executor.submit(loginUser, line))
        concurrent.futures.wait(tasks)


def loginUser(line):
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
        print(f'jwtToken获取失败：{username}')


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
        return response.json()["code"]


# 启动订单容器
def open_lab():
    login()
    # print(global_token_dict.items())
    tasks = []
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    for username, jwtToken in global_token_dict.items():
        tasks.append(executor.submit(open_lab_executor, jwtToken, username))
    concurrent.futures.wait(tasks)
    success_count = 0  # 初始化成功计数器为0
    print(f"开始时间统计到: {start_time:.2f} s")
    # 获取异步任务的结果
    for task in tasks:
        result = task.result()
        if result == 200:
            success_count += 1
            print("Task result:", result)
    # 统计总耗时和其他信息
    total_time = time.perf_counter() - start_time
    tps = len(tasks) / total_time if total_time > 0 else 0
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")


def open_lab_executor(jwtToken, username):
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
            return 200
        else:
            print(f'订单{labSubscriptionId}，lab容器打开失败')
            return 500


# 关闭已经打开的容器
def close_lab(jwtToken, username):
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
            return 200
        else:
            print(f'订单{labSubscriptionId}，lab容器关闭失败')
            return 500


def get_all_users():
    users = []
    with open(r'D:\PycharmProjects\HkuDapTest\user_info.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
def openContainerUrl_Header(user, headless):
    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    options.headless = headless
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    print("#############################【 " + username + "6】######################")
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
    element_open = driver.find_element_by_xpath(
        '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
    element_open.click()
    # 获取当前所有窗口的句柄
    handles = driver.window_handles
    # 切换到新打开的窗口
    driver.switch_to.window(handles[-1])
    open_url = driver.current_url

    time.sleep(5)
    # 根据获取的地址，拼接juypter中的文件信息
    new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
    driver.get(new_url)
    # 打印新页面的标题和地址
    print("标题" + driver.title + "初始地址" + open_url + "裁剪后地址" + new_url)

    time.sleep(5)
    execute_button = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
    execute_button.click()
    # 查找目标元素
    while True:
        try:
            time.sleep(5)
            print("#############################【 " + username + "4】#【区分是否打开浏览器" + str(
                headless) + "】#####################")
            # if headless:
            modal = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME,
                     'modal-content')
                )
            )
            # 调整窗口大小
            driver.set_window_size(800, 600)
            # 点击“重启并运行所有代码块”按钮
            restart_button = modal.find_element_by_css_selector('.btn-danger')
            restart_button.click()
            break
            # else:
            #     ebutton = WebDriverWait(driver, 10).until(
            #         EC.visibility_of_element_located(
            #             (By.XPATH,
            #              '//button[@class="btn btn-default btn-sm btn-danger" and @data-dismiss="modal" and text()="重启并运行所有代码块"]')
            #         )
            #     )
            #     # 对目标元素执行操作
            #     ebutton.click()
            #     break
            # print('成功获取元素！')
        except Exception as e:
            print(f"打开容器失败，继续执行下个任务error: {e}")
            alert = driver.switch_to.alert
            alert.dismiss()  # 关闭弹窗
            # print("元素定位失败")
            print("#############################【" + username + "3】######################")
            driver.refresh()  # 刷新页面

    while True:
        try:
            # time.sleep(100000)
            target_elements = driver.find_elements_by_xpath(
                '//div[contains(@class, "output_text") and @dir="auto"]/pre')

            text_to_check = "time cost"

            for element in target_elements:
                if text_to_check in element.text:
                    print(element.text)
                    return 200
            time.sleep(10)
        except:
            time.sleep(10)


# 并发打开juypter内部页面
def taskOpenJuypter():
    tasks = []
    success_count = 0
    users = get_all_users()
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    # 创建500个并发任务
    # 随机选择用户并发访问
    unheadless = 0
    for user in users:
        headless = True
        if unheadless > 0:
            headless = False
            unheadless -= 1
        tasks.append(executor.submit(openContainerUrl_Header, user, headless))

    concurrent.futures.wait(tasks)

    # 获取异步任务的结果
    for task in tasks:
        result = task.result()
        if result == 200:
            success_count += 1
        print("Task result:", result)

    # 统计总耗时和其他信息
    total_time = time.perf_counter() - start_time
    tps = len(tasks) / total_time if total_time > 0 else 0
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")


# 关闭已经打开的容器
def taskCloseLab():
    tasks = []
    success_count = 0
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    login()
    # print(global_token_dict.items())
    for username, jwtToken in global_token_dict.items():
        tasks.append(executor.submit(close_lab, jwtToken, username))
    concurrent.futures.wait(tasks)

    # 获取异步任务的结果
    for task in tasks:
        result = task.result()
        if result == 200:
            success_count += 1
        print("Task result:", result)

    total_time = time.perf_counter() - start_time
    tps = len(tasks) / total_time
    qps = success_count / total_time
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")
    print(f"QPS: {qps:.2f}")


if __name__ == '__main__':
    # taskOpenJuypter()
    # time.sleep(5000)
    taskCloseLab()
    # print()
