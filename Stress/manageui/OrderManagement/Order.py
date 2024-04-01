# author: zhangran
# createTime: 2024/4/1 13:49:50
# describe: 订单相关功能
import time

from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile


def TrialSubscition(driver):
    order_management = driver.find_element(by=By.XPATH, value=ConfigFile.order_management_xpath)
    order_management.click()
    time.sleep(2)

    trial_order = driver.find_element(by=By.XPATH, value=ConfigFile.trial_order_xpath)
    trial_order.click()
    time.sleep(2)

    subscription_order = driver.find_element(by=By.XPATH, value=ConfigFile.subscription_order_xpath)
    subscription_order.click()
    time.sleep(2)
