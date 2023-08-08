# author: zhangran
# createTime: 2023/7/26 13:33:54
# describe: 测试Rstudio容器进入运行代码


import concurrent
import multiprocessing
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import asyncio
from selenium.webdriver.common.action_chains import ActionChains

executor = concurrent.futures.ThreadPoolExecutor()
# dapurl = "http://118.31.244.163/dap-client/#/Signin"
# dapurl = "https://science-zr.datacyber.com/dap-client/#/Signin"
dapurl = "http://172.24.180.19/dap-client/#/Signin"

driver_path = r"D:\\chromedriver_32_115\\chromedriver.exe"


def get_all_users():
    users = []
    with open(r'user_rs.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
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

            element_open = driver.find_element(by=By.XPATH,
                                               value='//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
            element_open.click()
            print("#############################【线程" + str(
                prid) + username + " - open元素打开成功】######################")

            # 获取当前所有窗口的句柄
            handles = driver.window_handles
            # 切换到新打开的窗口
            driver.switch_to.window(handles[-1])
            open_url = driver.current_url
            driver.get(open_url)

            openEndTime = time.time()
            openduration = openEndTime - openTime
            # 打印新页面的标题和地址
            print(
                "标题" + driver.title + '地址' + open_url + "用户-->" + username + "到Rstudio时间--->" + f"时间统计：共花费 {openduration:.2f} 秒")
            break
        except Exception as e:
            print(
                "#############################【线程" + str(prid) + username + "--->open元素失败】######################")
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "--->open打开重试超时，超过重试次数】")
                return 500
            driver.refresh()
    dmTime = time.time()
    while True:
        try:
            time.sleep(3)
            driver.implicitly_wait(5)
            # 模拟键盘向下滚动操作
            driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # 等待页面加载
            # 找到 "solution" 文件夹并单击
            solution_folder = driver.find_element(by=By.XPATH,
                                                  value="//div[@class='GEL-OVUBGI GEL-OVUBJQ' and @title='solution']")
            solution_folder.click()
            # 等待页面加载完成
            time.sleep(3)
            # 找到 "test.R" 文件并单击
            test_file = driver.find_element(by=By.XPATH,
                                            value="//div[@class='GEL-OVUBGI GEL-OVUBJQ' and @title='6_boosting_CCB_cohort2_stressTest.R']")
            if test_file:
                test_file.click()
                # 等待文件加载完成
                time.sleep(3)
                text_area = driver.find_element(by=By.XPATH,
                                                value="//*[@id='rstudio_source_text_editor']/textarea")
                text_area.send_keys(Keys.CONTROL, "a")
                # 模拟按下Ctrl+Enter键执行代码
                text_area.send_keys(Keys.CONTROL, Keys.ENTER)

                dmEndtime = time.time()
                dmduration = dmEndtime - dmTime
                print(
                    "#############################【线程" + str(
                        prid) + username + "选中运行全部代码成功】######################" + f"时间统计：共花费 {dmduration:.2f} 秒")
                break
            else:
                # driver.refresh()
                driver.find_element(by=By.ID, value="rstudio_workbench_tab_files").click()

        except Exception as e:
            print("错误信息--->" + str(e))
            print("#############################【线程" + str(
                prid) + username + "运行全部代码失败】######################")
            rstudio_files = driver.find_element(by=By.ID, value="rstudio_workbench_tab_files")
            if rstudio_files:
                rstudio_files.click()
            else:
                driver.find_element(by=By.XPATH, value="//div[@class='rstudio-HyperlinkLabel GEL-OVUBJQ']").click()
            try:
                alert = driver.switch_to.alert
                alert.dismiss()  # 关闭弹窗
            except NoAlertPresentException:
                pass  # 如果不存在alert，则跳过
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【线程" + str(
                    prid) + username + "--->运行全部代码，超过重试次数】")
                return 500
            time.sleep(1)
            # driver.refresh()
    zxStartTime = time.time()
    while True:
        try:
            # 获取整个屏幕元素
            screen_element = driver.find_element(by=By.TAG_NAME, value="body")
            # 设置横向和纵向滑动距离
            x_offset = 100
            y_offset = 100
            # 使用ActionChains类模拟鼠标滑动
            action = ActionChains(driver)
            action.move_to_element(screen_element).perform()
            time.sleep(3)
            action.click_and_hold().move_by_offset(x_offset, y_offset).release().perform()
            # 等待一段时间再继续执行
            time.sleep(2)
            driver.implicitly_wait(5)
            print(
                "#############################【线程" + str(
                    prid) + username + "】#【区分是否循环获取结果】#####################")
            while True:
                output_text = driver.find_element(By.XPATH, value="//*[@id=\"rstudio_console_output\"]").text
                lines = output_text.splitlines()
                # print("############lines#############", lines)
                last_line = lines[-1].strip()
                # print("最后 一行打印的是", last_line)Time difference of 1.900014 hours
                if "Time difference of" in last_line:
                    print(last_line)
                    zxEndTime = time.time()
                    zxduration = zxEndTime - zxStartTime
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{prid} 执行成功,线程退出.")
                    print(f"执行代码时间统计：共花费 {zxduration:.2f} ，当前时间是{current_time}秒")
                    driver.quit()
                    pass
                    # return 200
                else:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{prid}代码未完成或发生错误 ({current_time})")
                    break
        except:
            print("判断是否执行完成error：", e)
            try:
                alert = driver.switch_to.alert
                alert.dismiss()  # 关闭弹窗
            except NoAlertPresentException:
                pass  # 如果不存在alert，则跳过

            try:
                alert = driver.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                pass  # 如果不存在alert，则跳过

            driver.implicitly_wait(2)


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
