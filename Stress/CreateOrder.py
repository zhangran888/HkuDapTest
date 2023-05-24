# author: zhangran
# createTime: 2023/5/11 16:39:02
# describe:创建500个学生用户的订单生成500个用户，同时给500个用户创建对应一笔订单
import time

import requests
import random

# 输入参数定义区域 #公司演示环境地址
# API_ENDPOINT = "http://dap.datacyber.com/api/client/lab/subscription/add"
# 压测地址
API_ENDPOINT = "http://120.26.166.101/api/client/lab/subscription/add"
# jwtToken = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZWFAMS5jb20iLCJpYXQiOjE2ODM3OTMwNTQsImFjY291bnQiOiJ0ZWFAMS5jb20iLCJqdGkiOiI5ZjNiYWJkYS1kNjllLTQ2MTgtOWVhNi0wZjJmNTdmZWVjNzQifQ.T4FZgUG1xlPArfAtyMs-9ngBwYam5x3B7bKEy3mhkPg"
jwtToken = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZWFAMS5jb20iLCJpYXQiOjE2ODQ4OTM1OTUsImFjY291bnQiOiJ0ZWFAMS5jb20iLCJqdGkiOiJkYWU1ZjYxYy1lZjUzLTQwN2MtYjMxYS1jZGQ2NjE1NzUxZmEifQ.1p97rObyX4-SmugjxVccr8bSktnuvRXAN8xQv6HVQoE"
headers = {"jwtToken": f"{jwtToken}", "Content-Type": "application/json;charset=UTF-8"}

TOTAL_ORDERS = 50
STUDENT_TYPES = ["HKU"]
labId = "1659122395938656257"
labPriceId = "1659122501932912642"


# 循环创建订单
for i in range(TOTAL_ORDERS):
    # 构造通用的订单信息
    order_info = {
        "accessType": "Individual Student",
        "currency": "USD",
        "delegates": {
            "firstName": "",
            "lastName": "",
            "emailAddress": "",
            "phone": ""
        },
        "labId": labId,
        "label": "testCode",
        "file_expire_date": "",
        "labPriceId": labPriceId,
        "payExtraHour": "0",
        "payMethod": "schoolPay",
        "scheduleLabSession": "0"
    }
    # 随机生成一个学生信息
    student_list = []
    for j in range(10):
        student_info = {
            "firstName": f"student{i*10 + j + 1}",
            "lastName": f"stln{i*10 + j + 1}",
            "emailAddress": f"student{i*10 + j + 1}@example.com",
            "studentType": random.choice(STUDENT_TYPES),
            "studentNumber": f"{i*10 + j + 1}"
        }
        student_list.append(student_info)
    # 将学生信息加入到订单信息中
    order_info["studentList"] = student_list

    # 发送 HTTP POST 请求创建订单
    response = requests.post(API_ENDPOINT, json=order_info, headers=headers)
    time.sleep(12)
    print(response.json())

    # 检查响应是否成功
    if response.status_code == requests.codes.ok:
        print(f"订单{i + 1} 创建成功，包含 {len(student_list)} 名学生.")
    else:
        print(f"订单创建失败 {i + 1}. Error: {response.text}")

