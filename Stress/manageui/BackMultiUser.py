# author: zhangran
# createTime: 2024/4/17 13:53:48
# describe:多用户串行登录打开管理后台，进行UI自动化操作
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile
from Stress.manageui.MenuList import menuListByUser

chromepath = ConfigFile.driver_path
options = webdriver.ChromeOptions()
options.add_argument(ConfigFile.no_sandbox)  # 沙箱模式用于隔离浏览器进程
options.add_argument(ConfigFile.incognito)  # 无痕模式
options.add_argument(ConfigFile.disablegpu)  # 这里的信息是附加信息，可以不设置，但是推荐设置，禁用GPU加载
options.add_argument(ConfigFile.maximized)  # 浏览窗口最大化
options.add_argument(ConfigFile.automation)  # 启用自动化控制
options.add_argument(ConfigFile.infobars)  # 禁用提示和通知
options.add_argument(ConfigFile.devshmusage)  # 禁用临时文件
options.add_argument(ConfigFile.browsernavigation)  # 禁用浏览器导航
options.add_argument(ConfigFile.NetworkServiceInProcess)  # 启用网络服务进程，提高稳定性和安全性
service = Service(chromepath)


def get_all_users():
    users = []
    with open(r'bankuser.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            users.append((username, password))
    return users


async def openWinow(user):
    try:
        username, password = user
        driver = webdriver.Chrome(options=options, service=service)
        driver.get(ConfigFile.url_path)
        driver.set_page_load_timeout(30000)
        driver.implicitly_wait(5)

        username_email = driver.find_element(by=By.CSS_SELECTOR, value=ConfigFile.input_username)
        username_email.send_keys(username)
        password_email = driver.find_element(by=By.CSS_SELECTOR, value=ConfigFile.input_password)
        password_email.send_keys(password)
        loginbtn = driver.find_element(by=By.CLASS_NAME, value=ConfigFile.click_btn)
        loginbtn.click()
        menuListByUser(driver, username, password)
    except Exception as e:
        print(f"Error processing user {username}: {e}")
    finally:
        driver.quit()


async def taskOpen():
    tasks = []
    users = get_all_users()

    for user in users:
        tasks.append(asyncio.create_task(openWinow(user)))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(taskOpen())
