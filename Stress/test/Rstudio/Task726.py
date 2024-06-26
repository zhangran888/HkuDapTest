# author: zhangran
# createTime: 2023/7/26 13:33:54
# describe: 测试Rstudio容器进入运行代码


import concurrent
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
import asyncio
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

executor = concurrent.futures.ThreadPoolExecutor()
dapurl = "http://118.31.244.163/dap-client/#/Signin"
# dapurl = "http://dap.datacyber.com/dap-client/#/Signin"


def get_all_users():
    users = []
    with open(r'user_rs.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
async def openContainerUrl_Header(user, headless):
    MAX_RETRY_COUNT = 1800  # 最大重试次数
    retry_count = 0  # 当前重试次数

    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_115\\chromedriver.exe"
    options = Options()
    options.headless = headless
    options.add_argument("--incognito")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    print("#############################【 " + username + "6】######################")
    startTime = time.time()
    driver.get(dapurl)
    while True:
        try:
            await asyncio.sleep(2)
            username_email = driver.find_element_by_css_selector('input[placeholder="Email"]')
            username_email.send_keys(username)
            password_email = driver.find_element_by_css_selector('input[placeholder="Password"]')
            password_email.send_keys(password)
            loginbtn = driver.find_element_by_class_name("el-button--large")
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

            element_open = driver.find_element_by_xpath(
                '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
            element_open.click()
            print("#############################【" + username + " - open元素打开成功】######################")

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
            print("#############################【" + username + "--->open元素失败】######################")
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "--->open打开重试超时，超过重试次数】")
                return 500
            driver.refresh()
    dmTime = time.time()
    while True:
        try:
            await asyncio.sleep(2)
            # 模拟键盘向下滚动操作
            driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
            time.sleep(2)  # 等待页面加载
            # 找到 "solution" 文件夹并单击
            solution_folder = driver.find_element_by_xpath(
                "//div[@class='GEL-OVUBGI GEL-OVUBJQ' and @title='solution']")
            solution_folder.click()
            # 等待页面加载完成
            time.sleep(2)
            # 找到 "test.R" 文件并单击
            test_file = driver.find_element_by_xpath("//div[@class='GEL-OVUBGI GEL-OVUBJQ' and @title='6_boosting_CCB_cohort2_stressTest.R']")
            # test_file = driver.find_element_by_xpath(
            #     "//div[@class='GEL-OVUBGI GEL-OVUBJQ' and @title='stressTest.R']")
            # test_file = driver.find_element_by_xpath(
            #     "//div[@class='GEL-OVUBGI GEL-OVUBJQ' and @title='test.R']")
            if test_file:
                # ActionChains(driver).double_click(test_file).perform()
                test_file.click()
                # 等待文件加载完成
                time.sleep(2)
                text_area = driver.find_element_by_xpath("//*[@id='rstudio_source_text_editor']/textarea")
                text_area.send_keys(Keys.CONTROL, "a")
                # 模拟按下Ctrl+Enter键执行代码
                text_area.send_keys(Keys.CONTROL, Keys.ENTER)

                dmEndtime = time.time()
                dmduration = dmEndtime - dmTime
                print(
                    "#############################【" + username + "选中运行全部代码成功】######################" + f"时间统计：共花费 {dmduration:.2f} 秒")
                break
            else:
                # driver.refresh()
                driver.find_element_by_id("rstudio_workbench_tab_files").click()

        except Exception as e:
            print("错误信息--->" + str(e))
            print("#############################【" + username + "运行全部代码失败】######################")
            rstudio_files = driver.find_element_by_id("rstudio_workbench_tab_files")
            if rstudio_files:
                rstudio_files.click()
            else:
                driver.find_element_by_xpath("//div[@class='rstudio-HyperlinkLabel GEL-OVUBJQ']").click()
            try:
                alert = driver.switch_to.alert
                alert.dismiss()  # 关闭弹窗
            except NoAlertPresentException:
                pass  # 如果不存在alert，则跳过
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "--->运行全部代码，超过重试次数】")
                return 500
            time.sleep(1)
            # driver.refresh()
    zxStartTime = time.time()
    while True:
        try:
            # 获取整个屏幕元素
            screen_element = driver.find_element_by_tag_name("body")
            # 设置横向和纵向滑动距离
            x_offset = 100
            y_offset = 100
            # 使用ActionChains类模拟鼠标滑动
            action = ActionChains(driver)
            action.move_to_element(screen_element).perform()
            time.sleep(1)
            action.click_and_hold().move_by_offset(x_offset, y_offset).release().perform()
            # 等待一段时间再继续执行
            time.sleep(2)
            print("#############################【" + username + "】#【区分是否循环获取结果】#####################")
            while True:
                output_text = driver.find_element_by_xpath("//*[@id=\"rstudio_console_output\"]").text
                lines = output_text.splitlines()
                # print("############lines#############", lines)
                last_line = lines[-1].strip()
                # print("最后 一行打印的是", last_line)Time difference of 1.900014 hours
                if "Time difference of" in last_line:
                    print(last_line)
                    zxEndTime = time.time()
                    zxduration = zxEndTime - zxStartTime
                    print(f"执行代码时间统计：共花费 {zxduration:.2f} 秒")
                    # await asyncio.sleep(300)
                    return 200
                else:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"代码未完成或发生错误 ({current_time}): {output_text}")
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

            await asyncio.sleep(2)


# 并发打开juypter内部页面
async def taskRstudio():
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
    qps = success_count / total_time
    print(f"总耗时: {total_time:.2f} s")
    print(f"总请求: {len(tasks)}")
    print(f"成功请求: {success_count}")
    print(f"TPS: {tps:.2f}")
    print(f"QPS: {qps:.2f}")


if __name__ == '__main__':
    asyncio.run(taskRstudio())
