# author: zhangran
# createTime: 2024/4/1 13:49:50
# describe: 订单相关功能
import time

from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile


def TrialSubscition(driver, username):
    if username == "testACRC":
        acrc_order_management = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_order_management_xpath)
        acrc_order_management.click()
        time.sleep(2)

        acrc_trial_order = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_trial_order_xpath)
        acrc_trial_order.click()
        time.sleep(2)

        acrc_trial_order_detail = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_trial_order_detail_xpath)
        acrc_trial_order_detail.click()
        time.sleep(2)
        acrc_trial_order_detail_back = driver.find_element(by=By.XPATH,
                                                           value=ConfigFile.acrc_trial_order_detail_back_xpath)
        acrc_trial_order_detail_back.click()
        time.sleep(2)

        acrc_subscription_order = driver.find_element(by=By.XPATH, value=ConfigFile.acrc_subscription_order_xpath)
        acrc_subscription_order.click()
        time.sleep(2)
        acrc_subscription_order_detail = driver.find_element(by=By.XPATH,
                                                             value=ConfigFile.acrc_subscription_order_detail_xpath)
        acrc_subscription_order_detail.click()
        time.sleep(2)
        acrc_subscription_order_detail_back = driver.find_element(by=By.XPATH,
                                                                  value=ConfigFile.acrc_subscription_order_detail_back_xpath)
        acrc_subscription_order_detail_back.click()
        time.sleep(2)
    else:
        order_management = driver.find_element(by=By.XPATH, value=ConfigFile.order_management_xpath)
        order_management.click()
        time.sleep(2)

        trial_order = driver.find_element(by=By.XPATH, value=ConfigFile.trial_order_xpath)
        trial_order.click()
        time.sleep(2)

        trial_order_detail = driver.find_element(by=By.XPATH, value=ConfigFile.trial_order_detail_xpath)
        trial_order_detail.click()
        time.sleep(2)
        trial_order_detail_back = driver.find_element(by=By.XPATH, value=ConfigFile.trial_order_detail_back_xpath)
        trial_order_detail_back.click()
        time.sleep(2)

        subscription_order = driver.find_element(by=By.XPATH, value=ConfigFile.subscription_order_xpath)
        subscription_order.click()
        time.sleep(2)
        subscription_order_detail = driver.find_element(by=By.XPATH, value=ConfigFile.subscription_order_detail_xpath)
        subscription_order_detail.click()
        time.sleep(2)
        subscription_order_detail_back = driver.find_element(by=By.XPATH,
                                                             value=ConfigFile.subscription_order_detail_back_xpath)
        subscription_order_detail_back.click()
        time.sleep(2)
