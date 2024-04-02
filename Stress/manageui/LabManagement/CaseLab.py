# author: zhangran
# createTime: 2024/4/1 13:49:40
# describe: case、Lab相关功能
import time

from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile


def CaseLab(driver, username):
    if username == "testIT" or username == "testACRC":
        it_lab_management = driver.find_element(by=By.XPATH, value=ConfigFile.it_lab_management_xpath)
        it_lab_management.click()
        time.sleep(2)

        it_case_list = driver.find_element(by=By.XPATH, value=ConfigFile.it_case_list_xpath)
        it_case_list.click()
        time.sleep(2)

        it_case_list_dataset = driver.find_element(by=By.XPATH, value=ConfigFile.it_case_list_dataset_xpath)
        it_case_list_dataset.click()
        time.sleep(2)

        it_case_list_dataset_cancel = driver.find_element(by=By.XPATH,
                                                          value=ConfigFile.it_case_list_dataset_cancel_xpath)
        it_case_list_dataset_cancel.click()
        time.sleep(2)

        it_lab_list = driver.find_element(by=By.XPATH, value=ConfigFile.it_lab_list_xpath)
        it_lab_list.click()
        time.sleep(2)
    else:
        lab_management = driver.find_element(by=By.XPATH, value=ConfigFile.lab_management_xpath)
        lab_management.click()
        time.sleep(2)

        case_list = driver.find_element(by=By.XPATH, value=ConfigFile.case_list_xpath)
        case_list.click()
        time.sleep(2)

        case_list_dataset = driver.find_element(by=By.XPATH, value=ConfigFile.case_list_dataset_xpath)
        case_list_dataset.click()
        time.sleep(2)

        case_list_dataset_cancel = driver.find_element(by=By.XPATH, value=ConfigFile.case_list_dataset_cancel_xpath)
        case_list_dataset_cancel.click()
        time.sleep(2)

        lab_list = driver.find_element(by=By.XPATH, value=ConfigFile.lab_list_xpath)
        lab_list.click()
        time.sleep(2)
