# author: zhangran
# createTime: 2023/5/22
# describe: 登录500用户容器压测，并增加页面活跃元素，让页面处于活跃状态
import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import asyncio

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
    startTime = time.time()
    driver.get("http://120.26.166.101/dap-client/#/Signin")
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
            # 根据获取的地址，拼接juypter中的文件信息
            new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
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
            break
        except Exception as e:
            print("#############################【" + username + "open元素失败】######################")
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
            dmEndtime = time.time()
            dmduration = dmEndtime - dmTime
            print(
                "#############################【" + username + "运行全部代码元素定位到】######################" + f"时间统计：共花费 {dmduration:.2f} 秒")
            return 200
        except Exception as e:
            print("#############################【" + username + "运行全部代码元素定位到】######################")
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
    asyncio.run(taskOpenJuypter())
