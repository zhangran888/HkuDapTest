# author: zhangran
# createTime: 2023/6/14
# describe: 统计ECS连接数，进入到juypter执行代码页面
# 1 2 3 4 5 6 7 8 9 10 20 30 40 50 60 70 80 90 100

import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from selenium.common.exceptions import NoAlertPresentException
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
    with open(r'user_ws.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开juypter容器地址
async def openContainerUrl_Header(user, headless):
    MAX_RETRY_COUNT = 1800  # 最大重试次数
    retry_count = 0  # 当前重试次数

    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_114\\chromedriver.exe"
    options = Options()
    options.headless = headless
    options.add_argument("--incognito")
    options.add_argument('--ignore-certificate-errors')
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    print("#############################【 " + username + "6】######################")
    startTime = time.time()
    driver.get("http://47.99.202.72/dap-client/#/Signin")
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

            await asyncio.sleep(2)
            # 简单代码
            # new_url = open_url.replace('/tree?', '') + '/notebooks/solution/easycode.ipynb'
            if '/tree?' in open_url:
                # 根据获取的地址，拼接juypter中的文件信息 复杂代码
                new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
            else:
                raise Exception("无法打开正确的页面，请在 Jupyter notebook 主界面中打开页面！")

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
            # 执行 JavaScript 代码，禁用 monitor.js 日志打印
            js_code = """
                console.log = (function() {
                    var original_function = console.log;
                    return function() {
                        if (arguments.length > 0 && arguments[0].indexOf("monitor.js") !== -1) {
                            return;
                        }
                        original_function.apply(null, arguments);
                    };
                })();
            """
            driver.execute_script(js_code)
            # 执行 JavaScript 代码，禁用 monitor.js 日志打印

            await asyncio.sleep(2)
            execute_button = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
            execute_button.click()
            dmEndtime = time.time()
            dmduration = dmEndtime - dmTime
            print(
                "#############################【" + username + "运行全部代码成功】######################" + f"时间统计：共花费 {dmduration:.2f} 秒")
            await asyncio.sleep(2)
            print("#############################【 " + username + "4】#【区分是否打开浏览器" + str(
                headless) + "】#####################")
            modal = WebDriverWait(driver, 3).until(
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
        except Exception as e:
            print(e)
            print("#############################【" + username + "运行全部代码失败】######################")
            await asyncio.sleep(2)

            try:
                alert = driver.switch_to.alert
                alert.dismiss()  # 关闭弹窗
            except NoAlertPresentException:
                pass  # 如果不存在alert，则跳过
            retry_count += 1
            if retry_count > MAX_RETRY_COUNT:
                print("【" + username + "--->运行全部代码，超过重试次数】")
                return 500
            driver.refresh()

            try:
                alert = driver.switch_to.alert
                alert.accept()
            except NoAlertPresentException:
                pass  # 如果不存在alert，则跳过
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
            print("#############################【" + username + "】#【区分是否循环获取结果" + new_url + "】#####################")
            target_elements = driver.find_elements_by_xpath(
                '//div[contains(@class, "output_text") and @dir="auto"]/pre')
            text_to_check = "time cost"
            for element in target_elements:
                if text_to_check in element.text:
                    print(element.text)
                    # 找到保存按钮元素并模拟点击
                    save_btn = driver.find_element_by_xpath(
                        "//div[@id='save-notbook']//button[@data-jupyter-action='jupyter-notebook:save-notebook']")
                    save_btn.click()
                    zxEndTime = time.time()
                    zxduration = zxEndTime - zxStartTime
                    print(f"执行代码时间统计：共花费 {zxduration:.2f} 秒")
                    # await asyncio.sleep(300)
                    print(f"持续结束时间: {datetime.now()} ")
                    return 200
            await asyncio.sleep(2)
        except:
            await asyncio.sleep(2)


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
    unheadless = 5
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
