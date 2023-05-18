# author: zhangran
# createTime: 2023/5/11 16:10:21
# describe:

# 登录并定义字典，存储不同用户的jwtToken数据
import json
import time

import pyautogui
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver


def login():
    # 从 txt 文件中读取用户名和密码
    with open(r'D:\PycharmProjects\HkuDapTest\user_info.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            chromepath = r"D:\\chromedriver_32_113\\chromedriver.exe"
            options = Options()
            options.headless = True
            driver = webdriver.Chrome(options=options, executable_path=chromepath)
            # open打开容器获取新开浏览器地址
            driver.get("http://47.96.2.99/dap-client/#/Signin")
            username_email = driver.find_element_by_css_selector('input[placeholder="Email"]')
            username_email.send_keys(username)
            password_email = driver.find_element_by_css_selector('input[placeholder="Password"]')
            password_email.send_keys(password)
            loginbtn = driver.find_element_by_class_name("el-button--large")
            loginbtn.click()
            open_url = driver.current_url
            print("标题" + driver.title + "访问地址" + open_url)

            # time.sleep(100)


if __name__ == '__main__':
    login()
