# author: zhangran
# createTime: 2024/4/1 13:49:16
# describe: 涉及到用户视图、lab视图相关功能
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile


def userLabOvew(driver):
    data_overview = driver.find_element(by=By.XPATH, value=ConfigFile.data_body_xpath)
    data_overview.click()
    time.sleep(2)

    user_overview = driver.find_element(by=By.XPATH, value=ConfigFile.user_overview_xpath)
    user_overview.click()
    time.sleep(2)

    move_toelement(driver, ConfigFile.operation_record_xpath)

    user_constomer = driver.find_element(by=By.XPATH, value=ConfigFile.user_constomer_xpath)
    user_constomer.click()
    time.sleep(2)

    move_toelement(driver, ConfigFile.operation_record_cons_xpath)

    lab_overview = driver.find_element(by=By.XPATH, value=ConfigFile.lab_overview_xpath)
    lab_overview.click()
    time.sleep(2)


def move_toelement(driver, xpath):
    operation_record = driver.find_element(by=By.XPATH, value=xpath)
    # 使用 ActionChains 类模拟鼠标动作，执行向下滚动操作
    actions = ActionChains(driver)
    actions.move_to_element(operation_record).perform()

    time.sleep(3)
