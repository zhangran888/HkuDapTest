# author: zhangran
# createTime: 2024/3/19 10:27:43
# describe:
import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

driver_path = r"D:\\chromedriver_32_122\\chromedriver.exe"
global_token_dict = {}

if __name__ == '__main__':
    # optionsA = webdriver.ChromeOptions()
    # serviceA = Service(executable_path=driver_path)
    # driver = webdriver.Chrome(options=optionsA, service=serviceA)
    # driver.get("https://dap.acrc.hku.hk/hku-dap-client/#/Signin")
    #
    #
    # time.sleep(10000)

    # 从 txt 文件中读取用户名和密码
    with open(r'D:\PycharmProjects\HkuDapTest\user_zero.txt', 'r') as f:
        for line in f:
            username, password = line.strip().split(':')
            # 构造登录请求的参数
            url = 'https://dap.acrc.hku.hk/api/client/student/user/login'
            headers = {"Content-Type": "application/json;charset=UTF-8"}

            data = {
                'username': username,
                'password': password
            }
            json_data = json.dumps(data)

            # 发送登录请求
            response = requests.post(url, data=json_data, headers=headers)
            # 检查响应是否成功
            if response.json()['code'] == 0:
                # 获取返回的 token 数据
                jwtToken = response.json()['data']
                global_token_dict[username] = jwtToken
                print(f'{username} 成功获取到 jwtToken：{jwtToken}')
            else:
                print(f'jwtToken获取失败：{jwtToken}')