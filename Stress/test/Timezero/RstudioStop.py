# author: zhangran
# createTime: 2024/3/20 9:57:54
# describe:关闭容器

import concurrent
import multiprocessing
import sys
import time
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

executor = concurrent.futures.ThreadPoolExecutor()
dapurl = "https://dap.acrc.hku.hk/hku-dap-client/#/Signin"

driver_path = r"D:\\chromedriver_32_122\\chromedriver.exe"


def get_all_users():
    users = []
    with open(r'user_zer.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开R容器地址
def test_eight_components(prid, user, mylist):
    time.sleep(prid * 1)
    serviceA = Service(executable_path=driver_path)
    optionsA = webdriver.ChromeOptions()
    optionsA.add_argument("--no-sandbox")
    optionsA.add_argument("--incognito")
    optionsA.add_argument('--disable-gpu')  # 这里的信息是附加信息，可以不设置，但是推荐设置
    optionsA.add_argument("start-maximized")
    optionsA.add_argument("enable-automation")
    optionsA.add_argument("--disable-infobars")
    optionsA.add_argument("--disable-dev-shm-usage")
    optionsA.add_argument("--disable-browser-side-navigation")
    optionsA.add_argument("enable-features=NetworkServiceInProcess")

    optionsA.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=optionsA, service=serviceA)
    time.sleep(3)

    MAX_RETRY_COUNT = 1800  # 最大重试次数
    retry_count = 0  # 当前重试次数

    username, password = user
    print("#############################【 线程" + str(prid) + username + "6】######################")
    startTime = time.time()
    driver.get(dapurl)
    driver.set_page_load_timeout(30000)
    while True:
        try:
            driver.implicitly_wait(5)
            username_email = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Email"]')
            username_email.send_keys(username)
            password_email = driver.find_element(by=By.CSS_SELECTOR, value='input[placeholder="Password"]')
            password_email.send_keys(password)
            loginbtn = driver.find_element(by=By.CLASS_NAME, value="el-button--large")
            loginbtn.click()
            endTime = time.time()
            duration = endTime - startTime
            print(
                "#############################【线程" + str(
                    prid) + username + "登录成功】######################" + "登录耗时-->" + f"时间统计：共花费 {duration:.2f} 秒")
            break
        except Exception as e:
            print("#############################【线程" + str(prid) + username + "登录元素失败】######################")
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "登录超时，超过重试次数】")
                return 500
            driver.refresh()
    openTime = time.time()
    while True:
        try:
            driver.implicitly_wait(5)
            # 获取当前所有窗口的句柄
            handles = driver.window_handles
            # 切换到新打开的窗口
            driver.switch_to.window(handles[0])

            element_stop = driver.find_element(by=By.XPATH,
                                               value='//button[@class="el-button el-button--text el-button--large"]/span[text()=" Stop "]')
            element_stop.click()
            print("#############################【线程" + str(
                prid) + username + " - stop元素关闭成功】######################")
            time.sleep(5)
            driver.close()
            break
        except Exception as e:
            print(
                "#############################【线程" + str(prid) + username + "--->stop元素失败】######################")
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "--->stop关闭重试超时，超过重试次数】")
                return 500
            driver.refresh()


if __name__ == "__main__":
    users = get_all_users()
    print(len(users))
    manager = multiprocessing.Manager()
    mylist = manager.list()

    pool = multiprocessing.Pool(processes=len(users))
    index = 0
    for user in users:
        index += 1
        pool.apply_async(func=test_eight_components, args=(index, user, mylist))

    pool.close()
    pool.join()

    while True:
        time.sleep(5)
        remaining_threads = pool._taskqueue.qsize()
        print("剩余工作线程数量：", remaining_threads)
        if remaining_threads < 1:
            print("执行成功", (len(users) - remaining_threads))
            sys.exit(0)
