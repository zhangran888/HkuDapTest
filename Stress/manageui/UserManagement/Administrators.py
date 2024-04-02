# author: zhangran
# createTime: 2024/4/1 13:49:58
# describe: 用户相关功能
import time

from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile


def AdminiCoustmer(driver, username):
    if username == "testACRC":
        acrc_user_management = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_user_management_xpath)
        acrc_user_management.click()
        time.sleep(2)

        acrc_administrators = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_administrators_xpath)
        acrc_administrators.click()
        time.sleep(2)

        acrc_customers = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_customers_xpath)
        acrc_customers.click()
        time.sleep(5)
    else:
        user_management = driver.find_element(by=By.XPATH, value=ConfigFile.user_management_xpath)
        user_management.click()
        time.sleep(2)

        administrators = driver.find_element(by=By.XPATH, value=ConfigFile.administrators_xpath)
        administrators.click()
        time.sleep(2)

        customers = driver.find_element(by=By.XPATH, value=ConfigFile.customers_xpath)
        customers.click()
        time.sleep(5)
