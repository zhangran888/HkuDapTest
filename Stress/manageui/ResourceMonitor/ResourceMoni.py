# author: zhangran
# createTime: 2024/4/1 13:49:29
# describe: 镜像、数据集、数据资源相关功能
import time

from selenium.webdriver.common.by import By

from Stress.manageui import ConfigFile


def MirrorDatasetSource(driver, username):
    if username == "testIT" or username == "testACRC":
        data_overview = driver.find_element(by=By.XPATH, value=ConfigFile.data_body_xpath)
        data_overview.click()
        time.sleep(2)

        it_dataset_list = driver.find_element(by=By.XPATH, value=ConfigFile.it_dataset_list_xpath)
        it_dataset_list.click()
        time.sleep(2)

        it_datasource_list = driver.find_element(by=By.XPATH, value=ConfigFile.it_datasource_list_xpath)
        it_datasource_list.click()
        time.sleep(2)
    else:
        resource_monitoring = driver.find_element(by=By.XPATH, value=ConfigFile.resource_monitoring_xpath)
        resource_monitoring.click()
        time.sleep(2)

        mirror_list = driver.find_element(by=By.XPATH, value=ConfigFile.mirror_list_xpath)
        mirror_list.click()
        time.sleep(2)

        dataset_list = driver.find_element(by=By.XPATH, value=ConfigFile.dataset_list_xpath)
        dataset_list.click()
        time.sleep(2)

        datasource_list = driver.find_element(by=By.XPATH, value=ConfigFile.datasource_list_xpath)
        datasource_list.click()
        time.sleep(2)
