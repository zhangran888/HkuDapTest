# author: zhangran
# createTime: 2023/5/23
# describe: 登录500用户R容器压测，并增加页面活跃元素，让页面处于活跃状态
import concurrent
import time
from concurrent.futures import ThreadPoolExecutor
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
    with open(r'user_info1.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


# open打开Rstudio容器地址
async def openContainerUrl_Header(user, headless):
    # 这里是异步任务的具体实现
    chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
    options = Options()
    options.headless = headless
    options.add_argument("--incognito")
    driver = webdriver.Chrome(options=options, executable_path=chromepath)
    username, password = user
    print("#############################【 " + username + "6】######################")
    driver.get("http://120.26.166.101/dap-client/#/Signin")
    await asyncio.sleep(1)
    username_email = driver.find_element_by_css_selector('input[placeholder="Email"]')
    username_email.send_keys(username)
    password_email = driver.find_element_by_css_selector('input[placeholder="Password"]')
    password_email.send_keys(password)
    loginbtn = driver.find_element_by_class_name("el-button--large")
    loginbtn.click()
    await asyncio.sleep(1)
    element_open = driver.find_element_by_xpath(
        '//button[@class="el-button el-button--text el-button--large"]/span[text()="Open "]')
    element_open.click()
    # 获取当前所有窗口的句柄
    handles = driver.window_handles
    # 切换到新打开的窗口
    driver.switch_to.window(handles[-1])
    open_url = driver.current_url

    await asyncio.sleep(5)
    # 根据获取的地址，拼接juypter中的文件信息
    new_url = open_url.replace('/tree?', '') + '/notebooks/solution/titanic-project-example%20(1).ipynb'
    driver.get(new_url)
    # 打印新页面的标题和地址
    print("标题" + driver.title + "初始地址" + open_url + "裁剪后地址" + new_url + "用户-->" + username)

    await asyncio.sleep(5)
    execute_button = driver.find_element_by_xpath('//*[@id="run_int"]/button[4]')
    execute_button.click()
    # 查找目标元素
    while True:
        try:
            await asyncio.sleep(5)
            print("#############################【 " + username + "4】#【区分是否打开浏览器" + str(
                headless) + "】#####################")
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
        except Exception as e:
            print(f"打开容器失败，继续执行下个任务error: {e}")
            alert = driver.switch_to.alert
            alert.dismiss()  # 关闭弹窗
            # print("元素定位失败")
            print("#############################【" + username + "3】######################")
            driver.refresh()  # 刷新页面
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
                    time.sleep(10)
                    return 200
            await asyncio.sleep(10)
        except:
            await asyncio.sleep(10)


# 并发打开Rstudio页面
async def taskOpenRstudio():
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
    asyncio.run(taskOpenRstudio())
