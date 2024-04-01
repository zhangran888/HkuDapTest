# author: zhangran
# createTime: 2024/3/21 17:20:14
# describe: DAP管理后台UI自动化

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile
from Stress.manageui.DataOverview import DataOview
from Stress.manageui.LabManagement import CaseLab
from Stress.manageui.OrderManagement import Order
from Stress.manageui.ResourceMonitor import ResourceMoni
from Stress.manageui.UserManagement import Administrators

driver_path = ConfigFile.driver_path

dap_url = ConfigFile.url_path

serviceA = Service(executable_path=driver_path)
optionsA = webdriver.ChromeOptions()
optionsA.add_argument(ConfigFile.no_sandbox)  # 沙箱模式用于隔离浏览器进程
optionsA.add_argument(ConfigFile.incognito)  # 无痕模式
optionsA.add_argument(ConfigFile.disablegpu)  # 这里的信息是附加信息，可以不设置，但是推荐设置，禁用GPU加载
optionsA.add_argument(ConfigFile.maximized)  # 浏览窗口最大化
optionsA.add_argument(ConfigFile.automation)  # 启用自动化控制
optionsA.add_argument(ConfigFile.infobars)  # 禁用提示和通知
optionsA.add_argument(ConfigFile.devshmusage)  # 禁用临时文件
optionsA.add_argument(ConfigFile.browsernavigation)  # 禁用浏览器导航
optionsA.add_argument(ConfigFile.NetworkServiceInProcess)  # 启用网络服务进程，提高稳定性和安全性

optionsA.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=optionsA, service=serviceA)


# 设置访问地址及浏览器相关信息
def loginIn():
    driver.get(dap_url)
    driver.set_page_load_timeout(30000)

    username = ConfigFile.user_name
    password = ConfigFile.pass_word
    driver.implicitly_wait(5)
    username_email = driver.find_element(by=By.CSS_SELECTOR, value=ConfigFile.input_username)
    username_email.send_keys(username)
    password_email = driver.find_element(by=By.CSS_SELECTOR, value=ConfigFile.input_password)
    password_email.send_keys(password)
    loginbtn = driver.find_element(by=By.CLASS_NAME, value=ConfigFile.click_btn)
    loginbtn.click()


def InManage():
    loginIn()

    # Data Overview模块
    DataOview.userLabOvew(driver)

    # Resource Monitoring模块
    ResourceMoni.MirrorDatasetSource(driver)

    # Lab Management模块
    CaseLab.CaseLab(driver)

    # Order Management 模块
    Order.TrialSubscition(driver)

    # User Management模块
    Administrators.AdminiCoustmer(driver)

    driver.close()


if __name__ == '__main__':
    InManage()
