# author: zhangran
# createTime: 2023/5/22
# describe: 登录500用户容器压测，问题排查，只到定位open元素阶段
import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

executor = concurrent.futures.ThreadPoolExecutor()


def get_all_users():
    users = []
    with open(r'D:\PycharmProjects\HkuDapTest\user_info.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
async def openContainerUrl_Header(user, headless):
    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    options.headless = headless
    options.add_argument("--incognito")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    print("#############################【 " + username + "6】######################")
    driver.get("http://120.26.166.101/dap-client/#/Signin")
    while True:
        try:
            await asyncio.sleep(10)
            username_email = driver.find_element_by_css_selector('input[placeholder="Email"]')
            username_email.send_keys(username)
            password_email = driver.find_element_by_css_selector('input[placeholder="Password"]')
            password_email.send_keys(password)
            loginbtn = driver.find_element_by_class_name("el-button--large")
            loginbtn.click()
            print("#############################【" + username + "登录成功】######################")
            break
        except Exception as e:
            print("#############################【" + username + "登录元素失败】######################")
    while True:
        try:
            await asyncio.sleep(10)
            element_open = driver.find_element_by_xpath(
                '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
            element_open.click()
            print("#############################【" + username + " - open元素打开成功】######################")
            return 200
        except Exception as e:
            print("#############################【" + username + "open元素失败】######################")
            return 500


# 并发打开juypter内部页面
async def taskOpenJuypter():
    tasks = []
    success_count = 0
    users = get_all_users()
    start_time = time.perf_counter()
    print(f"开始时间统计到: {start_time:.2f} s")
    print("开始时间统计到:" + str(datetime.now()))
    # 创建500个并发任务
    # 随机选择用户并发访问
    unheadless = 1
    for user in users:
        headless = True
        if unheadless > 0:
            headless = False
            unheadless -= 1
        tasks.append(asyncio.create_task(openContainerUrl_Header(user, headless)))

    await asyncio.gather(*tasks)

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


if __name__ == '__main__':
    asyncio.run(taskOpenJuypter())
