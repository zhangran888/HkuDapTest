# author: zhangran
# createTime: 2023/8/5
# describe: 登录500用户容器压测，并增加页面活跃元素，让页面处于活跃状态，删除了禁用js的操作
import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

executor = concurrent.futures.ThreadPoolExecutor()
# 这里是异步任务的具体实现
chromepath = r"D:\\chromedriver_32_115\\chromedriver.exe"
options = Options()
options.add_argument("--incognito")
options.add_argument('--ignore-certificate-errors')
service = Service(chromepath)
options.add_argument('--ignore-ssl-errors=yes')  # 忽略证书错误


def get_all_users():
    users = []
    with open(r'D:\PycharmProjects\HkuDapTest\user_info.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
async def openContainerUrl_Header(user, headless):
    MAX_RETRY_COUNT = 1800  # 最大重试次数
    retry_count = 0  # 当前重试次数
    # options.headless = headless
    if headless:
        options.add_argument('--headless')
    username, password = user
    driver = webdriver.Chrome(options=options, service=service)
    print("#############################【 " + username + "6】######################")
    startTime = time.time()
    driver.get("https://science-zr.datacyber.com/dap-client/#/Signin")
    while True:
        try:
            await asyncio.sleep(2)
            username_email = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Email"]')
            username_email.send_keys(username)
            password_email = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Password"]')
            password_email.send_keys(password)
            loginbtn = driver.find_element(by=By.CLASS_NAME, value="el-button--large")
            loginbtn.click()
            endTime = time.time()
            duration = endTime - startTime
            print(
                "#############################【" + username + "登录成功】######################" + "登录耗时-->" + f"时间统计：共花费 {duration:.2f} 秒")
            break
        except Exception as e:
            print("#############################【" + username + "登录元素失败】######################")
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "登录超时，超过重试次数】")
                return 500
            driver.refresh()
    openTime = time.time()
    while True:
        try:
            await asyncio.sleep(2)
            # 获取当前所有窗口的句柄
            handles = driver.window_handles
            # 切换到新打开的窗口
            driver.switch_to.window(handles[0])
            element_open = driver.find_element(by=By.XPATH, value=
            '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
            element_open.click()
            print("#############################【" + username + " - open元素打开成功】######################")

            # 获取当前所有窗口的句柄
            handles = driver.window_handles
            # 切换到新打开的窗口
            driver.switch_to.window(handles[-1])
            open_url = driver.current_url

            await asyncio.sleep(2)
            if '/tree?' in open_url:
                # 根据获取的地址，拼接juypter中的文件信息
                new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
                # new_url = open_url.replace('/tree?', '') + '/notebooks/solution/easycode.ipynb'
            else:
                raise Exception("无法打开正确的页面，请在 Jupyter notebook 主界面中打开页面！")
            # driver.get(new_url)
            # 在新的浏览器窗口中打开 URL
            driver.execute_script("window.open('" + new_url + "');")
            # 切换到新的窗口
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])
            openEndTime = time.time()
            openduration = openEndTime - openTime
            # 打印新页面的标题和地址
            print(
                "标题" + driver.title + "初始地址" + open_url + "裁剪后地址" + new_url + "用户-->" + username + "到juypter时间--->" + f"时间统计：共花费 {openduration:.2f} 秒")

            await asyncio.sleep(10000)
        except Exception as e:
            print("#############################【" + username + "--->open元素失败】######################")
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "--->open打开重试超时，超过重试次数】")
                return 500
            driver.refresh()

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
    unheadless = 100
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
    qps = success_count / total_time
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")
    print(f"QPS: {qps:.2f}")


if __name__ == '__main__':
    asyncio.run(taskOpenJuypter())
